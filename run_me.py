from langchain.chains import TransformChain
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain import globals
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import PydanticOutputParser
import base64
from typing import Dict
from models import CartModel, ItemModel
from schema import Cart, Item
from prompt import READ_RECEIPT
import os
import shutil
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configparser

# Set verbose
globals.set_debug(False)
config = configparser.ConfigParser()
config.read('config.ini')

class ImageModelProcessor:
    def __init__(self, model_name: str, temperature: float, max_tokens: int, parser: PydanticOutputParser):
        self.model = ChatOpenAI(temperature=temperature, model=model_name, max_tokens=max_tokens)
        self.parser = parser
        self.load_image_chain = TransformChain(
            input_variables=["image_path"],
            output_variables=["image"],
            transform=self.load_image
        )

    @staticmethod
    def encode_image_to_base64(image_path: str) -> str:
        """
        Load image from file and encode it as base64.

        Args:
            image_path (str): The file path to the image.

        Returns:
            str: Base64 encoded image.
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def load_image(self, inputs: Dict[str, str]) -> Dict[str, str]:
        """
        Load image from the provided file path and return a dictionary with the base64 encoded image.

        Args:
            inputs (dict): A dictionary with 'image_path' key.

        Returns:
            dict: A dictionary with 'image' key containing the base64 encoded image.
        """
        image_path = inputs["image_path"]
        image_base64 = self.encode_image_to_base64(image_path)
        return {"image": image_base64}

    def image_model(self, inputs: Dict[str, str]) -> str:
        """
        Invoke model with image and prompt.

        Args:
            inputs (dict): A dictionary with 'prompt' and 'image' keys.

        Returns:
            str: The response from the model.
        """
        msg = self.model.invoke([
            HumanMessage(content=[
                {"type": "text", "text": inputs["prompt"]},
                {"type": "text", "text": self.parser.get_format_instructions()},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{inputs['image']}"}}
            ])
        ])
        return msg.content

    def read_receipt_image(self, image_path: str, prompt_template: str) -> Dict:
        """
        Get image information using a vision model chain.

        Args:
            image_path (str): The file path to the image.
            prompt_template (str): The prompt template for the model.

        Returns:
            dict: The parsed information from the model.
        """
        vision_chain = self.load_image_chain | self.image_model | self.parser
        return vision_chain.invoke({'image_path': image_path, 'prompt': prompt_template})


# Initialize parser (replace 'Cart' with the actual pydantic model)
parser = PydanticOutputParser(pydantic_object=CartModel)

# Create an instance of the ImageModelProcessor
image_processor = ImageModelProcessor(
    model_name="gpt-4-vision-preview",
    temperature=0.5,
    max_tokens=1024,
    parser=parser
)

def process_images():
    # connect to the database
    db_name = config.get('DATABASE', 'Name')
    directory = config.get('GENERAL', 'receipts_dir')
    processed_directory = config.get('GENERAL', 'receipts_processed_dir')

    # Create engine and connect it to sqlite DB
    engine = create_engine(f"sqlite:///{db_name}")
    Session = sessionmaker(bind=engine)
    session = Session()

    # Process each image in the directory
    for filename in os.listdir(directory):

        filepath = os.path.join(directory, filename)

        try:
            cart_result = image_processor.read_receipt_image(filepath, 'READ_RECEIPT')
        except Exception as e:
            print(e)
            continue

        # set up an identifier
        identifier = f"{filename}-{cart_result.store_name}-{cart_result.timestamp}"

        # check if filename has already been processed:
        item = session.query(Cart).filter(Cart.identifier == identifier).first()

        if item:
            print(f"Receipt has already been processed: {identifier}")
            continue

        #cart = CartModel.parse_obj(result)
        cart_db = Cart(store_name=cart_result.store_name, currency=cart_result.currency, purchase_total=cart_result.purchase_total,
                       purchase_total_tax=cart_result.purchase_total_tax, identifier=identifier, filename=filename)

        session.add(cart_db)
        session.commit()

        for item in cart_result.items:
            #item = ItemModel.parse_obj(item_data)
            item_db = Item(item_name=item.item_name, item_quantity=item.item_quantity,
                           item_quantity_units=item.item_quantity_units, item_discount=item.item_discount,
                           item_price=item.item_price, cart_id=cart_db.id)

            session.add(item_db)

        session.commit()

        # Move the image to the processed directory
        shutil.move(filepath, os.path.join(processed_directory, filename))


if __name__ == "__main__":
    # Example usage
    process_images()
