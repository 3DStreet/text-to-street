import openai
import json
import os
from dotenv import dotenv_values

config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

#openai.api_key = os.getenv("OPENAI_API_KEY")

ASSIST_TEXT_FILENAME = 'prompt_bot.txt'
STREETMIX_SCHEMA_FILENAME = 'streetmix.json'


def load_prompt():
    with open(ASSIST_TEXT_FILENAME, "r") as file:
        return file.read()


def load_streetmix_schema():
    with open(STREETMIX_SCHEMA_FILENAME, "r") as file:
        return json.loads(file.read())


def get_street(name, title, data):
    """Return streetmix JSON with street description"""
    # here will be valid JSON checking
    print(name)
    print(data)
    return json.dumps({"name": title, "data": data})


def get_streetmix_json(user_message):
    # Step 1: send the conversation and available functions to GPT
    assistant_description = load_prompt()
    sreetmix_schema = load_streetmix_schema()
    messages = [
        {"role": "system", "content": assistant_description},
        {"role": "system", "content": "Only use the functions you have been provided with. Use default values for properties if they are not provided. Only output valid JSON"},
        {"role": "user", "content": user_message}
    ]
    functions = [
        {
            "name": "get_street",
            "description": "get 3d street (url with 3dstreet) by its description",
            "parameters": sreetmix_schema
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",
        # auto is default. "auto" means the model can pick between an end-user or calling a function
    )
    response_message = response["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_street": get_street,
        }
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        print(function_args)
        function_response = fuction_to_call(
            name=function_args.get("name"),
            title=user_message,
            data=function_args.get("data"),
        )

        return function_response # return JSON from get_street

    return response_message # in case if GPT not called a function

# get_streetmix_json("create a street with sidewalks and palm trees, red bicicle roads, bus station, train and car roads. with grass in one side and buildings in another")