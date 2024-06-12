"""
author: Luka Mladenovic 0108-2021
author: Andrija Gajic 0033-2021
"""

from django.urls import path
from .views import view_customers, view_resellers, view_all_products, view_product, manual_product_insert, \
    api_product_insert, serialized_product_insert, get_all_sellers_for_product, get_all_products_for_seller, \
    login, register_admin, register_reseller, register_customer, logout, supported_product_insert, role, \
    insert_location, view_cart, add_product_to_cart, remove_product_from_cart, insert_transaction, get_reccomended_product, \
    delete_customer, delete_reseller, change_password, view_transactions,view_user_transactions
    

urlpatterns = [
    path("customers/view", view_customers, name="view_customers"),
    path("resellers/view", view_resellers, name="view_resellers"),
    path("products/view/all", view_all_products, name="view_all_products"),
    path("products/view/<int:product_id>", view_product, name="view_product"),
    path("products/insert/manual", manual_product_insert, name="manual_product_insert"),
    path("products/insert/api", api_product_insert, name="api_product_insert"),
    path("products/insert/serialized", serialized_product_insert, name="serialized_product_insert"),
    path("products/sellers/product", get_all_sellers_for_product, name="get_all_sellers_for_product"),
    path("products/products/seller", get_all_products_for_seller, name="get_all_products_for_seller"),
    path("auth/login", login, name="login"),
    path("auth/register/admin", register_admin, name="register_admin"),
    path("auth/register/reseller", register_reseller, name="register_reseller"),
    path("auth/register/customer", register_customer, name="register_customer"),
    path("auth/logout", logout, name="logout"),
    path("auth/role", role, name="get_role"),
    path("products/insert/supported", supported_product_insert, name="supported_product_insert"),
    path("products/insert/location", insert_location, name="insert_location"),
    path("products/view/cart", view_cart, name="view_cart"),
    path("products/add/cart", add_product_to_cart, name="add_product_to_cart"),
    path("products/remove/cart", remove_product_from_cart, name="remove_product_from_cart"),
    path("products/insert/transaction", insert_transaction, name="insert_transaction"),
    path("products/view/reccomended", get_reccomended_product, name="view_reccomended"),
    path("delete/customer", delete_customer, name="delete_customer"),
    path("delete/reseller", delete_reseller, name="delete_reseller"),
    path("user/changepassword", change_password, name="change_password"),
    path("user/transactions/view", view_user_transactions, name="view_user_transactions"),
    path("transactions/view", view_transactions, name="view_transactions"),
]
