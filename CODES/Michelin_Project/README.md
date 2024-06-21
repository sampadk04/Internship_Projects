# Michelin: TireScan

This repository contains the code developed during my internship at Michelin for the TireScan project. The project aims to leverage EAN numbers of tires to extract valuable information from scraped web data using LLMs.

## Project Goal:

Given an EAN (European Article Number) for a tire, the goal is to:

1. **Scrape Relevant URLs:** Use the Google Custom Search API to find relevant URLs associated with the provided EAN. If no results are found, the EAN is considered invalid.
2. **Preprocess Scraped Data:** Extract and clean the text content from the scraped URLs, preparing it for LLM processing.
3. **Validate EAN:** Utilize LLMs (OpenAI or Gemini APIs) with the preprocessed data to determine if the EAN belongs to a tire.
4. **Extract Tire Information:** If the EAN is valid, extract useful information like tire name, brand, diameter, model, vehicle type, etc., from the scraped data.

## Algorithms:

This project explores four different algorithms for extracting information from the scraped data:

1. **RAG Pipeline:** This approach utilizes a retrieval-augmented generation (RAG) pipeline.
- It first creates a vector store containing embeddings of the preprocessed text chunks.
- Then, a retrieval chain is used to find relevant context from the vector store based on a query for each specific attribute.
- Finally, an LLM (Gemini-Pro) processes the retrieved context to provide the answer.

2. **Prompt Updating:** This method involves iteratively refining the LLM prompt.
- The scraped data is split into chunks, and the LLM is queried with each chunk.
- The LLM output from the previous chunk is provided as additional context for the next prompt, allowing for continuous refinement of the results.

3. **Langchain's Refine:** This approach leverages the Refine chain in Langchain.
- It uses a prompt template to extract information based on the scraped text.
- A refine template is used to continuously refine the output based on new chunks of text, improving accuracy.

4. **Langchain's Extraction Chains:** This approach utilizes Langchain's built-in extraction chains.
- It defines a schema specifying the desired information to be extracted.
- The extraction chain then uses the LLM (Gemini-Pro) to extract the information from the text content based on the defined schema.

## Code Files:
- [constants.py](./constants.py): Contains project constants, including API keys and configuration parameters.
- [final_notebook.ipynb](./final_notebook.ipynb): This Jupyter notebook contains the implementation of all four algorithms, along with the necessary setup and preprocessing steps.
- [prompts.py](./prompts.py): Contains the prompt templates used for the different algorithms.
- [requirements.txt](./requirements.txt): Lists all the required libraries for the project.
- [utils.py](./utils.py): Contains helper utility functions for text preprocessing and translation.

### Output:
The output of each algorithm is a dictionary containing the extracted information, such as:
```Python
{
    "Diameter": 12.4,
    "Width": 32,
    "Brand": "BKT",
    "Model": "TR 135",
    "Vehicle Type": "Agriculture"
}
```

## Future Work:
- Implement a more robust validation process for EANs using LLMs.
- Explore different LLM models and their impact on extraction accuracy.
- Integrate with a database to store extracted information.
- Develop a user interface for interacting with the TireScan system.

This repository provides a starting point for building a system that can extract valuable information from web data using LLMs. The code is well-documented and can be easily adapted for other similar tasks.