//author: Luka Kaludjerovic 0041-2021
//author: Andrija Gajic 0033/2021
async function delivery(){
    event.preventDefault();
    let radios = document.getElementsByName('payment');
    let address = document.getElementsByName('address')[0].value;
    // postcode is integer
    let postcode = document.getElementsByName('postcode')[0].value;
    let city = document.getElementsByName('city')[0].value;
    // add to locatl storage
    sessionStorage.setItem("address", address);
    sessionStorage.setItem("postcode", postcode);
    sessionStorage.setItem("city", city);
    // try{
    //     const response = await fetch('products/insert/location', {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json',
    //         },
    //         body: JSON.stringify({
    //             address: address,
    //             zip: postcode,
    //             city: city
    //         })
    //     });
    //     // wait for fetch to finish
    //     const data = await response.json();
    // } catch (error) {
    //     console.error('Error:', error);
    // }


    if(radios[0].checked)
        window.location.href = 'payment';
    else{
        fetch('api/products/insert/transaction', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                address: address,
                zip: postcode,
                city: city,
                type: "delivery"
            })
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            window.location.href = 'order';
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
        
}

document.addEventListener('DOMContentLoaded', function(){
    document.getElementById("number-of-items").innerText = sessionStorage.getItem("cart");
    document.getElementById("total-price").innerText = sessionStorage.getItem("price");

    populateCart();
})
let cart;
function populateCart(){
    // make fetch call to get all products in cart products/view/cart

    fetch('api/products/view/cart')
    .then(response => {
        return response.json();
    })
    .then(data => {
        cart = data.products;
        let sum=0;
        let quantityItems=0;
        for(let i = 0; i < cart.length; i++){
            if(parseInt(cart[i].quantity) <= 0){
                continue;
            }
            let tr = document.createElement("tr");
            tr.id = i;
    
            let td = document.createElement("td");
            let img = document.createElement("img");
            img.src = cart[i].photo;
            img.width = 100;
            td.appendChild(img);
            tr.appendChild(td);
    
            td = document.createElement("td");
            td.innerHTML = cart[i].product;
            tr.appendChild(td);
    
            td = document.createElement("td");
            td.innerHTML = 'Reseller: ' + cart[i].name;
            tr.appendChild(td);
    
            td = document.createElement("td");
            td.innerHTML = 'Location: ' + cart[i].location;
            tr.appendChild(td);
    
            td = document.createElement("td");
            td.innerHTML = 'Quantity: ' + cart[i].quantity;
            quantityItems+=cart[i].quantity
            tr.appendChild(td);
    
            td = document.createElement("td");
            td.innerHTML = 'Total price: ' + cart[i].price * cart[i].quantity + "&euro;";
            sum+=cart[i].price * cart[i].quantity
            tr.appendChild(td);
    
            td = document.createElement("td");
            let minus = document.createElement("input");
            minus.type = "button";
            minus.value = "-";
            minus.addEventListener("click", function(){
                fetch('api/products/remove/cart', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        product_id: cart[i].id
                    })
                })
                .then(response => {
                    return response.json();
                })
                .then(data => {
                    console.log('Success:', data);
                    populateCart();
                    location.reload(true);
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
    
                populateCart();
                location.reload(true);
            })
            td.appendChild(minus);
            tr.appendChild(td);
    
            td = document.createElement("td");
            let plus = document.createElement("input");
            plus.type = "button";
            plus.value = "+";
            plus.addEventListener("click", function(){
                fetch('api/products/add/cart', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        product_id: cart[i].id
                    })
                })
                .then(response => {
                    return response.json();
                })
                .then(data => {
                    console.log('Success:', data);
                    populateCart();
                    location.reload(true);
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
    
                
            })
            td.appendChild(plus);
            tr.appendChild(td);
    
            table.appendChild(tr);
        }

    document.getElementById("number-of-items").innerText = quantityItems;
    document.getElementById("total-price").innerText = sum;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
    let table = document.getElementById("products-in-cart");

    
}