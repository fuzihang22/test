let listing_count = 1;

function addProduct() {
    listing_count++;

    let itemContainer = document.createElement("div");
    itemContainer.setAttribute("class", "item-container");

    // CSRF token generation for each product
    let csrf_token_value = document.getElementById("csrf_token").value;
    let crsf_tag = document.createElement("input");
    crsf_tag.setAttribute("id", "product_list-" + listing_count + "-csrf_token");
    crsf_tag.setAttribute("name", "product_list-" + listing_count + "-csrf_token");
    crsf_tag.setAttribute("type", "hidden");
    crsf_tag.setAttribute("value", csrf_token_value);
    itemContainer.appendChild(crsf_tag);

    // Header for item
    let header = document.createElement("h3");
    header.innerHTML = "Item " + listing_count + ":";
    itemContainer.appendChild(header);

    // Constructing quantity form
    let q_label = document.createElement("label");
    q_label.setAttribute("for", "product_list-" + listing_count + "-quantity");
    q_label.innerHTML = "Quantity";
    let q_input = document.createElement("input");
    q_input.setAttribute("id", "product_list-" + listing_count + "-quantity");
    q_input.setAttribute("name", "product_list-" + listing_count + "-quantity");
    q_input.setAttribute("required", "");
    q_input.setAttribute("size", "16");
    q_input.setAttribute("step", "any");
    q_input.setAttribute("type", "number");
    q_input.setAttribute("value", "");
    let q_container = document.createElement("p");
    q_container.appendChild(q_label);
    q_container.appendChild(document.createElement("br"));
    q_container.appendChild(q_input);
    itemContainer.appendChild(q_container);

    // Constructing description form
    let d_label = document.createElement("label");
    d_label.setAttribute("for", "product_list-" + listing_count + "-description");
    d_label.innerHTML = "Description";
    let d_input = document.createElement("input");
    d_input.setAttribute("id", "product_list-" + listing_count + "-description");
    d_input.setAttribute("name", "product_list-" + listing_count + "-description");
    d_input.setAttribute("required", "");
    d_input.setAttribute("size", "16");
    d_input.setAttribute("type", "text");
    d_input.setAttribute("value", "");
    let d_container = document.createElement("p");
    d_container.appendChild(d_label);
    d_container.appendChild(document.createElement("br"));
    d_container.appendChild(d_input);
    itemContainer.appendChild(d_container);

    // Constructing category form
    let c_label = document.createElement("label");
    c_label.setAttribute("for", "product_list-" + listing_count + "-category");
    c_label.innerHTML = "Category";
    let c_input = document.createElement("select");
    c_input.setAttribute("id", "product_list-" + listing_count + "-category");
    c_input.setAttribute("name", "product_list-" + listing_count + "-category");
    c_input.setAttribute("required", "");
    c_input.setAttribute("size", "16");

    let optionValues = ["Bread", "Fruit", "Vegetables", "Dairy", "Other"];

    for (let i = 0; i < optionValues.length; i++) {
        let optionElement = document.createElement("option");
        optionElement.value = optionValues[i];
        optionElement.textContent = optionValues[i];
        c_input.appendChild(optionElement);
    }

    let c_container = document.createElement("p");
    c_container.appendChild(c_label);
    c_container.appendChild(document.createElement("br"));
    c_container.appendChild(c_input);
    itemContainer.appendChild(c_container);

    // Constructing delete button
    let deleteButton = document.createElement("button");
    deleteButton.innerHTML = "Delete";
    deleteButton.setAttribute("type", "button");
    deleteButton.style.backgroundColor = "red"; // Set the background color to red
    deleteButton.style.color = "white";    
    deleteButton.addEventListener("click", function () {
        itemContainer.remove();
        listing_count--;
         
    });
    itemContainer.appendChild(deleteButton);

    document.getElementById("additionalItems").appendChild(itemContainer);
    
}
