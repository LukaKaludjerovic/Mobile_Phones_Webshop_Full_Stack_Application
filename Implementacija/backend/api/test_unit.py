import json
from django.core.files.uploadedfile import SimpleUploadedFile
import io
import csv
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from api.models import Cart, Customer, Reseller, Transaction, Product, Location, City, SupportedProduct, TransactionProduct, \
    Picture

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
import io
import csv

from api.models import add_to_cart

from django.test import TestCase, Client
from django.contrib.auth import get_user_model

class LoginTest(TestCase):
    """
    Author: Vukan Terzic 0334-2021
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('login')

        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='12345', email="test@mail.com")

    def test_login(self):
        data = {
            'username': 'testuser',
            'password': '12345'
        }

        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Login successful')
        self.assertIn('user_type', response_data)
        self.assertEqual(response_data['user_type'], 'none')

class RemoveProductFromCartTest(TestCase):
    """
    Author: Vukan Terzic 0334-2021
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('remove_product_from_cart')
        reseller = Reseller.objects.create(username='Reseller', password='password', email="a@ga.com", forename="Reseller", surname="Mladenovic", phone="12223890", pib="1456789")
        reseller.save()
        self.customer = Customer.objects.create(username='mladenovicluka', password='123123123', email="mladenoviclukaa@gmail.com",forename="Luka", surname="Mladenovic", phone="123423567890")
        
        self.client.force_login(self.customer)
        suppPro = SupportedProduct.objects.create(name="iPhone 15", description="Good phone", specifications="{'size':64gb}", type="phone", brand="iPhone")
        picture = Picture.objects.create(picture="/static/iphone15promax.jpg")
        suppPro.pictures.add(picture)
        suppPro.save()
        self.product = Product.objects.create(supported_product=suppPro, price=1000.0, seller=reseller)
        
        add_to_cart(self.customer, self.product)

    def test_remove_product_from_cart(self):
        
        data = {
            'product_id': self.product.id
        }
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Item removed from cart successfully')
        self.assertFalse(Cart.objects.filter(customer=self.customer, product=self.product).exists())
        

class RegisterResellerTest(TestCase):
    """
    Author: Vukan Terzic 0334-2021
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('register_reseller')

    def test_register_reseller(self):
        # Define the data to send in the request
        data = {
            'username': 'testreseller',
            'password': '12345',
            'email': 'testreseller@example.com',
            'company_name': 'Test Reseller',
            'phone': '1234567890',
            'repeat_password': '12345',
            'pib': '123456789',
            'city': 'Test City',
            'street': 'Test Street',
            'postal_code': '12345',
            'number': '1',
            'x': '0',
            'y': '0'
        }

        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Registration successful')
        User = get_user_model()
        self.assertTrue(User.objects.filter(username=data['username']).exists())
        user = User.objects.get(username=data['username'])
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
        self.assertTrue(City.objects.filter(name=data['city']).exists())
        self.assertTrue(Location.objects.filter(city__name=data['city'], street=data['street']).exists())
        location = Location.objects.get(city__name=data['city'], street=data['street'])
        self.assertEqual(user.location, location)
        
class RegisterAdminTest(TestCase):
    """
    Author: Vukan Terzic 0334-2021
    """
    def setUp(self):
        self.client = Client()
        self.url =  reverse('register_admin')

    def test_register_admin(self):
        # Define the data to send in the request
        data = {
            'username': 'testadmin',
            'password': '12345',
            'email': 'testadmin@example.com',
            'forename': 'Test',
            'surname': 'Admin',
            'phone': '1234567890',
            'repeat_password': '12345'
        }

        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Registration successful')
        User = get_user_model()
        self.assertTrue(User.objects.filter(username=data['username']).exists())
        user = User.objects.get(username=data['username'])
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)

class GetAllProductsForSellerTest(TestCase):
    """
    Author: Vukan Terzic 0334-2021
    """

    def setUp(self):
        self.client = Client()
        self.url = reverse('get_all_products_for_seller')

    def test_get_all_products_for_seller(self):
        reseller = Reseller.objects.create(username='Reseller', password='password', email="res@gmai.com",
                                           forename="Reseller", surname="Mladenovic", phone="12223890", pib="1456789")
        suppPro = SupportedProduct.objects.create(name="iPhone 15", description="Good phone",
                                                  specifications="{'size':64gb}", type="phone", brand="iPhone")
        picture = Picture.objects.create(picture="/static/iphone15promax.jpg")
        suppPro.pictures.add(picture)
        suppPro.save()
        product = Product.objects.create(supported_product=suppPro, price=1000.0, seller=reseller)
        self.client.force_login(reseller)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        expected_data = {
            "products": [
                {
                    "name": suppPro.name,
                    "price_from": product.price,
                    "photo_location": suppPro.pictures.first().picture.url,
                    "id": product.id
                }
            ]
        }

        self.assertEqual(response_data, expected_data)
class GetAllSellersForProductTest(TestCase):
    """
    Author: Vukan Terzic 0334-2021
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('get_all_sellers_for_product')
    def test_get_all_sellers_for_product(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        expected_data = {
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

        self.assertEqual(response_data, expected_data)
        
class SerializedProductInsertTest(TestCase):
    """
    Author: Vukan Terzic 0334-2021
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('serialized_product_insert')

    def test_insert_serialized_product(self):
        suppPro1 = SupportedProduct.objects.create(name="iPhone 15", description="Good phone", specifications="{'size':64gb}", type="phone", brand="iPhone")
        picture = Picture.objects.create(picture="/static/iphone15promax.jpg")
        suppPro1.pictures.add(picture)
        suppPro1.save()
        suppPro2 = SupportedProduct.objects.create(name="iPhone 16", description="Good phone", specifications="{'size':64gb}", type="phone", brand="iPhone")
        suppPro2.pictures.add(picture)
        suppPro2.save()
        reseller = Reseller.objects.create(username='Reseller', password='password', email="a@ga.com", forename="Reseller", surname="Mladenovic", phone="12223890", pib="1456789")
        self.client.force_login(reseller)
        data = {
            "supported_item_id": [suppPro1.id, suppPro2.id],  # replace with actual supported product IDs
            "price": [1000, 2000]
        }
        csv_file = io.StringIO()
        writer = csv.writer(csv_file)
        writer.writerow(data.keys())
        writer.writerows(zip(*data.values()))
        file_data = SimpleUploadedFile("test.csv", csv_file.getvalue().encode(), content_type='text/csv')
        response = self.client.post(self.url, {'file': file_data})
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('results', response_data)
        response_ids = response_data['results']
        expected_ids = list(Product.objects.values_list('id', flat=True))
        self.assertCountEqual(response_ids, expected_ids)
    
class CustomerViewTest(TestCase):
    """
    Author: Luka Mladenovic 0108-2021
    Author: Andrija Gajic 0033-2021
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('view_customers')

    def test_view_customers(self):
        customer = Customer.objects.create(username='mladenovicluka', password='123123123', email="mladenoviclukaa@gmail.com",forename="Luka", surname="Mladenovic", phone="123423567890")
        city = City.objects.create(name="Beograd")
        location = Location.objects.create(street="Citacka", city=city, postal_code="11253", number=1, x_coord=1, y_coord=1)
        customer.location = location
        customer.save()
        response = self.client.get(self.url)
        expected_data = {
            'customer_count': 1,
            'customers': [{
                'username': customer.username,
                'ime': customer.forename,
                'prezime': customer.surname,
                'lokacija': customer.location.city.name if customer.location and customer.location.city else "",
            }]
        }
        self.assertDictEqual(response.json(), expected_data)

class ResellerViewTest(TestCase):
    """
    Author: Andrija Gajic 0033-2021
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('view_resellers')

    def test_view_resellers(self):
        reseller = Reseller.objects.create(username='Reseller', password='password', email="nesto", forename="5G", surname="", phone="1222345890", pib="1456789")
        city = City.objects.create(name="Beograd")
        reseller.location = Location.objects.create(street="Citacka", city=city, postal_code="11253", number=1, x_coord=1, y_coord=1)
        reseller.save()
        response = self.client.get(self.url)
        expected_data = {
            'reseller_count': 1,
            'resellers': [{
                'username': reseller.username,
                'ime': reseller.forename,
                'prezime': reseller.surname,
                'lokacija': reseller.location.city.name if reseller.location and reseller.location.city else "",
            }]
        }
        self.assertDictEqual(response.json(), expected_data)

class ProductsViewAllTest(TestCase):
    """
    Author: Andrija Gajic 0033-2021
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('view_all_products')

    def test_view_all_products(self):
        suppPro = SupportedProduct.objects.create(name="iPhone 15", description="Good phone", specifications="{'size':64gb}", type="phone", brand="iPhone")
        picture = Picture.objects.create(picture="/static/iphone15promax.jpg")
        suppPro.pictures.add(picture)
        reseller1 = Reseller.objects.create(username='Reseller1', password='password', email="a@gmail.com", forename="Reseller1", surname="Mladendovic", phone="12223890", pib="1456789")
        reseller2 = Reseller.objects.create(username='Reseller2', password='password', email="b@gmail.com", forename="Reseller2", surname="Mladdenovic", phone="1222345890", pib="145789")
        product1 = Product.objects.create(supported_product=suppPro, price=1000.0, seller=reseller1)
        product2 = Product.objects.create(supported_product=suppPro, price=1200.0, seller=reseller2)
        
        response = self.client.get(self.url)
        expected_data = {
            'products': [{
                'name': suppPro.name,
                'price_from': product1.price,
                'photo_location': suppPro.pictures.first().picture.url,
                'brand': suppPro.brand,
                'id': suppPro.id,
            }]
        }
        self.assertDictEqual(response.json(), expected_data)
        
class ProductsViewTest(TestCase):
    """
    Author: Andrija Gajic 0033-2021
    """
    def setUp(self):
        self.client = Client()

    def test_view_products(self):
        suppPro = SupportedProduct.objects.create(name="iPhone 15", description="Good phone", specifications="{'size':64gb}", type="phone", brand="iPhone")
        picture = Picture.objects.create(picture="/static/iphone15promax.jpg")
        suppPro.pictures.add(picture)
        reseller1 = Reseller.objects.create(username='Reseller1', password='password', email="a@gmail.com", forename="Reseller1", surname="Mladendovic", phone="12223890", pib="1456789")
        reseller2 = Reseller.objects.create(username='Reseller2', password='password', email="b@gmail.com", forename="Reseller2", surname="Mladdenovic", phone="1222345890", pib="145789")
        location = Location.objects.create(street="Citacka", city=City.objects.create(name="Beograd"), postal_code="11253", number=1, x_coord=1, y_coord=1)
        reseller1.location = location
        reseller2.location = location
        reseller1.save()
        reseller2.save()
        product1 = Product.objects.create(supported_product=suppPro, price=1000.0, seller=reseller1)
        product2 = Product.objects.create(supported_product=suppPro, price=1200.0, seller=reseller2)
        
        self.url = reverse('view_product', args=[suppPro.id])
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        
        exepcted_data = {
            "name": suppPro.name,
            "type": suppPro.type,
            "description": suppPro.description,
            "photo_location": suppPro.pictures.first().picture.url,
            "specification": suppPro.specifications,
            "offers": [
                {
                    "id": product1.id,
                    "name": reseller1.forename,
                    "price": product1.price,
                    "location": reseller1.location.street,
                },
                {
                    "id": product2.id,
                    "name": reseller2.forename,
                    "price": product2.price,
                    "location": reseller2.location.street,
                }
            ]
        }
        self.assertDictEqual(response.json(), exepcted_data)
        
class InsertProductManualTest(TestCase):
    """
    Author: Andrija Gajic 0033-2021
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('manual_product_insert')
        
    def test_insert_product_manual(self):
        suppPro = SupportedProduct.objects.create(name="iPhone 15", description="Good phone", specifications="{'size':64gb}", type="phone", brand="iPhone")
        picture = Picture.objects.create(picture="/static/iphone15promax.jpg")
        suppPro.pictures.add(picture)
        suppPro.save()
        reseller = Reseller.objects.create(username='Reseller', password='password', email="a@ga.com", forename="Reseller", surname="Mladenovic", phone="12223890", pib="1456789")
        data = {
            
            "type": suppPro.name,
            "price": 1000.0,
            "username": reseller.username,
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.json(), {"message": "Item added successfully"})
        self.assertEqual(Product.objects.count(), 1)
        
class InsertProductApiTest(TestCase):
    """
    Author: Andrija Gajic 0033-2021
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('api_product_insert')
        
    def test_insert_product_api(self):
        suppPro = SupportedProduct.objects.create(name="iPhone 15", description="Good phone", specifications="{'size':64gb}", type="phone", brand="iPhone")
        picture = Picture.objects.create(picture="/static/iphone15promax.jpg")
        suppPro.pictures.add(picture)
        suppPro.save()
        reseller = Reseller.objects.create(username='Reseller', password='password', email="a@ga.com", forename="Reseller", surname="Mladenovic", phone="12223890", pib="1456789")
        data = {
            "api_key": "1234567890",
            "type": suppPro.name,
            "price": 1000.0,
            "username": reseller.username,
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.json(), {"message": "Item added successfully"})
        self.assertEqual(Product.objects.count(), 1)

class TransactionViewTest(TestCase):
    """
    Author: Luka Mladenovic 0108-2021
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('view_transactions')

    def test_view_transactions(self):
        city = City.objects.create(name="Beograd")
        location = Location.objects.create(street="Citacka", city=city, postal_code="11253", number=1, x_coord=1, y_coord=1)
        reseller = Reseller.objects.create(username='Reseller', password='password', email="reseller@gmail.com", forename="ResellerKalu", surname="ResellerMladenovic", phone="1222345890", pib="1456789", location=location)
        customer = Customer.objects.create(username='mladenovicluka', password='123123123', email="mladenoviclukaa@gmail.com",forename="Luka", surname="Mladenovic", phone="12342123567890")
        transaction = Transaction.objects.create(customer=customer, seller=reseller, total_price=1000.0, transaction_type="purchase", location=location)
        supported_product = SupportedProduct.objects.create(name="iPhone 15", description="Good phone", specifications="{'size':64gb}", type="phone", brand="iPhone")
        product = Product.objects.create(supported_product=supported_product, price=1000.0, seller=reseller)
        TransactionProduct.objects.create(transaction=transaction, product=product, quantity=1)
        response = self.client.get(self.url)
        expected_data = {
            'transactions_count': 1,
            'transactions': [{
                'customer': f"{transaction.customer.forename} {transaction.customer.surname}",
                'reseller': transaction.seller.forename,
                'type': transaction.transaction_type,
                'total_price': transaction.total_price,
            }]
        }

        self.assertDictEqual(response.json(), expected_data)



class UserTransactionsViewTest(TestCase):
    """
    Author: Luka Mladenovic 0108-2021
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('view_user_transactions')

    def test_view_user_transactions(self):
        customer = Customer.objects.create(username='mladenovicluka', password='123123123', email="mladenoviclukaa@gmail.com",forename="Luka", surname="Mladenovic", phone="123423567890")
        self.client.force_login(customer)
        city = City.objects.create(name="Beograd")
        location = Location.objects.create(street="Citacka", city=city, postal_code="11253", number=1, x_coord=1, y_coord=1)
        reseller = Reseller.objects.create(username='Reseller', password='password', email="reseller@gmail.com",
                                           forename="ResellerKalu", surname="ResellerMladenovic", phone="1222345890",
                                           pib="1456789", location=location)
        transaction = Transaction.objects.create(customer=customer, seller=reseller, total_price=100.0, transaction_type="purchase")
        response = self.client.post(self.url, data={'username': customer.username}, content_type='application/json')
        expected_data = {
            'transactions_count': 1,
            'amount': transaction.total_price,
            'transactions': [{
                'reseller': transaction.seller.forename,
                'type': transaction.transaction_type,
                'total_price': transaction.total_price,
            }]
        }
        self.assertDictEqual(response.json(), expected_data)


class ChangePasswordTest(TestCase):
    """
    Author: Luka Mladenovic 0108-2021
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('change_password')

    def test_change_password(self):
        customer = Customer.objects.create_user(username='Customer', password='old_password', email="customer@c.com", forename="Customer", surname="Test", phone="1234567890")
        self.client.force_login(customer)
        response = self.client.post(self.url, data={'old_password': 'old_password', 'new_password': 'new_password'}, content_type='application/json')
        self.assertEqual(response.json(), {"message": "Password changed successfully!"})


class DeleteCustomerTest(TestCase):
    """
    Author: Luka Mladenovic 0108-2021
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('delete_customer')

    def test_delete_customer(self):
        customer = Customer.objects.create(username='Customer', password='password', email="customer@c.com", forename="Customer", surname="Test", phone="1234567890")
        response = self.client.post(self.url, data={'username': customer.username},content_type='application/json')
        self.assertEqual(response.json(), {"message": "Customer deleted! "})

class DeleteResellerTest(TestCase):
    """
    Author: Luka Mladenovic 0108-2021
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('delete_reseller')

    def test_delete_reseller(self):
        city = City.objects.create(name="Beograd")
        location = Location.objects.create(street="Citacka", city=city, postal_code="11253", number=1, x_coord=1,
                                           y_coord=1)
        reseller = Reseller.objects.create(username='Reseller', password='password', email="reseller@gmail.com", forename="ResellerKalu", surname="ResellerMladenovic", phone="1222345890", pib="1456789", location=location)

        response = self.client.post(self.url, data={'username': reseller.username}, content_type='application/json')
        self.assertEqual(response.json(), {"message": "Reseller deleted! "})


class RecommendedProductTest(TestCase):
    """
    Author: Luka Mladenovic 0108-2021
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('view_reccomended')

    def test_get_reccomended_product(self):
        customer = Customer.objects.create(username='mladenovicluka', password='123123123', email="mladenoviclukaa@gmail.com",forename="Luka", surname="Mladenovic", phone="12342123567890")
        self.client.force_login(customer)
        city = City.objects.create(name="Beograd")
        location = Location.objects.create(street="Citacka", city=city, postal_code="11253", number=1, x_coord=1,
                                           y_coord=1)
        supported_product = SupportedProduct.objects.create(name="iPhone 15", description="Good phone", specifications="{'size':64gb}", type="phone", brand="iPhone")
        picture = Picture.objects.create(picture="/static/iphone15promax.jpg")
        supported_product.pictures.add(picture)
        reseller = Reseller.objects.create(username='Reseller', password='password', email="reseller@gmail.com",
                                           forename="ResellerKalu", surname="ResellerMladenovic", phone="1222345890",
                                           pib="1456789", location=location)
        product = Product.objects.create(supported_product=supported_product, seller=reseller, price=100.0)
        response = self.client.post(self.url, data={'username': customer.username, 'x': 0, 'y': 0, 'supportedProduct': supported_product.id}, content_type='application/json')
        expected_data = {
            "product": supported_product.name,
            "name": reseller.forename,
            "location": reseller.location.city.name,
            "price": product.price,
            "photo": product.supported_product.pictures.first().picture.url,
            "id": product.id,
        }

        self.assertDictEqual(response.json(), expected_data)

class InsertTransactionTest(TestCase):
    """
    Author: Luka Mladenovic 0108-2021
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('insert_transaction')

    def test_insert_transaction(self):
        customer = Customer.objects.create(username='mladenovicluka', password='123123123', email="mladenoviclukaa@gmail.com",forename="Luka", surname="Mladenovic", phone="12342123567890")
        self.client.force_login(customer)
        response = self.client.post(self.url, data={'address': 'Citacka', 'zip': '11000', 'city': 'Belgrade', 'type': 'purchase'}, content_type='application/json')
        self.assertEqual(response.json(), {"message": "Transaction added successfully"})


class RegisterCustomerTest(TestCase):
    """
    Author: Luka Kaludjerovic 0041-2021
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('register_customer')
    
    def test_register_customer(self):
        data = {
            'username': 'UnitTestCustomer', 
            'password': '123123123', 
            'email': 'unit@test.com', 
            'forename': 'Unit Test', 
            'surname': 'Customer', 
            'phone': '+381123456789', 
            'repeat_password': '123123123'
        }
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Registration successful')
        User = get_user_model()
        self.assertTrue(User.objects.filter(username=data['username']).exists())
        user = User.objects.get(username=data['username'])
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)

class LogoutTest(TestCase):
    """
    Author: Luka Kaludjerovic 0041-2021
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('logout')
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username = 'UnitTestCustomer', 
            password = '123123123', 
            email = 'unit@test.com', 
            forename = 'Unit Test', 
            surname = 'Customer', 
            phone = '+381123456789'
        )
    
    def test_logout(self):
        self.client.login(username='UnitTestCustomer', password='123123123')
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Logout successful')
        self.assertNotIn('_auth_user_id', self.client.session)


class GetRoleTest(TestCase):
    """
    Author: Luka Kaludjerovic 0041-2021
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('get_role')
    
    def test_get_role(self):
        customer = Customer.objects.create(username='mladenovicluka', password='123123123',
                                           email="mladenoviclukaa@gmail.com", forename="Luka", surname="Mladenovic",
                                           phone="12342123567890")
        self.client.force_login(customer)

        response = self.client.post(self.url, data={'username': customer.username},
                                    content_type='application/json')
        expected_data = {"role": "customer"}

        self.assertDictEqual(response.json(), expected_data)


class SupportedProductInsertTest(TestCase):
    """
    Author: Luka Kaludjerovic 0041-2021
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('supported_product_insert')
        self.data = {
            'name': 'iPhone16Pro',
            'description': 'A product for testing.',
            'specification': 'Specifications of the test product.',
            'type': 'Smartphone',
            'brand': 'Apple',
        }
        self.pictures = {
            SimpleUploadedFile("file1.jpg", b"file_content", content_type="image/jpeg"),
            SimpleUploadedFile("file2.jpg", b"file_content", content_type="image/jpeg"),
        }
    
    def test_supported_product_insert(self):
        response = self.client.post(self.url, data=self.data, files={'pictures': self.pictures})
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['message'], 'Item added successfully')

class InsertLocationTest(TestCase):
    """
    Author: Luka Kaludjerovic 0041-2021
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('insert_location')
        self.data = {
            'address': '123 Main St',
            'zip': '12345',
            'city': 'New York',
        }
    
    def test_insert_location(self):
        response = self.client.post(self.url, data=json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['message'], 'Location added successfully')
        

class ViewCartTest(TestCase):
    """
    Author: Andrija Gajic 0033-2021
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse('view_cart')

    def test_view_cart(self):
        customer = Customer.objects.create(username='mladenovicluka', password='123123123', email="a@gmail.com", forename="Luka", surname="Mladenovic", phone="123423567890")
        suppPro = SupportedProduct.objects.create(name="iPhone 15", description="Good phone", specifications="{'size':64gb}", type="phone", brand="iPhone")
        picture = Picture.objects.create(picture="/static/iphone15promax.jpg")
        suppPro.pictures.add(picture)
        suppPro.save()
        reseller = Reseller.objects.create(username='Reseller', password='password', email="nes@gmail.com", forename="Reseller", surname="Mladenovic", phone="12223890", pib="1456789")
        product = Product.objects.create(supported_product=suppPro, price=1000.0, seller=reseller)
        add_to_cart(customer, product)
        self.client.force_login(customer)
        response = self.client.get(self.url)

        expected_data = {
            'products': [{
                'product': suppPro.name,
                'name': reseller.forename,
                'location': "N/A",
                'price': product.price,
                'quantity': 1,
                'photo': suppPro.pictures.first().picture.url,
                'id': product.id,
            }]
        }
        self.assertDictEqual(response.json(), expected_data)
