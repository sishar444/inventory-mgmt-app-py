import csv
import os

def menu(username="@prof-rossetti", products_count=100):
    # this is a multi-line string, also using preceding `f` for string interpolation
    menu = f"""
    -----------------------------------
    INVENTORY MANAGEMENT APPLICATION
    -----------------------------------
    Welcome {username}!
    There are {products_count} products in the database.
        operation | description
        --------- | ------------------
        'List'    | Display a list of product identifiers and names.
        'Show'    | Show information about a product.
        'Create'  | Add a new product.
        'Update'  | Edit an existing product.
        'Destroy' | Delete an existing product.
        'Reset'   | Reset the product list to defaults. """ # end of multi- line string. also using string interpolation
    return menu

def read_products_from_file(filename="products.csv"):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    products = []
    # Open the file and populate the products list with product dictionaries
    with open(filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            products.append(row)
    return products

def write_products_to_file(filename="products.csv", products=[]):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    print(f"OVERWRITING CONTENTS OF FILE: '{filepath}' \n ... WITH {len(products)} PRODUCTS")
    # Open the file and write a list of dictionaries. each dict should represent a product.
    with open(filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["id", "name", "aisle", "department", "price"])
        writer.writeheader()
        for product in products:
            writer.writerow(product)


def reset_products_file(filename="products.csv", from_filename="products_default.csv"):
    print("RESETTING DEFAULTS")
    products = read_products_from_file(from_filename)
    write_products_to_file(filename, products)

def run():
    # First, read products from file...
    products = read_products_from_file()

    # Then, prompt the user to select an operation...
    print(menu())
    operation = input("Please select an operation: ")

    # Then, handle selected operation: "List", "Show", "Create", "Update", "Destroy" or "Reset"...
    if operation.title() == "List":
        list_products(products)
    elif operation.title() == "Show":
        show_product(products)
    elif operation.title() == "Destroy":
        # Overwrite products list with new list
        products = destroy_product(products)
    elif operation.title() == "Reset":
        reset_products_file()
        return
    else:
        print("Sorry, that operation was not recognized.")
    # Finally, save products to file so they persist after script is done...
    write_products_to_file(products=products)


def product_by_id(product_id, products):
    return [product for product in products if str(product["id"]) == product_id]

def product_as_dict(product_list):
    return dict(product_list[0])

def list_products(products):
    header_string = f"--------------------------------\nLISTING {len(products)} PRODUCTS:\n--------------------------------"
    print(header_string)
    for product in products:
        print(" #" + product["id"] + ":", product["name"])

def show_product(products):
    product_id = input("Ok. Please specify the product's identifier: ")
    header_string = f"--------------------------------\nSHOWING A PRODUCT:\n--------------------------------"
    print(header_string)
    product_list = product_by_id(product_id, products)
    if len(product_list) > 0:
        print(product_as_dict(product_list))
    else:
        print("There is no product with that identifier.")

def destroy_product(products):
    product_id = input("Ok. Please specify the product's identifier: ")
    header_string = f"--------------------------------\nDESTROYING A PRODUCT:\n--------------------------------"
    print(header_string)
    # Print the details of product to be deleted
    product_list = product_by_id(product_id, products)
    if len(product_list) > 0:
        print(product_as_dict(product_list))
        # Update passed in list to remove product with that id
        products = [prod for prod in products if prod.get('id') != product_id]
    else:
        print("There is no product with that identifier.")

    # Return the new list
    return products

# only prompt the user for input if this script is run from the command-line
# this allows us to import and test this application's component functions
if __name__ == "__main__":
    run()
