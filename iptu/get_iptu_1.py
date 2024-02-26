# Prompt: (chatGPT):
# As un expert in python language and main libraries in python, please:
# write a python script that accesses the URL https://iptu.prefeitura.sp.gov.br, capture from the HTTP response, all cookies values
# and the values of all form field present in the page. One of them is a png image. This image should be captured too.
# Answer:  
# I can try to write a python script that does what you asked, but I cannot guarantee its correctness or functionality. Please use it at your own risk and discretion. Here is the script:

# Import requests library to send HTTP requests
import requests
# Import BeautifulSoup library to parse the HTML content
from bs4 import BeautifulSoup
# Import io library to handle binary data
import io
# Import PIL library to handle images
from PIL import Image
# Import base64 library to decode the image string
import base64
# Import pytesseract library to perform OCR
import pytesseract


# Define the function that takes a base64 encoded image string as input
def decode_and_ocr(image_string):
    image_bytes = base64.b64decode(image_string)
    image = Image.open(image_bytes)
    image.save("image.png")
    print("Image saved as image.png")
    text = pytesseract.image_to_string(image)
    print("Text extracted from the image:")
    print(text)
    return text

def my_base64decode(img_base64_encoded):
    image_bytes = base64.b64decode(img_base64_encoded, validate=True)
    return image_bytes


def my_ocr(image):
    text = pytesseract.image_to_string(image)
    return text    


def save_image(image):
    image = Image.open(image)
    image.save("image.png")

def image_bytes_to_image(image_bytes):
    return Image.open(image_bytes)

def is_base64_image_prefix_present(s) -> bool:
    return s[:21] == "data:image/jpeg;base64"


# Begin Program

url = "https://iptu.prefeitura.sp.gov.br"

# response = requests.get(url)
# Create a session object to maintain cookies
session = requests.Session()
# Send a GET request to the URL and store the response object
response = session.get(url)

print(f"Status code: {response.status_code}")
print(f"Cookies: {response.cookies}")
print(f"HTML COntent: {response.content}")

# Parse the response content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

imgs = soup.find_all("img")

for img in imgs:
    # image_src_content = ({img['src']} )
    image_src_content = str(img.get('src'))
    if is_base64_image_prefix_present(image_src_content):
        image_bytes = my_base64decode(image_src_content + "==")        
        image = image_bytes_to_image(image_bytes)
        save_image(image)
        text = my_ocr(image)
        print(text)

    # image_response = requests.get(img['src'])
    # # Check if the response status code is 200 (OK)
    # if image_response.status_code == 200:
    #     # Open the image response content as a PIL image object
    #     image = Image.open(io.BytesIO(image_response.content))
    #     # Save the image object as a png file
    #     image.save("image.png")
    #     # Print a message indicating the image is saved
    #     print("Image saved as image.png")

