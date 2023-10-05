


# import re
# import requests
# from bs4 import BeautifulSoup

# def extract_text_and_images(url):
#     try:
#         # Make an HTTP request to the given URL to retrieve the page's HTML
#         response = requests.get(url)
#         response.raise_for_status()

#         # Parse the HTML content using BeautifulSoup
#         soup = BeautifulSoup(response.text, "html.parser")

#         # Extract text content from the HTML
#         text_content = soup.get_text()

#         # Find all image tags in the HTML
#         img_tags = soup.find_all("img")

#         # Extract the URLs of the images
#         image_urls = []

#         for img_tag in img_tags:
#             src = img_tag.get('src')
#             if src:
#                 image_urls.append(src)

#         return {
#             "text_content": text_content,
#             "image_urls": image_urls
#         }

#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return {
#             "text_content": "",
#             "image_urls": []
#         }

# import re
# import requests
# from bs4 import BeautifulSoup
# import os

# def extract_text_and_images(url):
#     try:
#         # Make an HTTP request to the given URL to retrieve the page's HTML
#         response = requests.get(url)
#         response.raise_for_status()

#         # Parse the HTML content using BeautifulSoup
#         soup = BeautifulSoup(response.text, "html.parser")

#         # Extract text content from the HTML
#         text_content = soup.get_text()

#         # Find all image tags in the HTML
#         img_tags = soup.find_all("img")

#         # Extract the URLs of the images
#         image_urls = []

#         for img_tag in img_tags:
#             src = img_tag.get('src')
#             if src:
#                 # Extract the base filename without query parameters
#                 base_filename, _ = os.path.splitext(src.split("?")[0])
                
#                 # Extract the file extension from the base filename
#                 file_extension = os.path.splitext(base_filename)[-1]

#                 # Define a list of valid image file extensions (add more if needed)
#                 valid_extensions = [".jpg", ".jpeg", ".png", ".gif"]

#                 # Check if the extracted file extension is valid; if not, use a default extension (e.g., ".jpg")
#                 if file_extension.lower() not in valid_extensions:
#                     file_extension = ".jpg"

#                 # Append the valid extension to the image URL
#                 src = base_filename + file_extension

#                 image_urls.append(src)

#         return {
#             "text_content": text_content,
#             "image_urls": image_urls
#         }

#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return {
#             "text_content": "",
#             "image_urls": []
#         }


import re
import requests
from bs4 import BeautifulSoup

def get_email_addresses(url):
    # Make an HTTP request to the given URL to retrieve the page's HTML
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Create a regular expression pattern to match email addresses
    pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

    # Find all the text on the page that matches the pattern
    emails = re.findall(pattern, soup.text)

    # Return the list of email addresses
    return emails