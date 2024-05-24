READ_RECEIPT = """
Read this hypothetical receipt from a purchase and extract the key information from it. 
I would like to know date and time of purchase, store name, currency, purchase total and total tax paid, currency of sale.
I also would like you to list out individual items, their quantity, price per item and any discounts that have been applied.
You can make the following assumptions:
- The language may not be English. First, guess the language from the text to ensure accurate parsing.
- The time is local and convert it to a UTC format.
- The store name should likely be taken from the header of the receipt.
- The currency can be assumed from the location or address.
- The purchase total tax is not explicitly mentioned on the receipt, assume it to be 0 or included in the total.
- The items listed on the receipt are to be formatted according to the schema.
- The item quantity units can be assumed to be "num" (number of items) if the receipt does not specify weight or volume for the listed example item.
- The item discount is assumed to be 0 if no discounts are explicitly mentioned on the receipt.
- Provide back all items in your response.
- Do not make any assumptions. Ignore info that is not clearly readable.
- Make sure you read the response format instructions carefully.
- Do not stop for brevity, list out all items that are readable.
"""