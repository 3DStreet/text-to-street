# text-to-street
Text to street assistant (chatbot, powered by OpenAI GPT model)
The assistant's purpose is to use the given text description of the street to form a corresponding 3D model of the street on the 3DStreet.org portal. The response is returned as a URL in the format 3dstreet.app/#url_encoded_json=...
or it could be also optional format: 3dstreet.app/#query=<street description>
# Main parts of code:
The file functions/text-to-street.py contains code for generating the assistant via the OpenAI API. The chatCompletion function is used to create an assistant, as well as the function_call mechanism to return a response from the assistant in the form of JSON of a given structure. The JSON structure has a streetmix API JSON structure (simplified for 3DStreet forming, not all properties from streetmix), which describes street segments in streetmix format. Based on this answer, a 3D street is generated on the side of the 3DStreet code.

The file functions/main.py contains a function to respond to a user's http request (via a URL provided by firebase functions). The user's request with a text description of the street is transmitted in the query parameter of the http request or by json(if the mimetype is application/json): {'query': '...'}. After deploying the firebase function to the firebase server, a URL is provided to access the function described here.

