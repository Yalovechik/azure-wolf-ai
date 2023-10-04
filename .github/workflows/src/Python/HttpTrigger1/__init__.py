# import logging

# import azure.functions as func


# def main(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     name = req.params.get('name')
#     if not name:
#         try:
#             req_body = req.get_json()
#         except ValueError:
#             pass
#         else:
#             name = req_body.get('name')

#     if name:
#         return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
#     else:
#         return func.HttpResponse(
#              "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
#              status_code=200
#         )

# import logging
# import azure.functions as func
# from azure.storage.blob import BlobServiceClient
# from . import scraper
# import re
# import requests  # Don't forget to add 'requests' to your requirements.txt file
# from azure.data.tables import TableServiceClient
# from urllib.parse import urlencode

# def main(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     url_domain = req.params.get('domain')
#     url_ext = req.params.get('extension')
#     url_full = "http://www." + url_domain + "." + url_ext

#     result = scraper.extract_text_and_images(url_full)  # Use the updated scraper function

#     if not url_domain:
#         try:
#             req_body = req.get_json()
#         except ValueError:
#             pass
#         else:
#             url_domain = req_body.get('domain')

#     if url_domain:
#         blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=teststorageaccountscrapp;AccountKey=N9IoVfErpKzPa4xhprvWKXWWdlPi6Tu0zW+o+EFXBDcN1DZc9yQtBH/NKY48rlsfqXIvQTThwWmQ+AStq4R0KQ==;EndpointSuffix=core.windows.net")

#         # Store text content in a separate blob container
#         text_container_client = blob_service_client.get_container_client("textcontainer")
#         text_blob_client = text_container_client.get_blob_client("doc.txt")
#         text_blob_client.upload_blob(result["text_content"], overwrite=True)

#         # Store images in another blob container (e.g., "imagecontainer")
#         image_container_client = blob_service_client.get_container_client("imagecontainer")

#         # Set up table client
#         table_service_client = TableServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=teststorageaccountscrapp;AccountKey=N9IoVfErpKzPa4xhprvWKXWWdlPi6Tu0zW+o+EFXBDcN1DZc9yQtBH/NKY48rlsfqXIvQTThwWmQ+AStq4R0KQ==;EndpointSuffix=core.windows.net")
#         table_name = "test"
#         table_client = table_service_client.get_table_client(table_name)        

#         encoded_url = urlencode({'url_full': url_full}) 

#         entity = {
#             "PartitionKey": "URLs",  # You can choose your partition key
#             "RowKey": encoded_url,           # You can use a unique identifier as the row key
#             "url_full": url_full
#         }
        
#         query_filter = f"PartitionKey eq 'URLs' and RowKey eq '{encoded_url}'"
#         existing_entities = table_client.query_entities(query_filter)

#         if not list(existing_entities):
#             table_client.upsert_entity(entity=entity)
           
#         else:
#             logging.warning(f"URL '{url}' already exists in Azure Table Storage.")
            
            

#         for image_url in result["image_urls"]:
#             # Check if the URL has a scheme (e.g., 'http://', 'https://')
#             if not image_url.startswith('http://') and not image_url.startswith('https://'):
#                 # If not, assume it's an incomplete URL and add a default scheme (e.g., 'http://')
#                 image_url = 'http://' + image_url

#             # Generate a unique blob name based on the image URL or use your preferred naming scheme
#             # For simplicity, we'll use the image filename here.
#             image_filename = image_url.split("/")[-1]
#             image_blob_client = image_container_client.get_blob_client(image_filename)

#             # Download the image and upload it to the image container
#             image_response = requests.get(image_url)
#             if image_response.status_code == 200:
#                 image_blob_client.upload_blob(image_response.content, overwrite=True)
#             else:
#                 logging.warning(f"Failed to download and store image: {image_url}")

#         return func.HttpResponse(f"Text content and images saved to Azure Blob Storage.")
#     else:
#         return func.HttpResponse(
#              "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
#              status_code=200
#         )

# # import logging
# # import azure.functions as func
# # from azure.storage.blob import BlobServiceClient
# # from . import scraper
# # import re
# # import requests
# # from azure.data.tables import TableServiceClient
# # from urllib.parse import urlencode
# # from datetime import datetime, timedelta  # Import datetime

# # def main(req: func.HttpRequest) -> func.HttpResponse:
# #     logging.info('Python HTTP trigger function processed a request.')

# #     url_domain = req.params.get('domain')
# #     url_ext = req.params.get('extension')
# #     url_full = "http://www." + url_domain + "." + url_ext

# #     result = scraper.extract_text_and_images(url_full)

# #     if not url_domain:
# #         try:
# #             req_body = req.get_json()
# #         except ValueError:
# #             pass
# #         else:
# #             url_domain = req_body.get('domain')

# #     if url_domain:
# #         blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=teststorageaccountscrapp;AccountKey=N9IoVfErpKzPa4xhprvWKXWWdlPi6Tu0zW+o+EFXBDcN1DZc9yQtBH/NKY48rlsfqXIvQTThwWmQ+AStq4R0KQ==;EndpointSuffix=core.windows.net")

# #         text_container_client = blob_service_client.get_container_client("textcontainer")
# #         text_blob_client = text_container_client.get_blob_client("doc.txt")

# #         # Set up table client
# #         table_service_client = TableServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=teststorageaccountscrapp;AccountKey=N9IoVfErpKzPa4xhprvWKXWWdlPi6Tu0zW+o+EFXBDcN1DZc9yQtBH/NKY48rlsfqXIvQTThwWmQ+AStq4R0KQ==;EndpointSuffix=core.windows.net")
# #         table_name = "test"
# #         table_client = table_service_client.get_table_client(table_name)

# #         encoded_url = urlencode({'url_full': url_full})

# #         entity = {
# #             "PartitionKey": "URLs",
# #             "RowKey": encoded_url,
# #             "url_full": url_full
# #         }

# #         query_filter = f"PartitionKey eq 'URLs' and RowKey eq '{encoded_url}'"
# #         existing_entities = table_client.query_entities(query_filter)

# #         if not list(existing_entities):
# #             table_client.upsert_entity(entity=entity)
# #         else:
# #             entity = list(existing_entities)[0]
# #             last_modified = entity["Timestamp"].replace(tzinfo=None)
# #             seven_days_ago = datetime.utcnow() - timedelta(days=7)
                
# #             # if existing_entities:

# #             # # Check if the entity was modified within the last 7 days
# #             #     entity = list(existing_entities)[0]
# #             #     last_modified = entity["Timestamp"].replace(tzinfo=None)
# #             #     seven_days_ago = datetime.utcnow() - timedelta(days=7)
# #             if last_modified >= seven_days_ago:
# #                 return func.HttpResponse(f"URL '{url_full}' already exists in Azure Table Storage and was modified within the last 7 days.")

# #         text_blob_client.upload_blob(result["text_content"], overwrite=True)

# #         image_container_client = blob_service_client.get_container_client("imagecontainer")

# #         for image_url in result["image_urls"]:
# #             if not image_url.startswith('http://') and not image_url.startswith('https://'):
# #                 image_url = 'http://' + image_url

# #             image_filename = image_url.split("/")[-1]
# #             image_blob_client = image_container_client.get_blob_client(image_filename)

# #             image_response = requests.get(image_url)
# #             if image_response.status_code == 200:
# #                 image_blob_client.upload_blob(image_response.content, overwrite=True)
# #             else:
# #                 logging.warning(f"Failed to download and store image: {image_url}")

# #         return func.HttpResponse(f"Text content and images saved to Azure Blob Storage.")
# #     else:
# #         return func.HttpResponse(
# #             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
# #             status_code=200
# #         )



# import logging
# import azure.functions as func
# from azure.storage.blob import BlobServiceClient
# from . import scraper
# import re
# import requests  # Don't forget to add 'requests' to your requirements.txt file
# from azure.data.tables import TableServiceClient
# from urllib.parse import urlencode

# def main(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     url_domain = req.params.get('domain')
#     url_ext = req.params.get('extension')
#     url_full = "http://www." + url_domain + "." + url_ext

#     result = scraper.extract_text_and_images(url_full)  # Use the updated scraper function

#     if not url_domain:
#         try:
#             req_body = req.get_json()
#         except ValueError:
#             pass
#         else:
#             url_domain = req_body.get('domain')

#     if url_domain:
#         blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=teststorageaccountscrapp;AccountKey=N9IoVfErpKzPa4xhprvWKXWWdlPi6Tu0zW+o+EFXBDcN1DZc9yQtBH/NKY48rlsfqXIvQTThwWmQ+AStq4R0KQ==;EndpointSuffix=core.windows.net")

#         # Store text content in a separate blob container
#         text_container_client = blob_service_client.get_container_client("textcontainer")
#         text_blob_client = text_container_client.get_blob_client("doc.txt")
#         text_blob_client.upload_blob(result["text_content"], overwrite=True)

#         # Store images in another blob container (e.g., "imagecontainer")
#         image_container_client = blob_service_client.get_container_client("imagecontainer")

#         # Set up table client
#         table_service_client = TableServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=teststorageaccountscrapp;AccountKey=N9IoVfErpKzPa4xhprvWKXWWdlPi6Tu0zW+o+EFXBDcN1DZc9yQtBH/NKY48rlsfqXIvQTThwWmQ+AStq4R0KQ==;EndpointSuffix=core.windows.net")
#         table_name = "test"
#         table_client = table_service_client.get_table_client(table_name)        

#         encoded_url = urlencode({'url_full': url_full}) 

#         entity = {
#             "PartitionKey": "URLs",  # You can choose your partition key
#             "RowKey": encoded_url,           # You can use a unique identifier as the row key
#             "url_full": url_full
#         }
#         # query_filter = f"PartitionKey eq 'URLs' and url_full eq '{url_full}'"
#         query_filter = f"PartitionKey eq 'URLs' and RowKey eq '{encoded_url}'"
#         existing_entities = table_client.query_entities(query_filter)

#         if not list(existing_entities):
#             table_client.upsert_entity(entity=entity)
           
#         else:
#             logging.warning(f"URL '{url}' already exists in Azure Table Storage.")

    
#         # query_filter = f"PartitionKey eq '{entity['PartitionKey']}' and url_full eq '{entity['url_full']}'"
#         # existing_entities = table_client.query_entities(query_filter)
#         # try:
#         #     first_entity = next(existing_entities)
#         #     logging.warning (f"An entity with PartitionKey='{entity['PartitionKey']}' and url_full='{entity['url_full']}' already exists.")
#         # except StopIteration:
#         #     pass
#         # table_client.upsert_entity(entity=entity)
            
            
            

#         for image_url in result["image_urls"]:
#             # Check if the URL has a scheme (e.g., 'http://', 'https://')
#             if not image_url.startswith('http://') and not image_url.startswith('https://'):
#                 # If not, assume it's an incomplete URL and add a default scheme (e.g., 'http://')
#                 image_url = 'http://' + image_url

#             # Generate a unique blob name based on the image URL or use your preferred naming scheme
#             # For simplicity, we'll use the image filename here.
#             image_filename = image_url.split("/")[-1]
#             image_blob_client = image_container_client.get_blob_client(image_filename)

#             # Download the image and upload it to the image container
#             image_response = requests.get(image_url)
#             if image_response.status_code == 200:
#                 image_blob_client.upload_blob(image_response.content, overwrite=True)
#             else:
#                 logging.warning(f"Failed to download and store image: {image_url}")

#         return func.HttpResponse(f"Text content and images saved to Azure Blob Storage.")
#     else:
#         return func.HttpResponse(
#              "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
#              status_code=200
#         )

# import logging 
# import azure.functions as func 
# from azure.storage.blob import BlobServiceClient 
# from . import scraper 
# import re 
# import requests  # Don't forget to add 'requests' to your requirements.txt file 
 
# def main(req: func.HttpRequest) -> func.HttpResponse: 
#     logging.info('Python HTTP trigger function processed a request.') 
 
#     url_domain = req.params.get('domain') 
#     url_ext = req.params.get('extension') 
#     url_full = "http://www." + url_domain + "." + url_ext 
 
#     result = scraper.extract_text_and_images(url_full)  # Use the updated scraper function 
 
#     if not url_domain: 
#         try: 
#             req_body = req.get_json() 
#         except ValueError: 
#             pass 
#         else: 
#             url_domain = req_body.get('domain') 
 
#     if url_domain: 
#         blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=teststorageaccountscrapp;AccountKey=N9IoVfErpKzPa4xhprvWKXWWdlPi6Tu0zW+o+EFXBDcN1DZc9yQtBH/NKY48rlsfqXIvQTThwWmQ+AStq4R0KQ==;EndpointSuffix=core.windows.net") 
 
#         # Store text content in a separate blob container 
#         text_container_client = blob_service_client.get_container_client("textcontainer") 
#         text_blob_client = text_container_client.get_blob_client("doc.txt") 
#         text_blob_client.upload_blob(result["text_content"], overwrite=True) 
 
#         # Store images in another blob container (e.g., "imagecontainer") 
#         image_container_client = blob_service_client.get_container_client("imagecontainer") 
 
#         for image_url in result["image_urls"]: 
#             # Check if the URL has a scheme (e.g., 'http://', 'https://') 
#             if not image_url.startswith('http://') and not image_url.startswith('https://'): 
#                 # If not, assume it's an incomplete URL and add a default scheme (e.g., 'http://') 
#                 image_url = 'http://' + image_url 
 
#             # Generate a unique blob name based on the image URL or use your preferred naming scheme 
#             # For simplicity, we'll use the image filename here. 
#             image_filename = image_url.split("/")[-1] 
#             image_blob_client = image_container_client.get_blob_client(image_filename) 
 
#             # Download the image and upload it to the image container 
#             image_response = requests.get(image_url) 
#             if image_response.status_code == 200: 
#                 image_blob_client.upload_blob(image_response.content, overwrite=True) 
#             else: 
#                 logging.warning(f"Failed to download and store image: {image_url}") 
 
#         return func.HttpResponse(f"Text content and images saved to Azure Blob Storage.") 
#     else: 
#         return func.HttpResponse( 
#              "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.", 
#              status_code=200 
#         )



import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import scraper
import re
import requests  # Don't forget to add 'requests' to your requirements.txt file
from azure.data.tables import TableServiceClient
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    table_name = os.environ.get('TABLE_NAME')
    imagecontainer = os.environ.get('BLOB_STORAGE_IMAGE_NAME')
    textcontainer = os.environ.get('BLOB_STORAGE_TEXT_NAME')
    

    url_domain = req.params.get('domain')
    url_ext = req.params.get('extension')
    url_full = "http://www." + url_domain + "." + url_ext

    result = scraper.extract_text_and_images(url_full)  # Use the updated scraper function

    if not url_domain:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            url_domain = req_body.get('domain')

    if url_domain:
        blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=mdtje40jf6;AccountKey=B+zzS7rp644l9q5I5I94rx07jpd7xHuymgBDMQsB1E1u/9+ix+lV5o83BzZvjjmdFUGV106uRfvK+ASt4Gkesg==;EndpointSuffix=core.windows.net")

        # Store text content in a separate blob container
        text_container_client = blob_service_client.get_container_client("textcontainer")
        text_blob_client = text_container_client.get_blob_client("doc.txt")
        text_blob_client.upload_blob(result["text_content"], overwrite=True)

        # Store images in another blob container (e.g., "imagecontainer")
        image_container_client = blob_service_client.get_container_client("imagecontainer")

        # Set up table client
        table_service_client = TableServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=mdtje40jf6;AccountKey=B+zzS7rp644l9q5I5I94rx07jpd7xHuymgBDMQsB1E1u/9+ix+lV5o83BzZvjjmdFUGV106uRfvK+ASt4Gkesg==;EndpointSuffix=core.windows.net")
        # table_name = "test"
        table_client = table_service_client.get_table_client(table_name)

        entity = {
            "PartitionKey": "URLs",  # You can choose your partition key
            "RowKey": "1",           # You can use a unique identifier as the row key
            "url_full": url_full
        }

        table_client.upsert_entity(entity=entity)

        for image_url in result["image_urls"]:
            # Check if the URL has a scheme (e.g., 'http://', 'https://')
            if not image_url.startswith('http://') and not image_url.startswith('https://'):
                # If not, assume it's an incomplete URL and add a default scheme (e.g., 'http://')
                image_url = 'http://' + image_url

            # Generate a unique blob name based on the image URL or use your preferred naming scheme
            # For simplicity, we'll use the image filename here.
            image_filename = image_url.split("/")[-1]
            image_blob_client = image_container_client.get_blob_client(image_filename)

            # Download the image and upload it to the image container
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                image_blob_client.upload_blob(image_response.content, overwrite=True)
            else:
                logging.warning(f"Failed to download and store image: {image_url}")

        return func.HttpResponse(f"Text content and images saved to Azure Blob Storage.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
