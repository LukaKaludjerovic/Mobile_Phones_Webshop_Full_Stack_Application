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

function add_phone(){
    event.preventDefault();
    let type = document.getElementsByName('type')[0].value;
    let storage = document.getElementsByName('storage')[0].value;
    let color = document.getElementsByName('color')[0].value;
    let price = document.getElementsByName('price')[0].value;
    let username = sessionStorage.getItem('username');

    fetch('api/products/insert/manual', {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json',
        }, 
        body: JSON.stringify({
            "type": type, 
            "storage": storage, 
            "color": color, 
            "price": price,
            "username": username
        })
    })
    .then(response => {
        if(!response.ok){
            throw new Error('Error with manual product adding!');
        }
        return response.json();
    })
    .then(data => {
        alert("Product successfully added! Thank you!");
        window.location.href = 'dashboard-reseller';
    })
    .catch(error => {
        console.error('Error: ', error);
    })
}
function upload() {
    document.getElementById('fileInput').click();
}

function file_name() {
    let fileInput = document.getElementById('fileInput');
    let fileName = fileInput.value.split('\\').pop();
    document.getElementById('file-name').innerText = 'Selected file: ' + fileName;
}

function add_phones() {
    let fileInput = document.getElementById('fileInput');
    let file = fileInput.files[0];

    let username = localStorage.getItem('username');
    console.log(username);
    if (file) {
        let formData = new FormData();
        formData.append('file', file);
        formData.append('username', username);

        fetch('/api/products/insert/serialized', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error with serial product adding!');
            }
            return response.json();
        })
        .then(data => {
            alert("Product successfully added! Thank you!");
            location.reload();
        })
        .catch(error => {
            console.error('Error: ', error);
        });
    } else {
        alert('File is not uploaded!');
    }
}


document.addEventListener('DOMContentLoaded', function(){
    let username = sessionStorage.getItem('username');
    fetch('api/products/products/seller?username='+username)
    .then(response => response.json())
    .then(data => {
        populatePhones(data);
    })
    .catch(error => {
        console.error('Error: ', error);
    });
})

function populatePhones(data){
    let div = document.getElementById('smartphones');
    let value = document.getElementById('total-value');
    let total_price = 0;
    div.innerHTML = '';

    data.products.forEach(product => {
        let name = product.name;
        let price = product.price_from;
        total_price += parseInt(price);

        div.innerHTML += '<p>Product: ' + name + '</p>';
        div.innerHTML += '<p>Price: ' + price + '&euro;</p>';
        div.innerHTML += '<hr>';
    })
    value.innerText = total_price;
    value.innerHTML += '&euro;';
}