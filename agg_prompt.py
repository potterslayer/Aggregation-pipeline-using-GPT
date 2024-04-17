from openai import OpenAI
import os
from dotenv import load_dotenv
MONGODB_CONNECTION_STRING=os.environ.get("")
DB_NAME=os.environ.get("")
COLLECTION_NAME=os.environ.get("")
_ = load_dotenv()
client = OpenAI(api_key="")
def get_system_prompt():
    return f"""You are a MongoDB expert with great expertise in writing MongoDB queries \
    for any given data to produce an expected output.
    """
    
def get_user_prompt(input_data, output_data):
    return f"""Your task is to write a MongoDB Query, specifically an aggregation pipeline\
    that would produce the expected output for the given input.

    You will always return a JSON response with the following fields.
    ```
    mongoDBQuery: The MongoDB aggregation pipeline to produce the expected output for a given input.\
    This field corresponds to just the list of stages in the aggregation pipeline \
    and shouldn't contain the "db.collection.aggregate" prefix.
    
    queryExplanation: A detailed explanation for the query that was returned.
    ```
    
    Input data: {input_data} 
    Expected output data: {output_data}
    """
def get_mongodb_query(input_data, output_data, model):
    system_prompt = get_system_prompt()
    user_prompt = get_user_prompt(input_data, output_data)

    #print(f"System Prompt: {system_prompt}")
    #print(f"User Prompt: {user_prompt}")
    
    messages = []
    messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})
    
    chat_completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        response_format={"type": "json_object"}
    )

    print(f"Assistant Response:\n{chat_completion.choices[0].message.content}")
ex1_input_data = """
[
  { "name": "Santa", "team": "India" },
  { "name": "Banta", "team": "India" },
  { "name": "gayle", "team": "West Indies" }
]
"""

ex1_output_data = """
[
 { "team": India, "playerCount": 2 },
 { "team": "West Indies", "playerCount": 1 }
]
"""
get_mongodb_query(ex1_input_data, ex1_output_data, "gpt-3.5-turbo-1106")