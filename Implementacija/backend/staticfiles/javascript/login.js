//author: Luka Kaludjerovic 0041-2021
function login(){
    event.preventDefault();
    let username = document.getElementsByName("username")[0].value;
    let password = document.getElementsByName("password")[0].value;

    fetch('api/auth/login', {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json',
        }, 
        body: JSON.stringify({
            "username": username, 
            "password": password, 
        })
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        if(data.error){
            alert("Wrong username or password!");
            document.getElementsByName("username")[0].value = '';
            document.getElementsByName("password")[0].value = '';
        }
        else{
            sessionStorage.setItem('user', data.user_type);
            sessionStorage.setItem('username', username);
            window.location.href = 'home';
        }
    })
    .catch(error => {
        console.error('Error: ', error);
    })
}

function register(){
    let radios = document.getElementsByName('role');
    if(radios[0].checked)
        window.location.href = 'new-customer';
    else
        window.location.href = 'new-reseller';
}

function new_customer(){
    event.preventDefault();
    let forename = document.getElementsByName("forename")[0].value;
    let surname = document.getElementsByName("surname")[0].value;
    let email = document.getElementsByName("email")[0].value;
    let username = document.getElementsByName("username")[0].value;
    let phonenumber = document.getElementsByName("phonenumber")[0].value;
    let password1 = document.getElementsByName("password1")[0];
    let password2 = document.getElementsByName("password2")[0];

    if (password1.value != password2.value) {
        alert("Passwords do not match!");
        password2.value = "";
    }
    else {
        fetch('api/auth/register/customer', {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json',
            }, 
            body: JSON.stringify({
                "username": username, 
                "password": password1.value, 
                "email": email, 
                "forename": forename, 
                "surname": surname, 
                "phone": phonenumber, 
                "repeat_password": password2.value,
            })
        })
        .then(response => {
            if(!response.ok){
                throw new Error('Error with registering a new customer!');
            }
            return response.json();
        })
        .then(data => {
            alert("Account successfully created! Welcome!");
            sessionStorage.setItem('user', 'customer');
            sessionStorage.setItem('username', username);
            window.location.href = 'home';
        })
        .catch(error => {
            console.error('Error: ', error);
        })
    }
}

function new_reseller(){
    console.log("new reseller");
    event.preventDefault();

    let company_name = document.getElementsByName("company_name")[0].value;
    let pib = document.getElementsByName("pib")[0].value;
    let email = document.getElementsByName("email")[0].value;
    let username = document.getElementsByName("username")[0].value;
    let phonenumber = document.getElementsByName("phonenumber")[0].value;
    let password1 = document.getElementsByName("password1")[0];
    let password2 = document.getElementsByName("password2")[0];

    let city = document.getElementsByName("city")[0].value;
    let street = document.getElementsByName("street")[0].value;
    let number = document.getElementsByName("number")[0].value;
    let postal_code = document.getElementsByName("postal_code")[0].value;

    if (password1.value != password2.value) {
        alert("Passwords do not match!");
        password2.value = "";
    } else {
        navigator.geolocation.getCurrentPosition(function(position) {
            let x = position.coords.latitude;
            let y = position.coords.longitude;

            fetch('api/auth/register/reseller', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    "company_name": company_name,
                    "pib": pib,
                    "password": password1.value,
                    "email": email,
                    "phone": phonenumber,
                    "username": username,
                    "repeat_password": password2.value,
                    "city": city,
                    "street": street,
                    "number": number,
                    "postal_code": postal_code,
                    "x": x,
                    "y": y
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error with registering a new reseller!');
                }
                return response.json();
            })
            .then(data => {
                alert("Account successfully created! Welcome!");
                sessionStorage.setItem('user', 'reseller');
                sessionStorage.setItem('username', username);
                window.location.href = 'home';
            })
            .catch(error => {
                console.error('Error: ', error);
            });
        }, function(error) {
            console.error('Error getting location: ', error);
            alert('Unable to retrieve your location. Please try again.');
        });
    }
}
