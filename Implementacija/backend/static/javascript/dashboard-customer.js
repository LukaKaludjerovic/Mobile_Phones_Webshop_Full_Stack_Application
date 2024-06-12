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
    let username = sessionStorage.getItem('username');
    fetch('api/user/transactions/view', {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json',
        }, 
        body: JSON.stringify({
            username: username
        })
    })
    .then(response => {
        if(!response.ok){
            throw new Error('Error with retrieving transactions for user!');
        }
        return response.json();
    })
    .then(data => {
        populateTransactions(data);
    })
    .catch(error => {
        console.error('Error: ', error);
    })
})

function populateTransactions(data){
    document.getElementById('total-number').innerText = data.transactions_count;
    document.getElementById('total-value').innerText = data.amount;

    let div = document.getElementById('your-orders');
    data.transactions.forEach(transaction => {
        div.innerHTML += `Reseller: ${transaction.reseller}`;
        div.innerHTML += '<br>';
        div.innerHTML += `Type: ${transaction.type}`;
        div.innerHTML += '<br>';
        div.innerHTML += `Price: ${transaction.total_price}`;
        div.innerHTML += '<hr>';
    })
}