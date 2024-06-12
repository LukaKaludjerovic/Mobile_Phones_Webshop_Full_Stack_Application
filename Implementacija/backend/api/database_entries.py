import requests
import os
url = "http://127.0.0.1:8000/api/products/insert/supported"
def add_product(name, description, specification, type, brand, pictures):
    # Prepare the data
    data = {
        "name": name,
        "description": description,
        "specification": specification,
        "type": type,
        "brand": brand,
    }
    # Prepare the files
    files = [("pictures", (open(picture, "rb"))) for picture in pictures]

    # Make the request
    response = requests.post(url, data=data, files=files)

    # Print the response
    if response.text:
        print(response.json())
    else:
        print("Empty response received")

# Call the function
add_product(
    "iPhone 15",
    "Newest iPhone model from Apple.",
    "6.7-inch OLED display, 120Hz refresh rate, A16 Bionic chip, 5G support, 512GB storage, 12MP camera.",
    "Smartphone",
    "Apple",
    ["C:\\faks\PSI\Projekat\project_FUM\Implementacija\\backend\static\imgs\iphone15.png"]  # Replace with your actual file paths
)


# make entry for iphone 14 plus
add_product(
    "iPhone 14 Plus",
    "Newest iPhone model from Apple.",
    "6.7-inch OLED display, 120Hz refresh rate, A16 Bionic chip, 5G support, 512GB storage, 12MP camera.",
    "Smartphone",
    "Apple",
    ["C:\\faks\PSI\Projekat\project_FUM\Implementacija\\backend\static\imgs\iphone14plus.png"]  # Replace with your actual file paths
)

# make entry for samsung galaxy s22
add_product(
    "Samsung Galaxy S22",
    "Newest Samsung Galaxy model.",
    "6.7-inch OLED display, 120Hz refresh rate, Exynos 2200 chip, 5G support, 512GB storage, 12MP camera.",
    "Smartphone",
    "Samsung",
    ["C:\\faks\PSI\Projekat\project_FUM\Implementacija\\backend\static\imgs\samsungs22.png"]  # Replace with your actual file paths
)
# make entry for samsung galaxy s22 ultra
add_product(
    "Samsung Galaxy S22 Ultra",
    "Newest Samsung Galaxy model.",
    "6.7-inch OLED display, 120Hz refresh rate, Exynos 2200 chip, 5G support, 512GB storage, 108MP camera.",
    "Smartphone",
    "Samsung",
    ["C:\\faks\PSI\Projekat\project_FUM\Implementacija\\backend\static\imgs\samsungs22ultra.png"]  # Replace with your actual file paths
)
# make entry for samsung galaxy s23
add_product(
    "Samsung Galaxy S23",
    "Newest Samsung Galaxy model.",
    "6.7-inch OLED display, 120Hz refresh rate, Exynos 2200 chip, 5G support, 512GB storage, 12MP camera.",
    "Smartphone",
    "Samsung",
    ["C:\\faks\PSI\Projekat\project_FUM\Implementacija\\backend\static\imgs\samsungs23.png"]  # Replace with your actual file paths
)
# make entry for samsung galaxy s23 ultra
add_product(
    "Samsung Galaxy S23 Plus",
    "Newest Samsung Galaxy model.",
    "6.7-inch OLED display, 120Hz refresh rate, Exynos 2200 chip, 5G support, 512GB storage, 108MP camera.",
    "Smartphone",
    "Samsung",
    ["C:\\faks\PSI\Projekat\project_FUM\Implementacija\\backend\static\imgs\samsungs23plus.png"]  # Replace with your actual file paths
)
# make entry for samsung galaxy xiaomi 13 pro
add_product(
    "Xiaomi 13 Pro",
    "Newest Xiaomi model.",
    "6.7-inch OLED display, 120Hz refresh rate, Snapdragon 888 chip, 5G support, 512GB storage, 12MP camera.",
    "Smartphone",
    "Xiaomi",
    ["C:\\faks\PSI\Projekat\project_FUM\Implementacija\\backend\static\imgs\\xiaomi13pro.png"]  # Replace with your actual file paths
)
# make entry for iphone 14 plus
add_product(
    "iPhone 14 Plus",
    "Newest iPhone model from Apple.",
    "6.7-inch OLED display, 120Hz refresh rate, A16 Bionic chip, 5G support, 512GB storage, 12MP camera.",
    "Smartphone",
    "Apple",
    ["C:\\faks\PSI\Projekat\project_FUM\Implementacija\\backend\static\imgs\iphone14plus.png"]  # Replace with your actual file paths
)

# make entry for iphone 14 pro max
add_product(
    "iPhone 14 Pro Max",
    "Newest iPhone model from Apple.",
    "6.7-inch OLED display, 120Hz refresh rate, A16 Bionic chip, 5G support, 512GB storage, 12MP camera.",
    "Smartphone",
    "Apple",
    ["C:\\faks\PSI\Projekat\project_FUM\Implementacija\\backend\static\imgs\iphone14promax.png"]  # Replace with your actual file paths
)

# make entry for iphone 15 pro
add_product(
    "iPhone 15 Pro",
    "Newest iPhone model from Apple.",
    "6.7-inch OLED display, 120Hz refresh rate, A16 Bionic chip, 5G support, 512GB storage, 12MP camera.",
    "Smartphone",
    "Apple",
    ["C:\\faks\PSI\Projekat\project_FUM\Implementacija\\backend\static\imgs\iphone15pro.png"]  # Replace with your actual file paths
)

# make entry for iphone 15 pro max
add_product(
    "iPhone 15 Pro Max",
    "Newest iPhone model from Apple.",
    "6.7-inch OLED display, 120Hz refresh rate, A16 Bionic chip, 5G support, 512GB storage, 12MP camera.",
    "Smartphone",
    "Apple",
    ["C:\\faks\PSI\Projekat\project_FUM\Implementacija\\backend\static\imgs\iphone15promax.png"]  # Replace with your actual file paths
)

# make entry for iphone 15 plus
add_product(
    "iPhone 15 Plus",
    "Newest iPhone model from Apple.",
    "7.0-inch OLED display, 120Hz refresh rate, A16 Bionic chip, 5G support, 512GB storage, 12MP camera.",
    "Smartphone",
    "Apple",
    ["C:\\faks\PSI\Projekat\project_FUM\Implementacija\\backend\static\imgs\iphone15plus.png"]  # Replace with your actual file paths
)