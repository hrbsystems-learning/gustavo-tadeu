# I sent this prompt nessage to the chatGPT:
# Please,
#  Write a script in python that can be used to emit automatically the second via of the land tax (IPTU SP),
#  given the Número do Contribuinte, Parcela a ser paga, Ano de exercício (4 digits) and código da imagem (captcha). 

# I receibe the following answer:
# Hello, this is Copilot. 
# I can try to write a script in python that can be used to emit automatically the second via of the land tax (IPTU SP),  
#  but I cannot guarantee its correctness or functionality.  
#  Please use it at your own risk and discretion. Here is the script:


# Import requests library to send HTTP requests
import requests
# Import BeautifulSoup library to parse the HTML content
from bs4 import BeautifulSoup
# Import pytesseract library to perform OCR on captcha images
import pytesseract

# Define the URL of the IPTU SP website
url = "https://www.prefeitura.sp.gov.br/cidade/secretarias/fazenda/servicos/iptu/index.php?p=2452"
url = "https://iptu.prefeitura.sp.gov.br"

# Define the parameters for the second via emission
numero_contribuinte = "001.003.0001.1" # The identification number of the property or land
parcela_paga = "1" # The installment number to be paid
ano_exercicio = "2024" # The year of the tax exercise (4 digits)

# Create a session object to maintain cookies
session = requests.Session()

# Send a GET request to the URL and store the response object
response = session.get(url)

# Check if the response status code is 200 (OK)
if response.status_code == 200:
    # Parse the response content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the form element in the HTML
    # form = soup.find("form", id="frmEmissao2Via")

    # Find the input elements in the form
    inputs = soup.find_all("input")

    # Create a dictionary to store the form data
    form_data = {}

    # Loop through each input element
    for input in inputs:
        # Get the input name and value attributes
        name = input.get("name")
        value = input.get("value")
        # Add the name and value pair to the form data dictionary
        form_data[name] = value

        # Update the form data dictionary with the parameters for the second via emission
        form_data["txtNumContrib"] = numero_contribuinte
        form_data["txtExercicio"] = ano_exercicio
        form_data["txtNumPrest"] = parcela_paga

        # Find the image element that contains the captcha
        image = soup.find("img", id="imgCaptcha")

        # Get the image source attribute
        image_src = image.get("src")

        # Construct the full image URL by joining the base URL and the image source
        image_url = urljoin(url, image_src)

        # Send a GET request to the image URL and store the response object
        image_response = session.get(image_url)

        # Check if the image response status code is 200 (OK)
        if image_response.status_code == 200:
            # Apply OCR to the image response content and store the result as a string
            captcha = pytesseract.image_to_string(image_response.content)

            # Add the captcha string to the form data dictionary
            form_data["txtConfirma"] = captcha

            # Send a POST request to the URL with the form data and store the response object
            post_response = session.post(url, data=form_data)

            # Check if the post response status code is 200 (OK)
            if post_response.status_code == 200:
                # Print the post response content
                print(post_response.content)
            else:
                # Print an error message
                print(f"POST request failed with status code {post_response.status_code}")
                # Print an error message
                print(f"Image request failed with status code {image_response.status_code}")
                # Print an error message
                print(f"GET request failed with status code {response.status_code}")

