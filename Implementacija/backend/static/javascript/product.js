//author: Luka Kaludjerovic 0041-2021
//aurhor: Andrija Gajic 0033/2021
const specs = {
    iphone15promax: {Display: 6.7, Weight: 221, Chip: "Apple A17 Pro"}, 
    iphone15pro: {Display: 6.1, Weight: 187, Chip: "Apple A17 Pro"},
    iphone15plus: {Display: 6.7, Weight: 221, Chip: "Apple A17 Pro"},
    iphone15: {Display: 6.1, Weight: 187, Chip: "Apple A17 Pro"},
    iphone14promax: {Display: 6.7, Weight: 240, Chip: "Apple A16 Bionic"}, 
    iphone14pro: {Display: 6.1, Weight: 206, Chip: "Apple A16 Bionic"},
    iphone14plus: {Display: 6.7, Weight: 221, Chip: "Apple A16 Bionic"},
    iphone14: {Display: 6.1, Weight: 187, Chip: "Apple A16 Bionic"},
    iphone13: {Display: 6.1, Weight: 187, Chip: "Apple A15 Pro"},
    samsungs23plus: {Display: 6.21, Weight: 195, Chip: "Qualcomm Snapdragon 8"},
    samsungs23: {Display: 5.76, Weight: 168, Chip: "Qualcomm Snapdragon 8"},
    samsungs22ultra: {Display: 6.43, Weight: 228, Chip: "Qualcomm Snapdragon 8"},
    samsungs22: {Display: 5.7, Weight: 167, Chip: "Qualcomm Snapdragon 8"},
    xiaomi13pro: {Display: 6.72, Weight: 218, Chip: "Qualcomm Snapdragon 8"}
}

document.addEventListener('DOMContentLoaded', function() {
    let productDetails = JSON.parse(localStorage.getItem('productDetails'));
    let productId = localStorage.getItem('productId');

    if (!productDetails) {
        console.error('No product details found in local storage.');
        return;
    }

    let product = productDetails.name;
    let photo = productDetails.photo_location;
    let offers = productDetails.offers;
    console.log(offers)

    document.getElementsByTagName('title')[0].innerText = product + " - 5G Shop";

    let img = document.createElement('img');
    img.src = photo;
    img.alt = product;
    img.style.width = "100%";
    document.getElementById("product-image").appendChild(img);

    document.getElementById("product-title").innerText = product;


    let photoKey = photo.split('/').pop().split(".")[0];

    console.log(photoKey);

    console.log(specs[photoKey])

    document.getElementById("display").innerText = specs[photoKey.toLowerCase()].Display || 'N/A';
    document.getElementById("weight").innerText = specs[photoKey.toLowerCase()].Weight || 'N/A';
    document.getElementById("chip").innerText = specs[photoKey.toLowerCase()].Chip || 'N/A';

    let sellersTable = document.getElementById("sellers-table");
    offers.forEach(offer => {
        let row = sellersTable.insertRow();
        let cellName = row.insertCell(0);
        let cellPrice = row.insertCell(1);
        let cellLocation = row.insertCell(2);
        let addToCart = row.insertCell(3);

        cellName.innerText = offer.name;
        cellPrice.innerText = offer.price + "€";
        cellLocation.innerText = offer.location;
        row.id = offer.name + "/" + offer.price;
        addToCart.innerHTML = `<button onclick="addtocartdb('${offer.id}', '${offer.name}', '${offer.price}', '${offer.location}')">Add to cart</button>`;
    });
     document.getElementById('get-recommendation').addEventListener('click', function() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                let x = position.coords.latitude;
                let y = position.coords.longitude;
                let supportedProduct = productId;

                get_recommendation(x, y, supportedProduct);
            }, function(error) {
                console.error('Error Code = ' + error.code + ' - ' + error.message);
            });
        } else {
            console.log('Geolocation is not supported by this browser.');
        }
    });
});

function get_recommendation(x, y, supportedProduct){
    fetch('api/products/view/reccomended', {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json',
        }, 
        body: JSON.stringify({
            "username": sessionStorage.getItem('username'),
            "x": x, 
            "y": y,
            "supportedProduct": supportedProduct,
        })
    })
    .then(response => {
        if(!response.ok){
            throw new Error('Error with getting recommendation!');
        }
        return response.json();
    })
    .then(data => {
        let offers = document.getElementsByTagName('tr');
        for(let i = 0; i < offers.length; i++){
            if(offers[i].id == `${data.name}/${data.price}`){
                offers[i].style.border = '2px solid red';
            }
        }
    })
    .catch(error => {
        alert("Recommendation could not be made!");
        console.error('Error: ', error);
    })
}

function addtocartdb(productId, name, price, location){
    // make a POST request to the backend to add the product to the cart
    // the request should include the product ID
    const url = '/api/products/add/cart';
    const data = {product_id: productId};


    fetch(url, {
        method: 'POST', // or 'PUT'
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
         window.location.reload(true);
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}


function addtocart(productId, name, price, location){
    sessionStorage.setItem("cart", parseInt(sessionStorage.getItem("cart")) + 1);
    document.getElementById("cart").innerText = sessionStorage.getItem("cart");
    sessionStorage.setItem("price", parseInt(sessionStorage.getItem("price")) + parseInt(price));

    if(sessionStorage.getItem("products")){
        cart = JSON.parse(sessionStorage.getItem("products"));
    }
    if(containsSimilar({productId: productId, name: name, price: price, location: location})){
        updateCart({productId: productId, name: name, price: price, location: location});
    }
    else{
        let photo = sessionStorage.getItem('photo');
        let product = sessionStorage.getItem('product');
        cart.push({productId: productId, product: product, name: name, price: price, location: location, quantity: "1", photo: photo});
    }
    
    sessionStorage.setItem("products", JSON.stringify(cart));
}

function containsSimilar(product){
    return cart.some(item => item.productId == product.productId && 
                             item.name == product.name && 
                             item.location == product.location);
}

function updateCart(product){
    for(let i = 0; i < cart.length; i++){
        let item = cart[i];
        if(item.productId == product.productId && 
           item.name == product.name && 
           item.location == product.location){
            let unit_price = parseInt(cart[i].price) / parseInt(cart[i].quantity);
            cart[i].price = parseInt(cart[i].price) + unit_price;
            cart[i].quantity = parseInt(cart[i].quantity) + 1;
        }
    }
}

/*
{
    "name":"iPhone 15 Pro",
    "type":"Smartphone",
    "description":"Newest iPhone model from Apple.",
    "photo_location":"/media/iphone15pro.png",
    "specification":"6.7-inch OLED display, 120Hz refresh rate, A16 Bionic chip, 5G support, 512GB storage, 12MP camera.",
    "offers":[
        {
            "name":"LukaGas",
            "price":1111,
            "location":"Belgrade"
        }
    ]
}




*/