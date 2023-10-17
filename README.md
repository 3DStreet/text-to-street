# Text-to-Street
## Street assistant chatbot, powered by OpenAI GPT-4 model
The assistant's purpose is to use the given text description of the street to create a corresponding 3D model of the street in 3DStreet.app. The response is returned as a URL in next format: 
`3dstreet.app/#url_encoded_json=...`
or it could be also optional format: `3dstreet.app/#query=street_description`
### Main parts of code:
`functions/text-to-street.py` contains code for generating the assistant via the OpenAI API. The chatCompletion function is used to create an assistant, as well as the OpenAI [function_call](https://platform.openai.com/docs/guides/gpt/function-calling) feature to return a response from the assistant in the form of JSON of a given structure. The JSON structure has a streetmix API JSON structure (simplified for 3DStreet forming, not all properties from streetmix), which describes street segments in streetmix format. Based on this answer, a 3D street will be generated on the side of the 3DStreet portal. To generate a 3D street on the 3DStreet.app side, the response from the model in the form of encoded json is passed to the `url_encoded_json` parameter of the http request to 3dstreet.app:
`3dstreet.app/#url_encoded_json=...`

`functions/main.py` contains a function to respond to a user's http request (via a URL provided by firebase functions). 
#### Description of the request URL to the firebase function
The user's request with a text description of the street is transmitted in the `query` parameter of the http request or by json (if the mimetype of request is `application/json`): {'query': '...'}. After deploying the firebase function to the firebase server, a URL is provided to access the function described here.

# Next steps
- create JSON with a description of segments and their variants supported in 3dStreet
- use it to check the model's response and to generate a better assistant's response
- continue the dialogue after generating the street to correct/change street parameters

Running streaming to console demo:

add .env with OPENAI_API_KEY=[your token] inside of ./functions
python3 -m venv ./venv
pip3 install -r requirements.txt
cd functions
python3
from texttostreetdemo import get_streetmix_json
get_streetmix_json('make a street with 1 car lane and 1 parking lane')
