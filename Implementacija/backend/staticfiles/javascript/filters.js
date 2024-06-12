//author: Luka Kaludjerovic 0041-2021
//author: Andrija Gajic 0033-2021
function search() {
    // Prevent the form from submitting normally
    event.preventDefault();

    // Get the search query
    var query = document.querySelector('.textbox').value.toLowerCase();

    // Get all the phones
    let phones = document.getElementsByClassName("phonecell");

    // Loop through all the phones
    for(let i = 0; i < phones.length; i++){
        // Get the name of the phone
        let name = phones[i].getAttribute("name").toLowerCase();

        // If the name of the phone does not include the search query, hide the phone
        if(!name.includes(query)){
            phones[i].style.display = "none";
        }
        // Otherwise, show the phone
        else{
            phones[i].style.display = "inline-flex";
        }
    }
}

function addManufacturers(manufacturers){
    let filters = document.getElementsByClassName("filters")[0];

    if(manufacturers.length > 0){
        let title = document.createElement("b");
        title.innerText = "Manufacturer:";
        filters.appendChild(title);
    }

    manufacturers.forEach(manufacturer => {
        let input = document.createElement("input");
        input.type = "checkbox";
        input.name = "brand";
        input.id = manufacturer.toLowerCase();
        let label = document.createElement("label");
        label.setAttribute("for", manufacturer.toLowerCase());
        label.innerText = manufacturer;
        filters.appendChild(document.createElement("br"));
        filters.appendChild(input);
        filters.appendChild(label);
    });

    filters.appendChild(document.createElement("hr"));
}

function addGlider(){
    let filters = document.getElementsByClassName("filters")[0];

    let title = document.createElement("b");
    title.innerText = "Max price:";
    filters.appendChild(title);
    filters.appendChild(document.createElement("br"));

    let div = document.createElement("div");
    div.innerHTML += "30&euro;";
    let input = document.createElement("input");
    input.type = "range";
    input.name = "price";
    input.id = "price";
    input.min = "30";
    input.max = "1500";
    input.value = "700";
    input.step = "10";
    div.appendChild(input);
    div.innerHTML += "1500&euro;";
    div.appendChild(document.createElement("br"));
    let p = document.createElement("p");
    p.id = "gliderValue";
    p.innerHTML = "700&euro;";
    div.appendChild(p);
    filters.appendChild(div);
    filters.appendChild(document.createElement("hr"));

    let glider = document.getElementById("price");
    let gliderValueDisplay = document.getElementById("gliderValue");
    glider.addEventListener("input", function() {
        gliderValueDisplay.textContent = glider.value + "€";
    });
}

function resetCheckboxesAndGlider(){
    let phones = document.getElementsByClassName("phonecell");
    for(let i = 0; i < phones.length; i++){
        phones[i].style.display = "inline-flex";
    }
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    var glider = document.getElementById("price");
    var gliderValueDisplay = document.getElementById("gliderValue");
    checkboxes.forEach(function(checkbox) {
        checkbox.checked = false;
    });
    glider.value = 700;
    gliderValueDisplay.textContent = glider.value + "€";

    document.querySelector('.textbox').value = '';
}

function filter(){
    let phones = document.getElementsByClassName("phonecell");

    let gliderValue = parseInt(document.getElementById("price").value);
    let brands = document.getElementsByName("brand");
    let brandsList = [];
    for(let i = 0; i < brands.length; i++){
        if(brands[i].checked)
            brandsList.push(brands[i].id);
    }
    for(let i = 0; i < phones.length; i++){
        let price = parseInt(phones[i].getAttribute("price"));
        let brand = phones[i].getAttribute("brand");
        if(price > gliderValue){
            phones[i].style.display = "none";
        }
        else if(brandsList.length > 0){
            for (let j = 0; j < brandsList.length; j++){
                //compare the brand of the phone with the brands that are checked, lower case insensitive
                if(brand.toLowerCase() != brandsList[j].toLowerCase()){
                    phones[i].style.display = "none";
                }
                else{
                    phones[i].style.display = "inline-flex";
                    break;
                }
            }
        }
        else{
            phones[i].style.display = "inline-flex";
        }
    }
}

function addFilters(){
    addManufacturers(['Alcatel', 'Apple', 'Honor', 'Huawei', 'Motorola', 'Samsung', 'Xiaomi']);
    addGlider();
    let filters = document.getElementsByClassName("filters")[0];
    let input = document.createElement("input");
    input.type = "reset";
    input.id = "resetButton";
    input.value = "Reset all filters";
    input.addEventListener("click", resetCheckboxesAndGlider);
    filters.appendChild(input);
    input = document.createElement("input");
    input.type = "submit";
    input.id = "submitButton";
    input.value = "Apply filters";
    input.addEventListener("click", filter);
    filters.appendChild(input);
}

document.addEventListener('DOMContentLoaded', function(){
    addFilters();
})