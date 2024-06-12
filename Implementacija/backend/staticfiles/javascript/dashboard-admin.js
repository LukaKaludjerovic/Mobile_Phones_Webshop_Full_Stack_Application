//author: Luka Kaludjerovic 0041-2021
function change_password(){
    event.preventDefault();
    let password = document.getElementsByName("password")[0].value;
    let password1 = document.getElementsByName("password1")[0].value;
    let password2 = document.getElementsByName("password2")[0].value;

    if(password == password1){
        alert('Old and new password cannot be same!');
        return;
    }
    
    if(password1 != password2){
        alert('Passwords do not match!');
        return;
    }

    fetch('api/user/changepassword', {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json',
        }, 
        body: JSON.stringify({
            "username": sessionStorage.getItem('username'),
            "old_password": password, 
            "new_password": password1,
        })
    })
    .then(response => {
        if(!response.ok){
            throw new Error('Error with changing password!');
        }
        return response.json();
    })
    .then(data => {
        alert("Password successfully changed!");
        location.reload();
    })
    .catch(error => {
        alert('Old password is incorrect!');
        console.error('Error: ', error);
    })
}

document.addEventListener('DOMContentLoaded', function(){
    fetch('api/customers/view')
    .then(response => response.json())
    .then(data => {
        populateCustomers(data);
    })
    .catch(error => {
        console.error('Error: ', error);
    });
})

function populateCustomers(data){
    let div = document.getElementById('customer');
    let number = document.getElementById('number-of-customers');

    number.innerHTML = data.customer_count;
    data.customers.forEach(customer => {
        div.innerHTML += 'Username: ' + customer.username + '<br>';
        div.innerHTML += 'Name: ' + customer.ime + ' ' + customer.prezime + '<br>'; 
        if(customer.lokacija != ''){
            div.innerHTML += 'Location: ' + customer.lokacija + '<br>';
        }
        div.innerHTML += `<input type="button" value="Delete customer" onclick="deleteCustomer('${customer.username}')">`;
        div.innerHTML += '<hr>';
    });
}

function deleteCustomer(username){
    let choice = confirm('Are you sure you want to delete customer: ' + username + '?');
    if(choice == false){
        return;
    }
    
    const url = 'api/delete/customer';
    fetch(url, {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json',
        }, 
        body: JSON.stringify({
            'username': username
        })
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        if(data.error){
            alert('An error occured. Customer is not deleted!');
            return;
        }
        else{
            location.reload();
        }
    })
    .catch(error => {
        console.log('Error: ', error);
    })
}

document.addEventListener('DOMContentLoaded', function(){
    fetch('api/resellers/view')
    .then(response => response.json())
    .then(data => {
        populateResellers(data);
    })
    .catch(error => {
        console.error('Error: ', error);
    });
})

function populateResellers(data){
    let div = document.getElementById('reseller');
    let number = document.getElementById('number-of-resellers');

    number.innerHTML = data.reseller_count;
    data.resellers.forEach(reseller => {
        div.innerHTML += 'Username: ' + reseller.username + '<br>';
        div.innerHTML += 'Name: ' + reseller.ime + ' ' + reseller.prezime + '<br>'; 
        if(reseller.lokacija != ''){
            div.innerHTML += 'Location: ' + reseller.lokacija + '<br>';
        }
        div.innerHTML += `<input type="button" value="Delete reseller" onclick="deleteReseller('${reseller.username}')">`;
        div.innerHTML += '<hr>';
    });
}

function deleteReseller(username){
    let choice = confirm('Are you sure you want to delete reseller: ' + username + '?');
    if(choice == false){
        return;
    }
    
    const url = 'api/delete/reseller';
    fetch(url, {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json',
        }, 
        body: JSON.stringify({
            'username': username
        })
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        if(data.error){
            alert('An error occured. Reseller is not deleted!');
            return;
        }
        else{
            location.reload();
        }
    })
    .catch(error => {
        console.log('Error: ', error);
    })
}

document.addEventListener('DOMContentLoaded', function(){
    fetch('api/transactions/view')
    .then(response => response.json())
    .then(data => {
        populateTransactions(data);
    })
    .catch(error => {
        console.error('Error: ', error);
    });
})

function populateTransactions(data){
    let div = document.getElementById('transactions');
    let number = document.getElementById('number-of-transactions');

    number.innerHTML = data.transactions_count;
    data.transactions.forEach(transaction => {
        div.innerHTML += 'Customer: ' + transaction.customer + '<br>';
        div.innerHTML += 'Reseller: ' + transaction.reseller + '<br>'; 
        div.innerHTML += 'Type: ' + transaction.type + '<br>'; 
        div.innerHTML += 'Total price: ' + transaction.total_price + '<br>'; 
        div.innerHTML += '<hr>';
    });
}