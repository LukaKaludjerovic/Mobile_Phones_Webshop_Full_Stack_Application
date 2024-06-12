"""
    Author: Andrija Gajic 0033-2021
    Author: Luka Kaludjerovic 0041-2021
"""

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from api.models import user_exists, add_admin, add_customer, add_reseller, add_city, get_city_by_name \
    , add_location, get_user_by_username, change_user_location, is_admin, is_reseller, is_customer
import json
import requests

def get_geocode_data(address):
    API_KEY = 'AIzaSyC6UIQQMYhbFAAJoE1w1xn2zyMczruVGBg'  # Replace with your Google Maps API key
    BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        "address": address,
        "key": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()
    print(data)
    full_address = city = zip_code = lat = lon = street_number = None

    if data['status'] == 'OK':
        geometry = data['results'][0]['geometry']['location']
        lat, lon = geometry['lat'], geometry['lng']
        full_address = data['results'][0]['formatted_address']
        # Extract city, zip code from the 'address_components' field
        for component in data['results'][0]['address_components']:
            if 'locality' in component['types']:
                city = component['long_name']
            elif 'postal_code' in component['types']:
                zip_code = component['long_name']
            # get street number
            elif 'street_number' in component['types']:
                street_number = component['long_name']
        return full_address, city, zip_code, street_number, lat, lon
    else:
        return None

def handle_login(request):
    """
    Controller function to handle user login. 

    :return: JsonResponse: Contains 'message' if login is successful, or 'error' if login fails.
    """
    data = json.loads(request.body)
    
    username = data.get('username')
    password = data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        # add user to session
        login(request, user)
        user_type = 'none'
        #user_type = ...    TODO: URGENT, RETURNS TYPE OF USER FOR GIVEN USERNAME AND PASSWORD 'customer', 'reseller' or 'admin'
        return JsonResponse({"message": "Login successful", "user_type": user_type}, status=200)
    else:
        return JsonResponse({"error": "Invalid credentials"}, status=400)
        
        
        
def handle_logout(request):
    """
    Controller function to handle user logout. 

    :return: JsonResponse: Contains 'message' if logout is successful, or 'error' if logout fails.
    """
    
    try:
        # logout user from session
        # this needs to be implemented
        logout(request)
        return JsonResponse({"message": "Logout successful"}, status=200)
    except KeyError:
        return JsonResponse({"error": "User not logged in"}, status=400)
    
    
def handle_register_customer(request):
    """
    Controller function to handle customer registration.
    
    :return: JsonResponse: Contains 'message' if registration is successful, or 'error' if registration fails.
    """
    data = json.loads(request.body)
    print(data)
    # Get the data from the request
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    forename = data.get('forename')
    surname = data.get('surname')
    phone = data.get('phone')
    repeat_password = data.get('repeat_password')
    print(username, password, email, forename, surname, phone, repeat_password)
    if password != repeat_password:
        return JsonResponse({"error": "Passwords do not match"}, status=400)
    from django.contrib.auth.models import User
    print(user_exists(username=username, email=email, phone=phone))
    if user_exists(username=username, email=email, phone=phone) is not False:
        return JsonResponse({"error": "Username already exists"}, status=400)
    print("Adding customer")
    user = add_customer(username, password, email, forename, surname, phone)
    login(request, user)
    return JsonResponse({"message": "Registration successful"}, status=200)

def handle_register_reseller(request):
    """
    Controller function to handle reseller registration.
    
    :return: JsonResponse: Contains 'message' if registration is successful, or 'error' if registration fails.
    """
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    forename = data.get('company_name')
    surname = ''
    phone = data.get('phone')
    repeat_password = data.get('repeat_password')
    pib = data.get('pib')

    city, street, postal_code, number, x_coord, y_coord = data.get('city'), data.get('street'), data.get('postal_code'), data.get('number'),\
        data.get("x"), data.get("y")


    # make google maps api call to get address, city, zip code, lat, lon from address
    if password != repeat_password:
        return JsonResponse({"error": "Passwords do not match"}, status=401)
    if user_exists(username=username, email=email, phone=phone) is not False:
        return JsonResponse({"error": "Username already exists"}, status=402)

    print(city, street, postal_code, number, x_coord, y_coord)
    user = add_reseller(username, password, email, forename, surname, phone, pib)
    print(user)
    # make default address for reseller - hardcoded for now
    current_city=get_city_by_name(city)
    if not current_city:
        add_city(city)
    city = get_city_by_name(city)
    location = add_location(city, street, postal_code, number, x_coord, y_coord)
    user = get_user_by_username(username)
    change_user_location(user, location)
    login(request, user)
    return JsonResponse({"message": "Registration successful"}, status=200)
    
def handle_register_admin(request):
    """
    Controller function to handle admin registration.
    
    :return: JsonResponse: Contains 'message' if registration is successful, or 'error' if registration fails.
    """
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    forename = data.get('forename')
    surname = data.get('surname')
    phone = data.get('phone')
    repeat_password = data.get('repeat_password')
    if password != repeat_password:
        return JsonResponse({"error": "Passwords do not match"}, status=400)
    if user_exists(username=username, email=email, phone=phone):
        return JsonResponse({"error": "Username already exists"}, status=400)
    user = add_admin(username, password, email, forename, surname, phone)
    login(request, user)
    return JsonResponse({"message": "Registration successful"}, status=200)
    
    

def handle_get_role(request):
    data = json.loads(request.body)
    username = data.get('username')
    user=get_user_by_username(username)
    role=''
    if is_admin(user):
        role='admin'
    if is_reseller(user):
        role='reseller'
    if is_customer(user):
        role='customer'
    return JsonResponse({"role": role}, status=200)
