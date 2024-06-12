"""
author: Luka Mladenovic 0108-2021
author: Andrija Gajic 0033-2021
author: Luka Kaludjerovic 0041-2021
"""
import os

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .shop.controllers.products import handle_get_product, handle_get_products, handle_manual_product_insert, \
    handle_api_product_insert, handle_serialized_product_insert, handle_get_all_sellers_for_product, handle_get_all_products_for_seller \
    ,handle_supported_product_insert, handle_insert_location, handle_get_cart, handle_add_product_to_cart, handle_remove_product_from_cart \
        , handle_insert_transaction, handle_get_reccomended_product
        
from .shop.controllers.users import handle_get_customers, handle_get_resellers, handle_delete_customer, handle_delete_reseller, handle_change_password, handle_get_transactions,handle_view_user_transactions
from .shop.controllers.auth import handle_login, handle_register_admin, handle_register_reseller, \
    handle_register_customer, handle_logout, handle_get_role


@require_http_methods(["GET"])
def view_customers(request):
    """
    View function to return the total count and details of all registered customers. Access is restricted to admin users.

    :param: GET HttpRequest: /api/customers/view

    :return: JsonResponse: Contains 'customer_count' and a list of 'customers' with detailed information.
    """
    return handle_get_customers()


@require_http_methods(["GET"])
def view_resellers(request):
    """
    View function to return the total count and details of all registered resellers. Access is restricted to admin users.

    :param: GET HttpRequest: /api/resellers/view

    :return: JsonResponse: Contains 'reseller_count' and a list of 'resellers' with detailed information.
    """
    return handle_get_resellers()


@require_http_methods(["GET"])
def view_product(request, product_id: int):
    """
    View function to return the details of a specific product by product ID.

    :param: GET HttpRequest: /api/products/view/{product_id}

    :return: JsonResponse: Contains detailed information about the specified product and a list of 'offers' with detailed information.
    """
    return handle_get_product(product_id)


@require_http_methods(["GET"])
def view_all_products(request):
    """
    View function to return details of all registered products.

    :param: GET HttpRequest: /api/products/view/all

    :return: JsonResponse: Contains  list of 'products' with detailed information.
    """
    return handle_get_products()


@csrf_exempt
@require_http_methods(["POST"])
def manual_product_insert(request):
    """
    View function to insert a new product through form data submission.

    :param: POST HttpRequest: /api/products/insert/manual

    :return: JsonResponse: Reports the outcome of the product insertion.
    """
    return handle_manual_product_insert(request)

@csrf_exempt
@require_http_methods(["POST"])
def supported_product_insert(request):
    """
    View function to insert a new product through form data submission.

    :param: POST HttpRequest: /api/products/insert/supported

    :return: JsonResponse: Reports the outcome of the product insertion.
    """
    return handle_supported_product_insert(request)

@csrf_exempt
@require_http_methods(["POST"])
def api_product_insert(request):
    """
    View function to insert a new product via API request with JSON body.

    :param: POST HttpRequest: /api/products/insert/api

    :return: JsonResponse: Reports the outcome of the product insertion.
    """
    return handle_api_product_insert(request)


@csrf_exempt
@require_http_methods(["POST"])
def serialized_product_insert(request):
    """
    View function to insert products from a serialized CSV file.

    :param: POST HttpRequest: /api/products/insert/serialized

    :return: JsonResponse: Reports the status of each product insertion from the CSV.
    """
    return handle_serialized_product_insert(request)

@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    """
    View function to handle user login.

    :param: POST HttpRequest: /api/login

    :return: JsonResponse: Contains 'token' if login is successful, or 'error' if login fails.
    """
    return handle_login(request)

@csrf_exempt
@require_http_methods(["POST"])
def register_reseller(request):
    """
    View function to handle reseller registration.

    :param: POST HttpRequest: /api/register/reseller

    :return: JsonResponse: Contains 'message' if registration is successful, or 'error' if registration fails.
    """
    return handle_register_reseller(request)
@csrf_exempt
@require_http_methods(["POST"])
def register_admin(request):
    """
    View function to handle admin registration.

    :param: POST HttpRequest: /api/register/admin

    :return: JsonResponse: Contains 'message' if registration is successful, or 'error' if registration fails.
    """
    return handle_register_admin(request)

@csrf_exempt
@require_http_methods(["POST"])
def register_customer(request):
    """
    View function to handle customer registration.

    :param: POST HttpRequest: /api/register/customer

    :return: JsonResponse: Contains 'message' if registration is successful, or 'error' if registration fails.
    """
    return handle_register_customer(request)

@csrf_exempt
@require_http_methods(["POST"])
def logout(request):
    """
    View function to handle user logout.

    :param: POST HttpRequest: /api/logout

    :return: JsonResponse: Contains 'message' if logout is successful, or 'error' if logout fails.
    """
    return handle_logout(request)

@require_http_methods(["GET"])
def get_all_sellers_for_product(request):
    """
    View function to return all resellers that offer a specific product.

    :param: GET HttpRequest: /api/products/{product_id}/sellers

    :return: JsonResponse: Contains a list of 'sellers' that offer the specified product.
    """
    return handle_get_all_sellers_for_product(request)

@require_http_methods(["GET"])
def get_all_products_for_seller(request):
    """
    View function to return all products offered by a specific reseller.

    :param: GET HttpRequest: /api/sellers/{seller_id}/products

    :return: JsonResponse: Contains a list of 'products' offered by the specified reseller.
    """
    return handle_get_all_products_for_seller(request)

@csrf_exempt
@require_http_methods(["POST"])
def get_reccomended_product(request):
    """
    View function to return all products offered by a specific reseller.

    :param: POST HttpRequest: /api/sellers/{seller_id}/products

    :return: JsonResponse: Contains a list of 'products' offered by the specified reseller.
    """
    return handle_get_reccomended_product(request)

@csrf_exempt
@require_http_methods(["POST"])
def add_product_to_cart(request):
    """
    View function to add a product to the cart.

    :param: POST HttpRequest: /api/products/add_to_cart

    :return: JsonResponse: Reports the outcome of the product insertion.
    """
    return handle_add_product_to_cart(request)

@csrf_exempt
@require_http_methods(["POST"])
def remove_product_from_cart(request):
    """
    View function to remove a product from the cart.

    :param: POST HttpRequest: /api/products/remove_from_cart

    :return: JsonResponse: Reports the outcome of the product removal.
    """
    return handle_remove_product_from_cart(request)

@csrf_exempt
@require_http_methods(["POST"])
def insert_transaction(request):
    """
    View function to insert a new transaction.

    :param: POST HttpRequest: /api/products/insert/transaction

    :return: JsonResponse: Reports the outcome of the transaction insertion.
    """
    return handle_insert_transaction(request)

@csrf_exempt
@require_http_methods(["POST"])
def insert_location(request):
    """
    View function to insert a new location.

    :param: POST HttpRequest: /api/products/insert/location

    :return: JsonResponse: Reports the outcome of the location insertion.
    """
    return handle_insert_location(request)

@require_http_methods(["GET"])
def view_cart(request):
    """
    View function to return the total count and details of all registered customers. Access is restricted to admin users.

    :param: GET HttpRequest: /api/customers/view

    :return: JsonResponse: Contains 'customer_count' and a list of 'customers' with detailed information.
    """
    return handle_get_cart(request)
def index(request):
    return render(request,'home.html')

def render_about(request):
    return render(request,'about.html')


def render_login(request):
    return render(request,'login.html')

def new_customer(request):
    return render(request,'new-customer.html')

def new_reseller(request):
    return render(request,'new-reseller.html')


def order(request):
    return render(request,'order.html')


def payment(request):
    return render(request,'payment.html')

def shop(request):
    return render(request,'shop.html')

def contact(request):
    return render(request,'contact.html')

def product(request):
    return render(request,'product.html')

def dashboard_customer(request):
    return render(request,'dashboard-customer.html')

def dashboard_reseller(request):
    return render(request,'dashboard-reseller.html')

def dashboard_admin(request):
    return render(request,'dashboard-admin.html')

def cart(request):
    return render(request,'cart.html')

def delivery(request):
    return render(request,'delivery.html')


@csrf_exempt
@require_http_methods(["POST"])
def role(request):
    """
    View function to get user role .

    :param: POST HttpRequest: /api/auth/role

    :return: JsonResponse: Contains user 'role'
    """
    return handle_get_role(request)

@csrf_exempt
@require_http_methods(["POST"])
def delete_customer(request):
    """
    View function to delete customer. 

    :param: POST HttpRequest: /api/delete/customer

    :return: JsonResponse: Contains the error or success message
    """
    return handle_delete_customer(request)

@csrf_exempt
@require_http_methods(["POST"])
def delete_reseller(request): 
    """
    View function to delete reseller. 

    :param: POST HttpRequest: /api/delete/reseller

    :return: JsonResponse: Contains the error or success message
    """
    return handle_delete_reseller(request)

@csrf_exempt
@require_http_methods(["POST"])
def change_password(request):
    """
    View function to change user's password. 

    :param: POST HttpRequest: /api/user/changepassword

    :return: JsonResponse: Contains the error or success message
    """
    return handle_change_password(request)

@require_http_methods(["GET"])
def view_transactions(request):
    """
    View function to return details of all transactions.

    :param: GET HttpRequest: /api/transactions/view/

    :return: JsonResponse: Contains  list of 'transactions' with detailed information.
    """
    return handle_get_transactions()
#
@csrf_exempt
@require_http_methods(["POST"])
def view_user_transactions(request):
    """
    View function to change user's password.

    :param: POST HttpRequest: /api/user/changepassword

    :return: JsonResponse: Contains the error or success message
    """
    return handle_view_user_transactions(request)