//author: Luka Kaludjerovic 0041-2021
document.addEventListener('DOMContentLoaded', function(){
    fetch('api/products/view/all')
    .then(response => response.json())
    .then(data => {
        populateHTML(data);
    })
    .catch(error => {
        console.error('Error: ', error);
    });
})

function populateHTML(data){
    let table = document.getElementById('products-table');
    table.innerHTML = '';

    data.products.forEach(product => {
        let name = `${product.name}`;
        let photo_location = `${product.photo_location}`;
        let price_from = `${product.price_from}`;

        let div = document.createElement('div');
        div.className = 'phonecell';
        div.setAttribute('price', `${product.price_from}`);
        div.setAttribute('brand', `${product.brand}`);
        div.setAttribute('name', `${product.name}`);
        div.innerHTML += '<img src="' + photo_location + '" alt="' + name + '" width="50%">';
        div.innerHTML += '<br>';
        div.innerHTML += '<h6>' + name + '</h6>';
        div.innerHTML += '<br>';
        div.innerHTML += '<h6>Starting at: ' + price_from + '&euro;</h6>';
        div.addEventListener('click', function(){
            sessionStorage.setItem("product", name);
            sessionStorage.setItem("photo", photo_location);
            fetchProductDetails(product.id);
        });
        table.appendChild(div);
    });
}

function fetchProductDetails(productId) {
    fetch(`api/products/view/${productId}`)
        .then(response => response.json())
        .then(data => {
            localStorage.setItem("productId", productId);
            localStorage.setItem("productDetails", JSON.stringify(data));
            window.location.href = 'product';
        })
        .catch(error => {
            console.error('Error fetching product details: ', error);
        });
}