// author: Luka Kaludjerovic 0041-2021
// author: Andrija Gajic 0033/2021
function createNavbar() {
    let navbar1 = document.getElementById("navbar1");
    let navbar2 = document.getElementById("navbar2");

    let li = document.createElement("li");
    li.className = "nav-item";
    let a = document.createElement("a");
    a.href = "home";
    a.className = "nav-link";
    if (document.title == "Home - 5G Shop") {
        a.className += " active";
    }
    a.innerText = "Home";
    li.appendChild(a);
    navbar1.appendChild(li);

    li = document.createElement("li");
    li.className = "nav-item";
    a = document.createElement("a");
    a.href = "about";
    a.className = "nav-link";
    if (document.title == "About us - 5G Shop") {
        a.className += " active";
    }
    a.innerText = "About us";
    li.appendChild(a);
    navbar1.appendChild(li);

    li = document.createElement("li");
    li.className = "nav-item";
    a = document.createElement("a");
    a.href = "shop";
    a.className = "nav-link";
    if (document.title == "Shop - 5G Shop" ||
        document.title == "Product - 5G Shop") {
        a.className += " active";
    }
    a.innerText = "Shop";
    li.appendChild(a);
    navbar1.appendChild(li);

    li = document.createElement("li");
    li.className = "nav-item";
    a = document.createElement("a");
    a.href = "contact";
    a.className = "nav-link";
    if (document.title == "Contact - 5G Shop") {
        a.className += " active";
    }
    a.innerText = "Contact";
    li.appendChild(a);
    navbar1.appendChild(li);

    li = document.createElement("li");
    li.className = "nav-item";
    a = document.createElement("a");
    a.className = "nav-link";
    if (document.title == "Login - 5G Shop" ||
        document.title == "New customer - 5G Shop" ||
        document.title == "New reseller - 5G Shop") {
        a.className += " active";
    }
    if (sessionStorage.getItem("user") == null) {
        a.href = "login";
        a.innerText = "Login";
    } else {
        if (sessionStorage.getItem("user") == "customer") {
            document.getElementById("header-left").className = "col-sm-9";
            document.getElementById("header-right").className = "col-sm-3";
            let innerli = document.createElement("li");
            innerli.className = "nav-item";
            let innera = document.createElement("a");
            innera.href = "cart";
            innera.className = "nav-link";
            if (document.title == "Cart - 5G Shop" ||
                document.title == "Delivery - 5G Shop" ||
                document.title == "Payment - 5G Shop" ||
                document.title == "Order - 5G Shop") {
                innera.className += " active";
            }
            innera.innerText = "Cart ";
            let span = document.createElement("span");
            span.id = "cart";
            span.className = "badge bg-secondary";
            // make fetch call to get all products in cart api/products/view/cart
            fetch('api/products/view/cart')
                .then(response => {
                    return response.json();
                })
                .then(data => {
                    span.innerText = data.products.length;
                    sessionStorage.setItem("cart", data.products.length);
                    span.innerText = data.products.length;
                })
                .catch(error => {
                    console.error('Error fetching cart:', error);
                });
            innera.appendChild(span);
            innerli.appendChild(innera);
            navbar2.appendChild(innerli);
        } else {
            document.getElementById("header-left").className = "col-sm-10";
            document.getElementById("header-right").className = "col-sm-2";
        }
        let innerli = document.createElement("li");
        innerli.className = "nav-item";
        let innera = document.createElement("a");
        if (sessionStorage.getItem("user") == "customer") {
            innera.href = "dashboard-customer";
        }
        if (sessionStorage.getItem("user") == "reseller") {
            innera.href = "dashboard-reseller";
        }
        if (sessionStorage.getItem("user") == "admin") {
            innera.href = "dashboard-admin";
        }
        innera.className = "nav-link";
        if (document.title == "Dashboard - 5G Shop") {
            innera.className += " active";
        }
        innera.innerText = "Dashboard";
        innerli.appendChild(innera);
        navbar2.appendChild(innerli);
        a.href = "home";
        a.innerText = "Logout";
        a.addEventListener("click", function () {
            logout();
        })
    }
    li.appendChild(a);
    navbar2.appendChild(li);
}

function logout() {
    let choice = confirm("Are you sure that you want to logout?");
    if (choice) {
        let username = sessionStorage.getItem('username');

        fetch('api/auth/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "username": username,
            })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error with logging out!');
                }
                return response.json();
            })
            .then()
            .catch(error => {
                console.error('Error: ', error);
            })
        sessionStorage.clear();
        window.location.href = 'home';
    }
}

function fetchUserRole() {
    let username = sessionStorage.getItem('username');
    fetch('/api/auth/role', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ "username": username })
    })
        .then(response => response.json())
        .then(data => {
            sessionStorage.setItem('user', data.role);
            createNavbar();
        })
        .catch(error => {
            console.error('Error fetching user role:', error);
        });
}

document.addEventListener('DOMContentLoaded', function () {
    if (sessionStorage.getItem("user") == "customer") {
        if(sessionStorage.getItem("cart") == null){
            sessionStorage.setItem("cart", "0");
            sessionStorage.setItem("price", "0");
        }
    }
    if (sessionStorage.getItem('username')) {
        fetchUserRole();
    } else {
        createNavbar();
    }
});
