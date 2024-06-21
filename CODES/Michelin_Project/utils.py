# helper utility functions

# imports
import os, requests

# import azure translator creds
from constants import azure_translator_creds


def remove_tags_to_ignore(soup, tags_to_ignore):
    """
    Remove the unwanted tags from the soup
    
    Parameters
    ----------
    soup: BeautifulSoup object
        soup object containing the html content
    tags_to_ignore: list
        list of html tags to ignore
    
    Returns
    -------
    soup: BeautifulSoup object
        soup object containing the html content after removing the unwanted tags
    """
    for tags in tags_to_ignore:
        for tag in soup.find_all(tags):
            tag.decompose()
    
    return soup


def extract_tags_to_use(soup, tags_to_use):
    """
    Extract the relevant tags from the soup
    
    Parameters
    ----------
    soup: BeautifulSoup object
        soup object containing the html content
    tags_to_use: list
        list of html tags to parse
    
    Returns
    -------
    text: str
        text extracted from the relevant tags
    """
    text_parts = []

    for tags in tags_to_use:
        # extract all elements with the given tag
        elements = soup.find_all(tags)

        for element in elements:
            """
            # handle the 'a' tag separately
            if tags == "a":
                text_parts.append(f"{element.text} ({element.get('href')})")
            else:
                text_parts.append(element.text)
            """
            type(element.text)
            text_parts.append(element.text)
        
    
    # loop through each text part and preprocess and clean them, 
    # by removing redundant lines and spaces
    for text_part in text_parts:
        # split the text part into lines
        lines = text_part.split("\n")

        # strip out the whitespaces for each line
        lines = [line.strip() for line in lines]

        # filter out the empty lines
        lines = [line for line in lines if line]

        # remove duplicated lines while preserving order
        seen_lines = set()
        lines = [line for line in lines if not (line in seen_lines or seen_lines.add(line))]

        # join these lines back to a single text
        text_part = " ".join(lines)
    
    # join all the text parts back to a single text
    text = " ".join(text_parts)

    # strip out the whitespaces
    text = text.strip()

    # replace the '\n's with a ' '
    text = text.replace('\n', ' ')
    text = text.strip()
    text_list = text.split(' ')
    # remove all the ''
    text_list = [x for x in text_list if x != '']
    text = ' '.join(text_list)    
    
    return text

def translate_text(text):
    """
    Translate the text using azure translator

    Parameters
    ----------
    text: str
        text to translate
    
    Returns
    -------
    translated_text: str
        translated text
    
    """
    body = [{
        'text': text
    }]

    constructed_url = azure_translator_creds['azure_translator_endpoint'] + azure_translator_creds['azure_translator_path']

    request = requests.post(
        constructed_url,
        params=azure_translator_creds['azure_translator_params'],
        headers=azure_translator_creds['headers'],
        json=body
    )

    # get the response
    response = request.json()
    # extract the translated text
    translated_text = response[0]['translations'][0]['text']

    return translated_text
    