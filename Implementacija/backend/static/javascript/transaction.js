// author: Andrija Gajic 0033/2021

function createTransaction(){
    let address = sessionStorage.getItem("address");
    let postcode = sessionStorage.getItem("postcode");
    let city = sessionStorage.getItem("city");
    fetch('api/products/insert/transaction', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            address: address,
            zip: postcode,
            city: city,
            type: "card"
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
        window.location.href = 'order';
    });
}