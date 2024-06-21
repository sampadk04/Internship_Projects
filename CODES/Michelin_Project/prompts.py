from langchain_core.prompts import ChatPromptTemplate
from constants import ean_code

custom_qa_prompt = ChatPromptTemplate.from_template(
    template = """You are an assistant for question-answering tasks. Use the following pieces of context scraped from web to answer the question. If you don't know the answer, just say that you don't know. Keep the answer concise.\nQuestion: {question} \nContext: {context} \nAnswer:"""
)

custom_retrival_prompt = ChatPromptTemplate.from_template(
    template="""You are an assistant for information retrieval tasks. Use the following pieces of context scraped from web to retrieve the information. If you don't know the answer, just output `NA`.\nInformation to Retrieve: {question} \nContext: {context} \nAnswer:"""
)


# output_schema = {
#     "Diameter": f"What is the diameter of the tyre with EAN code {ean_code}? Return the `diameter` (in inches) or `NA` if you don't know.",
#     "Width": f"What is the width of the tyre with EAN code {ean_code}? Return the `width` (in inches) or `NA` if you don't know.",
#     "Brand": f"What is the brand of the tyre with EAN code {ean_code}? Return the `brand name` or `NA` if you don't know.",
#     "Model": f"What is the model of the tyre with EAN code {ean_code}? Return the `model name` or `NA` if you don't know.",
#     "Vehicle Type": f"What is the vehicle type of the tyre with EAN code {ean_code}? Return `one of` Car, Truck, Agriculture, Motorcycle, Mining or `NA`.",
# }

output_schema = {
    "Diameter": f"Diameter of the tyre. Return only the `diameter` or `NA`.",
    "Width": f"Width of the tyre. Return only the `width` or `NA`.",
    "Brand": f"Brand of the tyre. Return only the `brand` or `NA`.",
    "Model": f"Model of the tyre. Return only the `model` or `NA`.",
    "Vehicle Type": f"Vehicle Type of the tyre. Return `one of` Car, Truck, Agriculture, Motorcycle, Mining or `NA`.",
}