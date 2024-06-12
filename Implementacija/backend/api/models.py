"""
    Author: Andrija Gajic 0033-2021
    Author: Vukan Terzic 0334-2021
"""
import os
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.files import File
from django.core.files.storage import default_storage


# REDOSLED Klasa: Picture, City, Location, SupportedProduct, User, Product, Rating, Cart, RemovedProduct, TransactionProduct, Transaction
# Picture funkcije: get_supported_product_pictures, add_picture_to_supported_product, add_supported_product_pictures, remove_picture_from_supported_product
# City funkcije: get_all_cities, get_city_by_name, add_city, delete_city


# Location funkcije: get_all_locations, get_location_by_city_and_street_and_number, 
# get_location_by_coords, add_location, delete_location


# SupportedProduct funkcije: get_all_supported_products, 
# get_supported_product_by_id, get_supported_product_by_name, 
# get_supported_product_pictures, change_supported_product_name, 
# change_supported_product_description, change_supported_product_specifications, 
# change_supported_product_type, add_picture_to_supported_product, 
# add_supported_product_pictures, add_supported_product, remove_picture_from_supported_product, 
# delete_supported_product


# User funkcije: get_user_location, get_user_by_username, get_user_by_email, 
# get_user_by_id, add_customer, add_reseller, add_admin, block_user, unblock_user, 
# change_user_location, change_user_username, is_admin, is_blocked, is_customer, 
# is_reseller, user_exists, delete_user


# Product funkcije: get_all_products, get_product_by_id, get_lowest_price_product, 
# get_products_by_seller, get_products_by_supported_product, 
# get_product_by_supported_product_and_seller, add_product, delete_product, change_product_price


# Rating funkcije: get_rating_by_product_and_customer, get_ratings_by_product, 
# get_ratings_by_customer, get_average_rating, change_rating, add_rating, delete_rating


# Cart funkcije: get_cart_by_customer, get_quantity_by_customer, add_to_cart, 
# remove_from_cart, empty_cart, change_cart_quantity, delete_cart


# RemovedProduct funkcije: get_removed_products, get_removed_product_by_product, 
# get_removed_products_by_seller, get_removed_products_by_supported_product, remove_product, 
# unremove_product


# Transaction funkcije: get_transactions_by_customer, get_products_quantity_by_transaction, 
# add_transaction

class Picture(models.Model):
    picture = models.ImageField(upload_to='imgs')

class City(models.Model):
    name = models.CharField(max_length=45)
  
# GETTERS
def get_all_cities():
    """
    Function to get all cities from the database.

    :return: QuerySet of City objects.
    """
    return City.objects.all()

def get_city_by_name(name):
    """
    Function to get a city from the database by name.

    :param name: Name of the city.
    :return: City object if the city exists, None otherwise.
    """
    return City.objects.filter(name=name).first()

# ADDERS
def add_city(name):
    """
    Function to add a city to the database.

    :param name: Name of the city.
    """
    return City.objects.create(name=name)

# DELETERS
def delete_city(city):
    """
    Function to delete a city from the database.

    :param city: City object.
    """
    city.delete()
class Location(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    street = models.CharField(max_length=45)
    postal_code = models.IntegerField()
    number = models.IntegerField()
    x_coord = models.FloatField()
    y_coord = models.FloatField()
    
# GETTERS
def get_all_locations():
    """
    Function to get all locations from the database.

    :return: QuerySet of Location objects.
    """
    return Location.objects.all()


def get_location_by_city_and_street_and_number(city, street, number):
    """
    Function to get a location from the database by city, street and number.

    :param city: City object.
    :param street: Street of the location.
    :param number: Number of the location.
    :return: Location object if the location exists, None otherwise.
    """
    return Location.objects.filter(city=city, street=street, number=number).first()

def get_location_by_coords(x_coord, y_coord):
    """
    Function to get a location from the database by coordinates.

    :param x_coord: X coordinate of the location.
    :param y_coord: Y coordinate of the location.
    :return: Location object if the location exists, None otherwise.
    """
    return Location.objects.filter(x_coord=x_coord, y_coord=y_coord).first()

# ADDERS
def add_location(city, street, postal_code, number, x_coord, y_coord):
    """
    Function to add a location to the database.

    :param city: City object.
    :param street: Street of the location.
    :param postal_code: Postal code of the location.
    :param number: Number of the location.
    :param x_coord: X coordinate of the location.
    :param y_coord: Y coordinate of the location.
    """
    return Location.objects.create(city=city, street=street, postal_code=postal_code, number=number, x_coord=x_coord, y_coord=y_coord)
    
# DELETERS
def delete_location(location):
    """
    Function to delete a location from the database.

    :param location: Location object.
    """
    location.delete()
    
class SupportedProduct(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=255)
    specifications = models.CharField(max_length=1000)
    brand = models.CharField(max_length=45)
    type = models.CharField(max_length=45)
    pictures = models.ManyToManyField(Picture)

# GETTERS
def get_all_supported_products():
    """
    Function to get all supported products from the database.

    :return: QuerySet of SupportedProduct objects.
    """
    return SupportedProduct.objects.all()

def get_supported_product_by_id(id):
    """
    Function to get a supported product from the database by ID.

    :param id: ID of the supported product.
    :return: SupportedProduct object if the product exists, None otherwise.
    """
    return SupportedProduct.objects.filter(id=id).first()

def get_supported_product_by_name(name):
    """
    Function to get a supported product from the database by name.

    :param name: Name of the product.
    :return: SupportedProduct object if the product exists, None otherwise.
    """
    return SupportedProduct.objects.filter(name=name).first()

def get_supported_product_pictures(supported_product):
    """
    Function to get all pictures of a supported product.

    :param supported_product: SupportedProduct object.
    :return: QuerySet of Picture objects.
    """
    return supported_product.pictures.all()

# MODIFIERS
def change_supported_product_name(supported_product, name):
    """
    Function to change the name of a supported product.

    :param supported_product: SupportedProduct object.
    :param name: New name of the supported product.
    """
    supported_product.name = name
    supported_product.save()
    
def change_supported_product_description(supported_product, description):
    """
    Function to change the description of a supported product.

    :param supported_product: SupportedProduct object.
    :param description: New description of the supported product.
    """
    supported_product.description = description
    supported_product.save()
    
def change_supported_product_specifications(supported_product, specifications):
    """
    Function to change the specifications of a supported product.

    :param supported_product: SupportedProduct object.
    :param specifications: New specifications of the supported product.
    """
    supported_product.specifications = specifications
    supported_product.save()
    
def change_supported_product_type(supported_product, type):
    """
    Function to change the type of a supported product.

    :param supported_product: SupportedProduct object.
    :param type: New type of the supported product.
    """
    supported_product.type = type
    supported_product.save()

# ADDERS
def add_picture_to_supported_product(supported_product, picture):
    """
    Function to add a picture to a supported product.

    :param supported_product: SupportedProduct object.
    :param picture: Picture object.
    """
    name = default_storage.save(picture.name, picture)
        
    # Create a new Picture object and save it to the database
    new_picture = Picture.objects.create(picture=name)
    
    # Add the ID of the new Picture object to the pictures field
    supported_product.pictures.add(new_picture.id)
    
def add_supported_product_pictures(supported_product, pictures):
    """
    Function to add pictures to a supported product.

    :param supported_product: SupportedProduct object.
    :param pictures: List of Picture objects.
    """
    for picture in pictures:
        # Save the picture file to the default storage
        name = default_storage.save(picture.name, picture)
        
        # Create a new Picture object and save it to the database
        new_picture = Picture.objects.create(picture=name)
        
        # Add the ID of the new Picture object to the pictures field
        supported_product.pictures.add(new_picture.id)

def add_supported_product(name, description, specifications, type, brand):
    """
    Function to add a supported product to the database.

    :param name: Name of the product.
    :param description: Description of the product.
    :param specifications: Specifications of the product.
    :param type: Type of the product.
    """
    return SupportedProduct.objects.create(name=name, description=description, specifications=specifications, type=type, brand=brand) 

# DELETERS
def remove_picture_from_supported_product(supported_product, picture):
    """
    Function to remove a picture from a supported product.

    :param supported_product: SupportedProduct object.
    :param picture: Picture object.
    """
    supported_product.pictures.remove(picture)
  
def delete_supported_product(supported_product):
    """
    Function to delete a supported product from the database.

    :param supported_product: SupportedProduct object.
    """
    supported_product.delete()
    
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, password = password, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_reseller(self, email, username, password, **extra_fields):
        user = self.create_user(email, username, password, **extra_fields)
        return user

    def create_admin(self, email, username, password, **extra_fields):
        user = self.create_user(email, username, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    forename = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=40)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    location = models.ForeignKey(Location, on_delete=models.RESTRICT, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'forename', 'surname', 'phone']
    
class Reseller(User):
    pib = models.IntegerField()
    

class Customer(User):
    pass

class Admin(User):
    pass

class BlockedUser(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name='blocking_admin')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='blocked_user')

# GETTERS
def get_all_customers():
    return Customer.objects.all()
def get_all_resellers():
    return Reseller.objects.all()
def get_user_location(user):
    """
    Function to get the location of a user.

    :param user: User object.
    :return: Location object if the user has a location, None otherwise.
    """
    return user.location

def get_user_by_username(username):
    """
    Function to get a user from the database by username.

    :param username: Username of the user.
    :return: User object if the user exists, None otherwise.
    """
    user = User.objects.filter(username=username).first()
    if is_admin(user):
        return Admin.objects.filter(username=username).first()
    if is_reseller(user):
        return Reseller.objects.filter(username=username).first()
    if is_customer(user):
        return Customer.objects.filter(username=username).first()
    return None


def get_user_by_email(email):
    """
    Function to get a user from the database by email.

    :param email: Email of the user.
    :return: User object if the user exists, None otherwise.
    """
    user = User.objects.filter(email=email).first()
    if is_admin(user):
        return Admin.objects.filter(email=email).first()
    if is_reseller(user):
        return Reseller.objects.filter(email=email).first()
    if is_customer(user):
        return Customer.objects.filter(email=email).first()

def get_user_by_id(id):
    """
    Function to get a user from the database by ID.

    :param id: ID of the user.
    :return: User object if the user exists, None otherwise.
    """
    user = User.objects.filter(id=id).first()
    if is_admin(user):
        return Admin.objects.filter(id=id).first()
    if is_reseller(user):
        return Reseller.objects.filter(id=id).first()
    if is_customer(user):
        return Customer.objects.filter(id=id).first()    

# ADDERS
def add_customer(username, password, email, forename, surname, phone):
    """
    Function to add a customer to the database.

    :param username: Username of the customer.
    :param password: Password of the customer.
    :param email: Email of the customer.
    :param forename: Forename of the customer.
    :param surname: Surname of the customer.
    :param phone: Phone number of the customer.
    """
    customer = Customer.objects.create_user(username=username, password=password, email=email, forename=forename, surname=surname, phone=phone)
    return customer

def add_reseller(username, password, email, forename, surname, phone, pib):
    """
    Function to add a reseller to the database.

    :param username: Username of the reseller.
    :param password: Password of the reseller.
    :param email: Email of the reseller.
    :param forename: Forename of the reseller.
    :param surname: Surname of the reseller.
    :param phone: Phone number of the reseller.
    :param pib: PIB of the reseller.
    """
    reseller = Reseller.objects.create_reseller(username=username, password=password, email=email, forename=forename, surname=surname, phone=phone, pib=pib)
    return reseller

def add_admin(username, password, email, forename, surname, phone):
    """
    Function to add an admin user to the database.

    :param username: Username of the admin user.
    :param password: Password of the admin user.
    :param email: Email of the admin user.
    :param forename: Forename of the admin user.
    :param surname: Surname of the admin user.
    :param phone: Phone number of the admin user.
    """
    admin = Admin.objects.create_admin(username=username, password=password, email=email, forename=forename, surname=surname, phone=phone)
    return admin

# MODIFIERS
def block_user(admin, user):
    """
    Function to block a user.

    :param admin: Admin user who is blocking the user.
    :param user: User to be blocked.
    """
    BlockedUser.objects.create(admin=admin, user=user)

def unblock_user(admin, user):
    """
    Function to unblock a user.

    :param admin: Admin user who is unblocking the user.
    :param user: User to be unblocked.
    """
    BlockedUser.objects.filter(admin=admin, user=user).delete()
    
def change_user_location(user, location):
    """
    Function to change the location of a user.

    :param user: User object.
    :param location: Location object.
    """
    user.location = location
    user.save()
    
def change_user_username(user, new_username):
    """
    Function to change a user's username.

    :param user: User object.
    :param new_username: String of new username.
    :return: True if the username was changed successfully, False otherwise.
    """
    if User.objects.filter(username=new_username).exists():
        return False

    user.username = new_username
    user.save()
    return True

# CHECKERS
def is_admin(user):
    """
    Function to check if a user is an admin.

    :param user: User object.
    :return: True if the user is an admin, False otherwise.
    """
    username = user.username
    return Admin.objects.filter(username=username).exists()

def is_blocked(user):
    """
    Function to check if a user is blocked.

    :param user: User object.
    :return: True if the user is blocked, False otherwise.
    """
    return BlockedUser.objects.filter(user=user).exists()

def is_customer(user):
    """
    Function to check if a user is a customer.

    :param user: User object.
    :return: True if the user is a customer, False otherwise.
    """
    username = user.username
    return Customer.objects.filter(username=username).exists()

def is_reseller(user):
    """
    Function to check if a user is a reseller.

    :param user: User object.
    :return: True if the user is a reseller, False otherwise.
    """
    username = user.username
    return Reseller.objects.filter(username=username).exists()

def user_exists(username, email, phone):
    """
    Function to check if a user exists in the database.

    :param username: Username of the user.
    :param email: Email of the user.
    :param phone: Phone number of the user.
    :return: True if the user exists, False otherwise.
    """
    return User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists() or User.objects.filter(phone=phone).exists()

# DELETERS
def delete_user(user):
    """
    Function to delete a user from the database.

    :param user: User object.
    """
    user.delete()
    
class Product(models.Model):
    supported_product = models.ForeignKey(SupportedProduct, on_delete=models.CASCADE)
    price = models.IntegerField()
    seller = models.ForeignKey('Reseller', on_delete=models.CASCADE)
    class Meta:
        unique_together = (('supported_product', 'seller'),)

# GETTERS
def get_all_products():
    """
    Function to get all products from the database.

    :return: QuerySet of Product objects.
    """
    return Product.objects.all()

def get_product_by_id(id):
    """
    Function to get a product from the database by ID.

    :param id: ID of the product.
    :return: Product object if the product exists, None otherwise.
    """
    return Product.objects.filter(id=id).first()

def get_lowest_price_product(supported_product):
    """
    Function to get the product with the lowest price.
    
    :param supported_product: Supported product object.
    :return: Product object with the lowest price.
    """
    return Product.objects.filter(supported_product=supported_product).order_by('price').first()

def get_products_by_seller(seller, sort_by = None):
    """
    Function to get all products of a specified seller.

    :param seller: Seller object.
    :param sort_by: Optional parameter to sort the products by price or rating.
    :return: QuerySet of Product objects.
    """
    products = Product.objects.filter(seller=seller)
    if sort_by == 'price_asc':
        return products.order_by('price')
    if sort_by == 'price_desc':
        return products.order_by('-price')
    if sort_by == 'rating_asc':
        return products.order_by('rating')
    if sort_by == 'rating_desc':
        return products.order_by('-rating')
    return products

def get_products_by_supported_product(supported_product, sort_by = None):
    """
    Function to get all products of a specified supported product.

    :param supported_product: Supported product object.
    :param sort_by: Optional parameter to sort the products by price or rating.
    :return: QuerySet of Product objects.
    """
    products = Product.objects.filter(supported_product=supported_product)
    if sort_by == 'price_asc':
        return products.order_by('price').all()
    if sort_by == 'price_desc':
        return products.order_by('-price').all()
    if sort_by == 'rating_asc':
        return products.order_by('rating').all()
    if sort_by == 'rating_desc':
        return products.order_by('-rating').all()
    return products.all()


def get_product_by_supported_product_and_seller(supported_product, seller):
    """
    Function to get a product by supported product and seller.

    :param supported_product: Supported product object.
    :param seller: Seller object.
    :return: Product object if the product exists, None otherwise.
    """
    return Product.objects.filter(supported_product=supported_product, seller=seller).first()

# ADDERS
def add_product(supported_product, price, seller):
    """
    Function to add a product to the database.

    :param supported_product: Supported product for the product.
    :param price: Price of the product.
    :param seller: Reseller who is selling the product.
    """
    return Product.objects.create(supported_product=supported_product, price=price, seller=seller)

# DELETERS
def delete_product(product):
    """
    Function to delete a product from the database.

    :param product: Product object.
    """
    product.delete()
    
# MODIFIERS
def change_product_price(product, price):
    """
    Function to change the price of a product.

    :param product: Product object.
    :param price: New price of the product.
    """
    product.price = price
    product.save()

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    rating = models.IntegerField()
    class Meta:
        unique_together = (('customer', 'product'),)
    
# GETTERS
def get_rating_by_product_and_customer(product, customer):
    """
    Function to get a rating by product and customer.

    :param product: Product object.
    :param customer: Customer object.
    :return: Rating object if the rating exists, None otherwise.
    """
    return Rating.objects.filter(product=product, customer=customer).first()

def get_ratings_by_product(product):
    """
    Function to get all ratings of a specified product.

    :param product: Product object.
    :return: QuerySet of Rating objects.
    """
    return Rating.objects.filter(product=product)

def get_ratings_by_customer(customer):
    """
    Function to get all ratings of a specified customer.

    :param customer: Customer object.
    :return: QuerySet of Rating objects.
    """
    return Rating.objects.filter(customer=customer)

def get_average_rating(product):
    """
    Function to get the average rating of a product.

    :param product: Product object.
    :return: Average rating of the product.
    """
    ratings = Rating.objects.filter(product=product)
    if ratings.count() == 0:
        return 0
    return sum([rating.rating for rating in ratings]) / ratings.count()

# MODIFIERS
def change_rating(rating, new_rating):
    """
    Function to change a rating.

    :param rating: Rating object.
    :param new_rating: New rating.
    """
    rating.rating = new_rating
    rating.save()
    
# ADDERS
def add_rating(product, customer, rating):
    """
    Function to add a rating to the database.

    :param product: Product object.
    :param customer: Customer object.
    :param rating: Rating of the product.
    """
    Rating.objects.create(product=product, customer=customer, rating=rating)
    
# DELETERS
def delete_rating(rating):
    """
    Function to delete a rating from the database.

    :param rating: Rating object.
    """
    rating.delete()
    
class Cart(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    class Meta:
        unique_together = (('customer', 'product'),)
        
# GETTERS
def get_cart_by_customer(customer):
    """
    Function to get the cart of a specified customer.

    :param customer: Customer object.
    :return: QuerySet of Cart objects.
    """
    return Cart.objects.filter(customer=customer).all()

def get_quantity_by_customer(customer):
    """
    Function to get the quantity of products in the cart of a specified customer.

    :param customer: Customer object.
    :return: Total quantity of products in the cart.
    """
    return sum([cart.quantity for cart in Cart.objects.filter(customer=customer)])

# ADDERS
def add_to_cart(customer, product):
    """
    Function to add a product to the cart.

    :param customer: Customer object.
    :param product: Product object.
    :param quantity: Quantity of the product.
    """
    if(Cart.objects.filter(customer=customer, product=product).exists()):
        cart = Cart.objects.get(customer=customer, product=product)
        cart.quantity += 1
        cart.save()
    else:
        Cart.objects.create(customer=customer, product=product, quantity=1)
    
# MODIFIERS
def remove_from_cart(customer, product):
    """
    Function to remove a product from the cart.

    :param customer: Customer object.
    :param product: Product object.
    """
    if Cart.objects.filter(customer=customer, product=product).exists():
        cart = Cart.objects.get(customer=customer, product=product)
        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()
        else:
            cart.delete()
    
def empty_cart(customer):
    """
    Function to empty the cart of a specified customer.

    :param customer: Customer object.
    """
    Cart.objects.filter(customer=customer).delete()
    
def change_cart_quantity(customer, product, quantity):
    """
    Function to change the quantity of a product in the cart.

    :param customer: Customer object.
    :param product: Product object.
    :param quantity: New quantity of the product.
    """
    cart = Cart.objects.get(customer=customer, product=product)
    cart.quantity = quantity
    cart.save()
    
# DELETERS
def delete_cart(cart):
    """
    Function to delete a cart from the database.

    :param cart: Cart object.
    """
    cart.delete()

class RemovedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
# GETTERS
def get_removed_products():
    """
    Function to get all removed products from the database.

    :return: QuerySet of RemovedProduct objects.
    """
    return RemovedProduct.objects.all()

def get_removed_product_by_product(product):
    """
    Function to get a removed product by product.

    :param product: Product object.
    :return: RemovedProduct object if the product is removed, None otherwise.
    """
    return RemovedProduct.objects.filter(product=product).first()

def get_removed_products_by_seller(seller):
    """
    Function to get all removed products of a specified seller.

    :param seller: Seller object.
    :return: QuerySet of RemovedProduct objects.
    """
    return RemovedProduct.objects.filter(product__seller=seller)

def get_removed_products_by_supported_product(supported_product):
    """
    Function to get all removed products of a specified supported product.

    :param supported_product: SupportedProduct object.
    :return: QuerySet of RemovedProduct objects.
    """
    return RemovedProduct.objects.filter(product__supported_product=supported_product)

# MODIFIERS
def remove_product(product):
    """
    Function to remove a product from the database.

    :param product: Product object.
    """
    RemovedProduct.objects.create(product=product)

def unremove_product(product):
    """
    Function to unremove a product.

    :param product: Product object.
    """
    RemovedProduct.objects.filter(product=product).delete()
    
class TransactionProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    class Meta:
        unique_together = (('product', 'transaction'),)

class Transaction(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    seller = models.ForeignKey('Reseller', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='TransactionProduct')
    location = models.ForeignKey(Location, on_delete=models.RESTRICT, null=True)
    transaction_type = models.CharField(max_length=45)
    total_price = models.IntegerField()
    
# GETTERS

def get_all_TransactionProduct():
    return TransactionProduct.objects.all()
def get_transactions_by_customer(customer):
    """
    Function to get all transactions of a specified customer.

    :param customer: Customer object.
    :return: QuerySet of Transaction objects.
    """
    return Transaction.objects.filter(customer=customer)

def get_products_quantity_by_transaction(transaction):
    """
    Function to get all products and their quantities of a specified transaction.

    :param transaction: Transaction object.
    :return: QuerySet of TransactionProduct objects.
    """
    return TransactionProduct.objects.filter(transaction=transaction)

# ADDERS
def add_transaction(customer, seller, products, location, transaction_type, quantities):
    """
    Function to add a transaction to the database.

    :param customer: Customer object.
    :param products: List of Product objects.
    """
    # calculate the total price of the transaction
    total_price = 0
    for i in range(len(products)):
        total_price += products[i].price * quantities[i]
    transaction = Transaction.objects.create(customer=customer, seller=seller, location=location, transaction_type=transaction_type, total_price=total_price)
    for i in range(len(products)):
        
        TransactionProduct.objects.create(product=products[i], transaction=transaction, quantity=quantities[i])
