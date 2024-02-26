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

# input data
input_data =[
{ 'numero_contribuinte' : '012.168.0212-2', 'parcela': 1, 'ano_exercicio': 2024},
{ 'numero_contribuinte' : '012.168.0212-2', 'parcela': 1, 'ano_exercicio': 2024},
{ 'numero_contribuinte' : '012.168.0212-2', 'parcela': 1, 'ano_exercicio': 2024},
{ 'numero_contribuinte' : '012.168.0212-2', 'parcela': 1, 'ano_exercicio': 2024},
{ 'numero_contribuinte' : '012.168.0212-2', 'parcela': 1, 'ano_exercicio': 2024},
]

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

def generateCaptchaImage(session : requests.session):
    url = "https://iptu.prefeitura.sp.gov.br/Api/EmitirBoleto/GerarCaptcha"
    params = {"_": 1708869910143}
    response = session.get(url, params=params)
    return str(response.content)

def is_not_debitAutomatic(session, numero_contribuinte, parcela_a_pagar, ano_exercicio, captcha_text):
    pass

def generate_IPTU_second_via(session,numero_contribuinte, parcela_a_pagar, ano_execicio, captcha_text):
    pass

def process_input_data(input_data_list : list) -> None:

    session = requests.session()
    session.get("https://iptu.prefeitura.sp.gov.br")

    current_numero_contribuinte = '' # initial value - empty string
    current_parcela = 1 # default value 1
    current_ano_exercicio = 2024 # defailt value 2024

    for current_Data_map in input_data_list:

        # initialize all current parameter values from input data list
        for key, value in current_Data_map.items():
            if key == 'numero_contribuinte':
                current_umero_contribuinte = value
            if key == 'parcela':
                current_parcela = value
            if key == 'ano_exercicio':
                current_ano_exercicio = value
        
        # calculate the text of the current captcha image 
        current_captcha_base64_encoded_image = generateCaptchaImage(session)
        current_captcha_image_bytes =  my_base64decode(current_captcha_base64_encoded_image)
        current_captcha_image = image_bytes_to_image(current_captcha_image_bytes)
        current_captcha_text = my_ocr(current_captcha_image)
            
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

# url = "https://iptu.prefeitura.sp.gov.br"

process_input_data(input_data_list=input_data)




