"""
    Author: Vukan Terzic 0334-2021
"""

from django.test import TestCase
from api.models import *
import traceback
class MyTests(TestCase):
    def test_add_city(self):
        city = None
        try:
            add_city("Belgrade")
            city = get_city_by_name("Belgrade")
            if city is None:
                print("City is None")
                return
        except:
            print("Error while adding city")
            return
        try:
            add_location(city, "Kneza Milosa", 1, 1, 1, 1)
            location = get_location_by_coords(1, 1)
        except Exception as e:
            print("Error while adding location:", str(e))
            return
        try:
            add_admin(email="mail1", username="user1", password="password", forename="name", surname="surname", phone="012")
            admin = get_user_by_email("mail1")
            if not is_admin(admin):
                print("Admin is not admin")
        except Exception as e:
            print("Error while adding admin:", str(e))
            print(traceback.format_exc())
            return
        try:   
            add_reseller(email="mail2", username="user2", password="password", forename="name", surname="surname", phone="012", pib=1)
            reseller = get_user_by_email("mail2")
            if not is_reseller(reseller):
                print("Reseller is not reseller")
        except Exception as e:
            print("Error while adding reseller:", str(e))
            return
        try:
            add_customer(email="mail3", username="user3", password="password", forename="name", surname="surname", phone="012")
            customer = get_user_by_email("mail3")
            if not is_customer(customer):
                print("Customer is not customer")
        except Exception as e:
            print("Error while adding customer:", str(e))
            return
        try:
            block_user(admin, customer)
            blockedUser = get_user_by_email("mail3")
            if not is_blocked(blockedUser) or blockedUser is None:
                print("Blocked is not blocked")
        except Exception as e:
            print("Error while blocking user:", str(e))
            return
        try:
            add_supported_product(name="product1", description="desc", specifications="spec", type="type", brand="brand")
            product = get_supported_product_by_name("product1")
            if product is None:
                print("Product is None")
                return
        except Exception as e:
            print("Error while adding supported product:", str(e))
            return
        try:
            add_product(product, 1, reseller)
            
            if get_all_products().count() != 1:
                print("Product not added")
        except Exception as e:
            print("Error while adding product:", str(e))
            return
        
        
        
            
        