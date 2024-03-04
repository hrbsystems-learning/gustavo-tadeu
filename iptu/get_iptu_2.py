# This program is not finished yet.
# Things that must be done:
#  1. Improvements in function my_ocr_using_easyocr. It demonstrate be better than my_ocr_using_pytesseract.
#     But needs work to be fine. OCR erros occurs when letter v follows w and vice versa.
#     Other option is coding another OCR functions, using others python OCR libs. 
#  2. Function is_not_debitAutomatic must be coded yet.
#  3. Funcrion generate_IPTU_second_via must be coded yet.    
# IMPORTANT: It is necessary to use the pillow version 9.5.0, because some dependencies on second and higher levels
#            are incompatable with pillow versions higher than 9.5.0
# to install or replace the current version of pillow library in your Python Virtual Environment
# use the command below:
#   conda install pillow=9.5.0  

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
import easyocr
import os

# list of input data to be processed
input_data =[
{ 'numero_contribuinte' : '019.061.0453-0', 'parcela': 1, 'ano_exercicio': 2024},
{ 'numero_contribuinte' : '012.168.0212-2', 'parcela': 1, 'ano_exercicio': 2024},
{ 'numero_contribuinte' : '012.168.0212-2', 'parcela': 1, 'ano_exercicio': 2024},
{ 'numero_contribuinte' : '012.168.0212-2', 'parcela': 1, 'ano_exercicio': 2024},
{ 'numero_contribuinte' : '012.168.0212-2', 'parcela': 1, 'ano_exercicio': 2024},
]


# Define functions

#  this function was repslced by extract_mage1. It should be deleted in near future
# def extract_image(response):
# 
#     soup = BeautifulSoup(response.content, "html.parser")
#     # Find the first img tag that has a src attribute starting with "data:image/png;base64,"
#     img_tag = soup.find("img", src=lambda x: x and x.startswith("data:image/png;base64,"))
#     # If the img tag is found, extract the base64 data
#     if img_tag:
#         base64_data = img_tag["src"].split(",")[1]
#         # Decode the base64 data and convert it to bytes
#         img_data = base64.b64decode(base64_data)
#         # Create a PIL image object from the bytes
#         img = Image.open(io.BytesIO(img_data))
#         # Save the image to a file with a unique name
#         img.save(f"image_{img_tag['alt']}.png")
#         # Return the PIL image object
#         return img
#     # If the img tag is not found, return None
#     else:
#         return None


def extract_image1(response):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    # Find the first img tag that has a src attribute starting with "data:image/png;base64,"
    img_tag = soup.find("img", src=lambda x: x and x.startswith("data:image/png;base64,"))
    # If the img tag is found, extract the base64 data
    if img_tag:
        base64_data = img_tag["src"].split(",")[1]
        # Decode the base64 data and convert it to bytes
        img_data = base64.b64decode(base64_data)
        # Create a BytesIO object from the bytes
        img_bytes = io.BytesIO(img_data)
        # Reopen the BytesIO object as a PIL image
        img = Image.open(img_bytes)
        # Return the PIL image in png format
        return img
    # If the img tag is not found, return None
    else:
        return None


# from now on, this function isn't necessary. It Should be deleted in ner future
# def decode_and_ocr(image_string):
#     image_bytes = base64.b64decode(image_string)
#     image = Image.open(image_bytes)
#     image.save("image.png")
#     print("Image saved as image.png")
#     text = pytesseract.image_to_string(image)
#     print("Text extracted from the image:")
#     print(text)
#     return text
    

def my_base64decode(img_base64_encoded):
    image_bytes = base64.b64decode(img_base64_encoded, validate=True)
    return image_bytes


def my_ocr_using_pytesseract(image):
    text = pytesseract.image_to_string(image)
    return text    


def my_ocr_using_easyocr(abs_image_file_path):
    # Create an EasyOCR reader object with English language
    reader = easyocr.Reader(['en'])
    # Read the text from the image using the reader object
    result = reader.readtext(abs_image_file_path, allowlist='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', detail=0)
    # Join the list of recognized texts into a single string
    text = ''.join(result)
    # Return the text
    return text


def save_image(image):
    # image = Image.open(image)
    image.save("image.png")
    return os.path.abspath("image.png")
    

def image_bytes_to_image(image_bytes):
    return Image.open(image_bytes)

def is_base64_image_prefix_present(s) -> bool:
    return s[:21] == "data:image/jpeg;base64"

def generateCaptchaImage(session : requests.session):
    url = "https://iptu.prefeitura.sp.gov.br/Api/EmitirBoleto/GerarCaptcha"
    params = {"_": 1708869910143}
    response = session.get(url, params=params)
    image = extract_image1(response)
    return image

def is_not_debitAutomatic(session, numero_contribuinte, parcela_a_pagar, ano_exercicio, captcha_text):
    pass

def generate_IPTU_second_via(session,numero_contribuinte, parcela_a_pagar, ano_execicio, captcha_text):
    pass

def process_input_data(input_data_list : list) -> None:

    session = requests.session()
    session.get("https://iptu.prefeitura.sp.gov.br")

    current_numero_contribuinte = '019.061.0453-0' # initial value - empty string
    current_parcela = 1 # default value 1
    current_ano_exercicio = 2024 # defailt value 2024

    for current_Data_map in input_data_list:

        # initialize all current parameter values from input data list
        for key, value in current_Data_map.items():
            if key == 'numero_contribuinte':
                current_numero_contribuinte = value
            if key == 'parcela':
                current_parcela = value
            if key == 'ano_exercicio':
                current_ano_exercicio = value
        
        # calculate the text of the current captcha image 
        current_captcha_image = generateCaptchaImage(session)
        abs_image_file_path = save_image(current_captcha_image)
        current_captcha_text = my_ocr_using_easyocr(abs_image_file_path)

        if is_not_debitAutomatic(
                session,
                numero_contribuinte = current_numero_contribuinte, # The identification number of the property or land
                parcela_a_pagar= current_parcela,
                ano_execicio= current_ano_exercicio,
                captcha_text= current_captcha_text):
                
                second_via_iptu = generate_IPTU_second_via(
                    session,
                    numero_contribuinte = current_numero_contribuinte, # The identification number of the property or land
                    parcela_a_pagar = current_parcela,
                    ano_execicio= current_ano_exercicio,
                    captcha_text= current_captcha_text
                    )

                print(second_via_iptu)


# Begin Program

process_input_data(input_data_list=input_data)




