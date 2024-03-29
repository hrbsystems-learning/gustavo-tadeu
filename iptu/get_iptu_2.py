# This program is not finished yet.
# Things that must be done:
#  1. Improvements in function my_ocr_using_easyocr. It demonstrate be better than my_ocr_using_pytesseract.
#     But needs work to become fine. OCR erros occur when letter v follows w and vice versa.
#     Other option is coding another OCR functions, using others python OCR libs. 
#  2. Funcrion generate_IPTU_second_via must be coded yet.    
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
# Import PIL library to handle images (pillow lib version 9.5.0 must be used)
from PIL import Image
# Import base64 library to decode the image string
import base64
# Import pytesseract library to perform OCR
import pytesseract
import easyocr
import os
from google.cloud import vision
from google.oauth2 import service_account


# list of input data to be processed
input_data =[
{ 'numero_contribuinte' : '019.061.0453-0', 'parcela': 1, 'ano_exercicio': 2024, "debito_automatico" : False},
{ 'numero_contribuinte' : '012.168.0212-2', 'parcela': 1, 'ano_exercicio': 2024, "debito_automatico" : False},
{ 'numero_contribuinte' : '012.168.0212-2', 'parcela': 1, 'ano_exercicio': 2024, "debito_automatico" : False},
{ 'numero_contribuinte' : '012.168.0212-2', 'parcela': 1, 'ano_exercicio': 2024, "debito_automatico" : False},
{ 'numero_contribuinte' : '012.168.0212-2', 'parcela': 1, 'ano_exercicio': 2024, "debito_automatico" : False},
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


def my_ocr_using_google_ai_vision_api( image_file_path : str) -> str:

    # Path to service account key
    SERVICE_ACCOUNT_FILE = '/home/helio/_work/_credentials/GCP/service-account-file-healthface-5324f-bf0a920dee18.json' 

    # Authenticate with service account
    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    # Initialize cloud vision client
    client = vision.ImageAnnotatorClient(credentials=credentials)

    # Read image contents
    with io.open(image_file_path, 'rb') as image_file:
        content = image_file.read()

    # Send image to cloud vision API
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    detected_text = ''
    # Print detected text
    for page in response.full_text_annotation.pages:
        print(page.property.detected_languages)
        print('\n'.join(page.blocks))
        detected_text = page.blocks

    return detected_text


def my_ocr_png_layers(image_path):
    # Attempt to open the image file
    try:
        image = Image.open(image_path)
    except IOError:
        return "Error: The image file could not be opened."

    # List to hold the text of each layer
    text_layers = []

    # Check if the image has layers
    if image.is_animated:
        # Process each frame (layer) of the image
        for frame in range(0, image.n_frames):
            image.seek(frame)
            text = pytesseract.image_to_string(image)
            text_layers.append(text)
    else:
        # If the image is not animated, process it as a single layer
        text = pytesseract.image_to_string(image)
        text_layers.append(text)

    return text_layers


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


def generate_IPTU_second_via(session,numero_contribuinte, parcela_a_pagar, ano_execicio, captcha_text):
    url = 'https://iptu.prefeitura.sp.gov.br' 
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        '__RequestVerificationToken': 'QXsEellKT4jFYNA8-3NinXRLMcoNKnpn7rMsSUEMN7mRyeB7pSgeiXgr0rSGmkoquyvxIw-21aMt8cSP7__CFujaRv01MXZxGbowQR5CAEM1',
        'NumeroContribuinte': numero_contribuinte,
        'Parcela': str(parcela_a_pagar),
        'Exercicio': str(ano_execicio),
        'numeroNotificacaoLancamento': '',
        'ValorDigitado': captcha_text,
    }
    response = session.post(url, data=data, headers=headers)
    return response
    
def process_input_data(input_data_list : list) -> None:

    session = requests.session()
    session.get("https://iptu.prefeitura.sp.gov.br")

    current_numero_contribuinte = '019.061.0453-0' # initial value - empty string
    current_parcela = 1 # default value 1
    current_ano_exercicio = 2024 # defailt value 2024
    current_debito_automatico = True # default value True

    for current_Data_map in input_data_list:

        # initialize all current parameter values from input data list
        for key, value in current_Data_map.items():
            if key == 'numero_contribuinte':
                current_numero_contribuinte = value
            if key == 'parcela':
                current_parcela = value
            if key == 'ano_exercicio':
                current_ano_exercicio = value
            if key == 'debito_automatico':
                current_debito_automatico = value   
        
        # calculate the text of the current captcha image 
        current_captcha_image = generateCaptchaImage(session)
        abs_image_file_path = save_image(current_captcha_image)
        current_captcha_text = my_ocr_using_google_ai_vision_api(abs_image_file_path)

        if not current_debito_automatico:                  
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




