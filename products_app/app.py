import csv
import os
import requests
import json

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
    # # First, read products from file...
    products = read_products_from_file()

    # Then, prompt the user to select an operation...
    print(menu())
    operation = input("Please select an operation: ")

    # Then, handle selected operation: "List", "Show", "Create", "Update", "Destroy" or "Reset"...
    if operation.title() == "List":
        porducts = list_products()
    elif operation.title() == "Show":
        show_product()
    elif operation.title() == "Create":
        id = get_largest_product_id(products) if len(products) > 0 else 0
        create_product_with_id(id+1)
    elif operation.title() == "Update":
        update_product()
    elif operation.title() == "Destroy":
        destroy_product()
    elif operation.title() == "Reset":
        reset_products_file()
        return
    else:
        print("Sorry, that operation was not recognized.")
    # Finally, save products to file so they persist after script is done...
    # write_products_to_file(products=products)

#
# Helper functions
#
def product_by_id(product_id, products):
    return [product for product in products if str(product["id"]) == product_id]

# Used to extract plain dictionary from object returned in product_by_id()
def product_as_dict(product_list):
    return dict(product_list[0])

def prod_id(row):
    return int(row["id"])

def get_largest_product_id(products):
    sorted_products = sorted(products, key=prod_id)
    sorted_products.reverse()
    top_prod = sorted_products[0]
    return int(top_prod["id"])

#
# List Products
#
def list_products():
    request_url = "https://nyu-info-2335-products-api-csv.herokuapp.com/products"
    response = requests.get(request_url)

    products = []
    try:
        products = json.loads(response.text)
        header_string = f"--------------------------------\nLISTING {len(products)} PRODUCTS:\n--------------------------------"
        print(header_string)
        for product in products:
            print(" #" + str(product["id"]) + ":", product["name"])
    except ValueError:
        print("Invalid response. Please try again.")

    return products

#
# Show Product
#
def show_product():
    product_id = input("Ok. Please specify the product's identifier: ")

    request_url = "https://nyu-info-2335-products-api-csv.herokuapp.com/products/" + product_id
    response = requests.get(request_url)

    try:
        product_list = json.loads(response.text)
        # If we reach here, api returned a product
        header_string = "--------------------------------\nSHOWING A PRODUCT:\n--------------------------------"
        print(header_string)
        print(product_list)
    except ValueError:
        print("There is no product with that identifier.")


#
# Create Product
#
def create_product_with_id(id):
    product_name = input("Ok. Please input the product's 'name': ")
    product_aisle = input("Ok. Please input the product's 'aisle': ")
    product_dept = input("Ok. Please input the product's 'department': ")
    product_price = input("Ok. Please input the product's 'price': ")

    product_dict = {"id": id, "name": product_name, "aisle": product_aisle, "department": product_dept, "price": product_price}
    request_url = "https://nyu-info-2335-products-api-csv.herokuapp.com/products"
    response = requests.post(request_url, json=product_dict)

    try:
        response_data = json.loads(response.text)
        header_string = "--------------------------------\nCREATING A NEW PRODUCT:\n--------------------------------"
        print(header_string)
        print(response_data)
    except ValueError:
        print("Invalid response. Please try again.")


#
# Update Product
#
def update_product():
    product_id = input("Ok. Please specify the product's identifier: ")

    request_url = "https://nyu-info-2335-products-api-csv.herokuapp.com/products/" + product_id
    response = requests.get(request_url)

    try:
        product_list = json.loads(response.text)
        # If we reach here, api returned a product
        product_name = input(f"Ok. What is the product's new 'name' (currently '{product_list['name']}'): ")
        product_aisle = input(f"Ok. What is the product's new 'aisle' (currently '{product_list['aisle']}'): ")
        product_dept = input(f"Ok. What is the product's new 'department' (currently '{product_list['department']}'): ")
        product_price = input(f"Ok. What is the product's new 'price' (currently '{product_list['price']}'): ")

        product_dict = {"id": product_id, "name": product_name, "aisle": product_aisle, "department": product_dept, "price": product_price}

        request_url = "https://nyu-info-2335-products-api-csv.herokuapp.com/products/" + product_id
        response = requests.put(request_url, json=product_dict)

        try:
            response_data = json.loads(response.text)
            header_string = "--------------------------------\nUPDATING A PRODUCT:\n--------------------------------"
            print(header_string)
            print(response_data)
        except ValueError:
            print("Invalid response. Please try again.")
    except ValueError:
        print("There is no product with that identifier.")

#
# Destroy Product
#
def destroy_product():
    product_id = input("Ok. Please specify the product's identifier: ")

    request_url = "https://nyu-info-2335-products-api-csv.herokuapp.com/products/" + product_id
    response = requests.delete(request_url)

    try:
        product_list = json.loads(response.text)
        # Check if response is an error message
        if product_list["message"]:
            print(product_list["message"])
        else:
            header_string = "--------------------------------\nDESTROYING A PRODUCT:\n--------------------------------"
            print(header_string)
            print(product_list)
    except ValueError:
        print("There is no product with that identifier.")


# only prompt the user for input if this script is run from the command-line
# this allows us to import and test this application's component functions
if __name__ == "__main__":
    run()
