document.addEventListener('DOMContentLoaded', function(){
    fetch('http://127.0.0.1:8000/api/products/view/all')
    .then(response => response.json())
    .then(data => {
        populateHTML(data);
    })
    .catch(error => {
        console.error('Error: ', error);
    });
})

function populateHTML(data){
    let container = document.getElementById('products');
    container.innerHTML = '';

    data.products.forEach(product => {
        let div = document.createElement('div');
        div.innerHTML = `
            <h2>${product.name}</h2>
            <img src="${product.photo_location}" alt="${product.name}">
            <p>Price: $${product.price_from}</p>
        `;
        container.appendChild(div);
    })
}