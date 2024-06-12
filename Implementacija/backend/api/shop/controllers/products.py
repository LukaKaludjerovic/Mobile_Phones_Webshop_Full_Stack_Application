"""
author: Luka Mladenovic 0108-2021
author: Andrija Gajic 0033-2021
"""


import csv
import io
import json

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from api.models import add_to_cart, get_all_supported_products, get_all_products, \
    get_lowest_price_product, add_supported_product, add_supported_product_pictures, add_product, get_products_by_seller, get_user_by_username, \
    get_supported_product_by_name, Reseller, get_supported_product_by_id, get_products_by_supported_product, get_cart_by_customer \
    , remove_from_cart, add_transaction

from api.models import get_product_by_id, \
        get_city_by_name, add_city, add_location
from api.models import get_product_by_id

import math

def calculate_distance(lat1, lon1, lat2, lon2):
    # Radius of the earth in km
    R = 6371.0

    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Differences
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance
    distance = R * c
    return distance

def handle_insert_location(request):
    """
    Controller function to insert a location based on form data submission.

    :param request: HttpRequest - The POST request containing 'address'.
    :return: JsonResponse indicating the result of the operation, either successful or an error message.
    """
    try:
        data = json.loads(request.body)
        address = data.get('address')
        zip = data.get('zip')
        city = data.get('city')
        city_obj = get_city_by_name(city)
        if city_obj is None:
            city_obj = add_city(city) 
        add_location(street=address, city=city_obj, postal_code=zip, number=-1, x_coord=-1, y_coord=-1)
        
    except KeyError:
        return JsonResponse({"error": "Invalid request: bad format"}, status=400)

    # full_address, city, zip_code, street_number, lat, lon = get_geocode_data(address) #TODO: Woohan job :D
    return JsonResponse({"message": "Location added successfully"}, status=200)

def handle_get_cart(request):
    """
    Controller function to return the user's cart.
    
    :param request: HttpRequest - The GET request containing the user.
    :return: JsonResponse containing a list of products in the user's cart with details including name, price and photo location.
    """
    user = request.user
    customer = get_user_by_username(user.username)
    
    carts = get_cart_by_customer(customer)
    data = {
        "products": [
            {
                "product": cart.product.supported_product.name,
                "name": cart.product.seller.forename,
                "location": cart.product.seller.location.city.name if cart.product.seller.location else "N/A",
                "price": cart.product.price,
                "quantity": cart.quantity,
                "photo": cart.product.supported_product.pictures.first().picture.url,
                "id": cart.product.id,
            } for cart in carts
        ]
    }
    
    return JsonResponse(data)
    
      
    


def handle_get_product(product_id):
    """
    Controller function to return detailed information about a specific product by product ID.

    :param product_id: int - The unique identifier of the product.
    :return: JsonResponse containing information about the product including name, type, description,
     specification, photo location, and offers with reseller_name, reseller_id, product_id, price and location.
    """

    supported_product=get_supported_product_by_id(product_id)
    products=get_products_by_supported_product(supported_product)


    offers=[]
    for product in products:
        offers.append({
            "id": product.id,
            "name": product.seller.forename,
            "price": product.price,
            "location": product.seller.location.street if product.seller.location else "N/A",
        })

    data = {
        "name": supported_product.name,
        "type": supported_product.type,
        "description": supported_product.description,
        "photo_location": supported_product.pictures.first().picture.url,
        "specification": supported_product.specifications,
        "offers": offers
    }
    print(data)
    return JsonResponse(data)

def calculate_best_product(data):
    """
    Function to calculate the best product based on the lowest price.

    :param data: dict - The dictionary containing a list of sellers with details including name, price and location.
    :return: None
    """
    best_price = 1000000
    best_seller = None

    for seller in data['sellers']:
        price = seller['price']
        if price < best_price:
            best_price = price
            best_seller = seller

    return best_seller

def handle_get_products():
    """
    Controller function to return a list of all registered products.

    :return: JsonResponse containing a list of products with details including name, starting price and photo location.
    """

    products = get_all_supported_products()
    data = {
        "products": [
            {
                "name": product.name,
                "price_from": get_lowest_price_product(product).price if get_lowest_price_product(product) else 'N/A',
                "photo_location": product.pictures.first().picture.url,
                "brand": product.brand,
                "id": product.id
            } for product in products
        ]
    }
    return JsonResponse(data)

def search_products(request):
    """
    Controller function to search for products based on a search query.

    :param request: HttpRequest - The GET request containing the search query.
    :return: JsonResponse containing a list of products with details including name, starting price and photo location.
    """
    data = handle_get_products()
    query = request.GET.get('query', None)
    if query:
        data['products'] = list(filter(lambda product: query.lower() in product['name'].lower(), data['products']))
    return JsonResponse(data)

def handle_get_all_sellers_for_product(request):
    """
    Controller function to return a list of all sellers offering a specific product.
    
    :param request: HttpRequest - The GET request containing the product ID.
    :return: JsonResponse containing a list of sellers with details including name, price and location.
    """
    product_id = 1
    # product_id = request.GET.get('product_id', None)
    data = {
        "sellers": [
            {
                "name": "3g shop",
                "price": 900,
                "location": "Kraljice Natalije 11",
                "rating": "4.5/5",
                "x_coordinate": "44.786568",
                "y_coordinate": "20.448921"
                
            },
            {
                "name": "4g shop",
                "price": 920,
                "location": "Kraljice Natalije 12",
                "rating": "4.3/5",
                "x_coordinate": "44.786568",
                "y_coordinate": "20.448921"
            }
        ]
    }

    # data = get_all_sellers(product_id) #TODO: Woohan job :D
    return JsonResponse(data)

def handle_get_all_products_for_seller(request):
    """
    Controller function to return a list of all products offered by a specific seller.

    :param request: HttpRequest - The GET request containing the seller ID.
    :return: JsonResponse containing a list of products with details including name, starting price and photo location.
    """
    
    user = request.user
    reseller = get_user_by_username(user.username)
    print(user.username)

    data1 = get_products_by_seller(reseller) #TODO: Woohan job :D
    print(data1)
    data = {
        "products": [
            {
                "name": product.supported_product.name,
                "price_from": product.price,
                "photo_location": product.supported_product.pictures.first().picture.url,
                "id": product.id
            } for product in data1
        ]
    }
    print(data)
    return JsonResponse(data)

@login_required(login_url='login')
def handle_get_reccomended_product(request):
    """
    Controller function to return a list of recommended products for the logged-in user.

    :param request: HttpRequest - The POST request containing the user ID.
    :return: JsonResponse containing a list of recommended products with details including name, starting price and photo location.
    """
    data = json.loads(request.body)
    username = data.get('username')
    customer = get_user_by_username(username)
    try: 
        data = json.loads(request.body)
        x = data.get('x')
        y = data.get('y')
        supportedProduct = data.get('supportedProduct')
        supportedProduct = get_supported_product_by_id(supportedProduct)
        products = get_products_by_supported_product(supportedProduct)
        best_product = None
        best_distance = 0
        for product in products:
            if(product.seller.location is None):
                distance = 10
            else:
                x_shop = product.seller.location.x_coord
                y_shop = product.seller.location.y_coord
                distance = calculate_distance(x, y, x_shop, y_shop)
                if distance > 10:
                    distance = 10
            if best_product is None:
                best_product = product
                best_distance = distance
            elif best_product.price + best_distance * 10  - product.price - distance * 10 > 0:
                best_product = product
                best_distance = distance
        data = {
            "product": best_product.supported_product.name,
            "name": best_product.seller.forename,
            "location": best_product.seller.location.city.name if best_product.seller.location else "N/A",
            "price": best_product.price,
            "photo": best_product.supported_product.pictures.first().picture.url,
            "id": best_product.id,
        }
        return JsonResponse(data)
        
    except KeyError:
        return JsonResponse({"error": "Invalid request: bad format"}, status=400)
    

@login_required(login_url='login')
def handle_add_product_to_cart(request):
    """
    Controller function to add a product to the user's cart.

    :param request: HttpRequest - The POST request containing the product ID.
    :return: JsonResponse containing a message indicating the result of the operation.
    """
    user = request.user
    customer = get_user_by_username(user.username)
    print(user.username)
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        print(data)
        print(product_id)
    except KeyError:
        return JsonResponse({"error": "Invalid request: bad format"}, status=400)
    product = get_product_by_id(product_id)
    print(product)
    add_to_cart(customer, product) #TODO: Woohan job :D
    status, message = 200, "Item added to cart successfully"

    if status != 200:
        return JsonResponse({"error": f"Invalid request: {message}"}, status=status)
    return JsonResponse({"message": "Item added to cart successfully"}, status=200)

@login_required(login_url='login')
def handle_remove_product_from_cart(request):
    """
    Controller function to remove a product from the user's cart.

    :param request: HttpRequest - The POST request containing the product ID.
    :return: JsonResponse containing a message indicating the result of the operation.
    """
    user = request.user
    customer = get_user_by_username(user.username)
    
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
    except KeyError:
        return JsonResponse({"error": "Invalid request: bad format"}, status=400)
    product = get_product_by_id(product_id)
    remove_from_cart(customer, product)
    
    status, message = 200, "Item removed from cart successfully"
    
    if status != 200:
        return JsonResponse({"error": f"Invalid request: {message}"}, status=status)
    return JsonResponse({"message": "Item removed from cart successfully"}, status=200)

def handle_insert_transaction(request):
    """
    Controller function to insert a transaction based on form data submission.

    :param request: HttpRequest - The POST request containing 'customer_id', 'product_id', 'quantity', and 'price'.
    :return: JsonResponse indicating the result of the operation, either successful or an error message.
    """
    user = request.user
    customer = get_user_by_username(user.username)
    # get all carts
    carts = get_cart_by_customer(customer)
    # get all products from carts
    products_plus_quantities = [(cart.product, cart.quantity) for cart in carts]
    resellers = [product.seller for (product, quantity) in products_plus_quantities]
    # get all unique resellers
    resellers = list(set(resellers))
    try:
        data = json.loads(request.body)
        address = data.get('address')
        zip = data.get('zip')
        city = data.get('city')
        type = data.get('type')
        # add city if it does not exist
        city_obj = get_city_by_name(city)
        if not city_obj:
            city_obj = add_city(city)

        print(city)
        print(city_obj)
        # add location
        location = add_location(street=address, city=city_obj, postal_code=zip, number=-1, x_coord=-1, y_coord=-1)
        for reseller in resellers:
            # get all products from reseller
            reseller_products_and_quantities = [(product, quantity) for (product, quantity) in products_plus_quantities if product.seller == reseller]
            reseller_products = [product for (product, quantity) in reseller_products_and_quantities]
            reseller_quantites = [quantity for (product, quantity) in reseller_products_and_quantities]
            add_transaction(customer, reseller, reseller_products, location=location, transaction_type=type, quantities=reseller_quantites)
        # remove all products from cart
        for cart in carts:
            for i in range(cart.quantity):
                remove_from_cart(customer, cart.product)
    except KeyError:
        return JsonResponse({"error": "Invalid request: bad format"}, status=400)

    status, message = 200, "Transaction added successfully"

    if status != 200:
        return JsonResponse({"error": f"Invalid request: {message}"}, status=status)
    return JsonResponse({"message": "Transaction added successfully"}, status=200)

def handle_manual_product_insert(request):
    """
    Controller function to manually insert a product based on form data.

    :param request: HttpRequest - The POST request containing 'type', 'storage', 'color', 'price', and 'username'.
    :return: JsonResponse indicating the result of the operation, either successful or an error message.
    """
    try:
        data = json.loads(request.body)
        type = data['type']
        price = data['price']
        username = data['username']
    except (KeyError, json.JSONDecodeError):
        return JsonResponse({"error": "Invalid request: bad format"}, status=400)

    reseller = get_user_by_username(username)
    print(reseller)
    supported_product = get_supported_product_by_name(type)
    print(supported_product)
    if not reseller or not isinstance(reseller, Reseller):
        return JsonResponse({"error": "Invalid reseller"}, status=500)

    if not supported_product:
        return JsonResponse({"error": "Invalid item"}, status=501)

    add_product(supported_product, price, reseller)

    return JsonResponse({"message": "Item added successfully"}, status=200)


def handle_api_product_insert(request):
    """
    Controller function to insert a product based on JSON body of API request.

    :param request: HttpRequest - The POST request with a JSON body containing 'api_key', 'supported_item_id', and 'price'.
    :return: JsonResponse indicating the result of the operation, either successful or an error message.
    """
    try:
        data = json.loads(request.body)
        api_key = data['api_key']
        type = data['type']
        price = data['price']
        username = data['username']
    except (KeyError, json.JSONDecodeError):
        return JsonResponse({"error": "Invalid request: bad format or missing data"}, status=400)

    if not api_key:
        return JsonResponse({"error": "Unauthorized request: incorrect API key"}, status=403)


    reseller = get_user_by_username(username)

    if not reseller:
        return JsonResponse({"error": "Unauthorized request: incorrect username"}, status=403)

    supported_product = get_supported_product_by_name(type)

    if not supported_product:
        return JsonResponse({"error": "Unauthorized request: incorrect supported_product"}, status=403)

    add_product(supported_product, price, reseller)

    return JsonResponse({"message": "Item added successfully"}, status=200)

@login_required(login_url='login')
def handle_serialized_product_insert(request):
    """
    Controller function to insert multiple products from a CSV file.

    :param request: HttpRequest - The POST request that must include a CSV file with 'supported_item_id' and 'price' headers.
    :return: JsonResponse containing the status of each product operation result, either successful or an error message.
    """
    user = request.user
    reseller = get_user_by_username(user.username)

    file = request.FILES['file']
    data = file.read().decode('utf-8')
    csv_data = csv.DictReader(io.StringIO(data))

    if 'supported_item_id' not in csv_data.fieldnames or 'price' not in csv_data.fieldnames:
        return JsonResponse({'error': 'Invalid request: csv missing required columns'}, status=400)

    results = []

    for row in csv_data:
        print(row)
        try:
            supported_product = get_supported_product_by_id(row['supported_item_id'])
            product = add_product(supported_product,row['price'],reseller)
            results.append(product.id)
        except:
            pass


    return JsonResponse({'results': results}, status=200)



def handle_supported_product_insert(request):
    """
    Controller function to insert a product based on form data submission.

    :param request: HttpRequest - The POST request containing 'name', 'description', 'specifications, ''type', 'brand' and 'pictures'. 
    :return: JsonResponse indicating the result of the operation, either successful or an error message.
    """
    
    try:
        name = request.POST['name']
        description = request.POST['description']
        specification = request.POST['specification']
        type = request.POST['type']
        brand = request.POST['brand']
        pictures = request.FILES.getlist('pictures')
        supported_product = add_supported_product(name, description, specification, type, brand)
        add_supported_product_pictures(supported_product, pictures)
        return JsonResponse({"message": "Item added successfully"}, status=200)
    except KeyError:
        return JsonResponse({"error": "Invalid request: bad format"}, status=400)
