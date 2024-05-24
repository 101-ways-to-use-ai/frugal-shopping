# Analyse your receipts with LLM
The ultimate tool for savvy shoppers and budget-conscious individuals: a Python-based application that transforms your receipts into powerful insights. 

Snap a photo of your receipt, and let a LLM do the parsing and analysis. you will get detailed information about every item you purchased, helping you track your expenditures with ease. 

This application can be used to track expenditures over time and even get LLM to analyse spending patterns to see where you are spending most of your grocery money. I like to use it for asking LLM whether something is a good deal or not when I am shopping. This way I am sure to always get the best deal.

Make informed decisions and stretch your dollar further with our innovative receipt analysis tool!

![store.png](receipts%2Fstore.png)

### Key Steps

Execute the `schema.py` to create tables in SQLite for storing data if this is your first time running this.

1. Place all receipts in the `receipts` directory provided in the repository.
2. Modify the `config.ini` file to set parameters such as database name and directories for storing receipts.
3. Execute the `run_me.py` file to recursively process all receipts in the directory:
    - Convert receipt images to base64 format.
    - Parse receipts using a large language model (e.g., GPT-4).
4. Review the data stored in the database:
    - Check the "card" table for total spent, store name, timestamp, and individual items.
    - Verify the "items" table for detailed information on each item from the receipts.

Modify the prompt in the `prompt.py` file if needed to customize the parsing requirements.


Ensure that the receipt image file exists on the mentioned path, and 'READ_RECEIPT' is correctly defined.
## Dependencies
- Langchain
- Pydantic
- Base64
- Schema

Before running, please make sure to install these dependencies.
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.