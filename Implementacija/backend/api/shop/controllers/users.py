"""
author: Luka Mladenovic 0108-2021
author: Andrija Gajic 0033-2021
"""
import json
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from api.models import get_all_customers, get_all_resellers, get_all_TransactionProduct, delete_user, \
    get_user_by_username, get_transactions_by_customer
    
from django.contrib.auth import authenticate, login, logout


def is_admin(func):
    """
    Decorator to restrict access to admin users only.

    :param func: Function to be decorated.
    :return: Wrapped function that checks if the user is an admin.
    """
    @wraps(func)
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin:
            return JsonResponse({"error": "Unauthorized access to admin resources"}, status=403)
        return func(request, *args, **kwargs)

    return wrapper


#@is_admin
def handle_get_customers():
    """
   Controller function to return the total count and details of all registered customers. Access is restricted to admin users.

   :return: JsonResponse: Contains 'customer_count' and a list of 'customers' with information such as username, ime,
    prezime, lokacija, transaction_count.
    """

    all_customers = get_all_customers()
    data={}
    data['customer_count']=len(all_customers)
    data['customers']=[]
    for customer in all_customers:
        data['customers'].append({
            "username":customer.username,
            "ime":customer.forename ,
            "prezime":customer.surname,
            "lokacija": customer.location.city.name if customer.location and customer.location.city else "",
        })

    return JsonResponse(data)


#@is_admin
def handle_get_resellers():
    """
    Controller function to return the total count and details of all registered resellers. Access is restricted to admin users.

    :return: JsonResponse: Contains 'reseller_count' and a list of 'resellers' with information such as username, ime,
    prezime, lokacija, transaction_count.
    """
    data = {
        "reseller_count": 1,
        "resellers": [
            {
                "username": "kaludjer123",
                "ime": "Luka",
                "prezime": "Kaludjerovic",
                "lokacija": "Beograd",
                "transactions_count": 110
            },
            {
                "username": "terza123",
                "ime": "Vukan",
                "prezime": "Terzic",
                "lokacija": "Beograd",
                "transaction_count": 1000
            }

        ]

    }
    all_customers = get_all_resellers()
    data = {}
    data['reseller_count'] = len(all_customers)
    data['resellers'] = []
    for customer in all_customers:
        data['resellers'].append({
            "username": customer.username,
            "ime": customer.forename,
            "prezime": customer.surname,
            "lokacija": customer.location.city.name if customer.location and customer.location.city else "",
        })

    return JsonResponse(data)

def handle_delete_customer(request):
    data = json.loads(request.body)
    username = data['username']
    user = get_user_by_username(username)
    delete_user(user)
    return JsonResponse({"message": "Customer deleted! "})


def handle_delete_reseller(request):
    data = json.loads(request.body)
    username = data['username']
    user = get_user_by_username(username)
    delete_user(user)
    return JsonResponse({"message": "Reseller deleted! "})

@login_required(login_url='login')
def handle_change_password(request):
    user = request.user
    data = json.loads(request.body)
    try:
        old_password = data['old_password']
        new_password = data['new_password']
    except KeyError:
        return JsonResponse({"error": "Missing required fields"}, status=400)
    if not user.check_password(old_password):
        return JsonResponse({"error": "Old password is incorrect"}, status=400)
    user.set_password(new_password)
    user.save()
    request.user = user
    
    user = authenticate(username=user.username, password=new_password)
    if user is not None:
        login(request, user)
    return JsonResponse({"message": "Password changed successfully!"}, status=200)
        

def handle_get_transactions():


    all_get_all_TransactionProduct = get_all_TransactionProduct()

    data = {}
    data['transactions_count'] = len(all_get_all_TransactionProduct)
    data['transactions'] = []

    for transactionProductin in all_get_all_TransactionProduct:
        data['transactions'].append({
            "customer": transactionProductin.transaction.customer.forename+" "+transactionProductin.transaction.customer.surname,
            "reseller": transactionProductin.transaction.seller.forename,
            "type": transactionProductin.transaction.transaction_type,
            "total_price": transactionProductin.transaction.total_price

        })

    return JsonResponse(data)


@login_required(login_url='login')
def handle_view_user_transactions(request):

    data = json.loads(request.body)
    username = data.get('username')
    
    customer = get_user_by_username(username)
    
    all_transactions =  get_transactions_by_customer( customer)

    data = {}
    data['transactions_count'] = len(all_transactions)
    data['amount'] = 0
    data['transactions'] = []

    for tran in all_transactions:
        data['transactions'].append({
            "reseller": tran.seller.forename,
            "type": tran.transaction_type,
            "total_price": tran.total_price
        })
        data["amount"] += int(tran.total_price)
    return JsonResponse(data)

