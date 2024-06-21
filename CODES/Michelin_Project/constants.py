# to store project constants
import os, uuid

# set an example ean code
ean_code = 8903094003235

# custom googlesearch apis
googlesearch_api_key = "AIzaSyDrGleWG7xtZz7BwAoIbgepki-8MHPlcZs"
googlesearch_cx = "b444d65462a034340"
googlesearch_api_url = "https://www.googleapis.com/customsearch/v1"
gemini_api_key = "AIzaSyBQOKOLox8xpKHZ8qTLdVXYpAm_-Sg6CFs"

# html tags to parse while scraping the webpages
tags_to_use = ["p", "article", "div" "h1", "h2", "h3", "h4", "span", "a", "b", "li", "td", "th"]
tags_to_ignore = ["script", "style"]

# langchain pipeline variables
max_chunk_size = 2500
chunk_intersection_size = 200

# azure translator api
azure_translator_api_key = "6e19c8bf0fec412583603a2541d7f498"
azure_translator_location = "westeurope"
azure_translator_creds = {
    "azure_translator_api_key" :  azure_translator_api_key,
    "azure_translator_endpoint" : "https://api.cognitive.microsofttranslator.com/",
    "azure_translator_location" : azure_translator_location,
    "azure_translator_path" : "/translate",
    "azure_translator_params" : {
        'api-version' : '3.0',
        'to' : ['en']
    },
    "headers" : {
        'Ocp-Apim-Subscription-Key': azure_translator_api_key,
        # location required if you're using a multi-service or regional (not global) resource.
        'Ocp-Apim-Subscription-Region': azure_translator_location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
}