# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from texttostreet import get_streetmix_json

from firebase_functions import https_fn, options
# The Firebase Admin SDK to access Cloud Firestore.
import firebase_admin
from firebase_admin import firestore

app = firebase_admin.initialize_app()
db = firestore.client()


# [START all]
# This endpoint supports CORS.
# [START trigger]
# [START usingMiddleware]
@https_fn.on_request(
    cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"])
)
def street_url(req: https_fn.Request) -> https_fn.Response:
    """Get the server's local date and time."""
    # [END usingMiddleware]
    # [END trigger]
    # [START sendError]
    # Forbidding PUT requests.
    if req.method == "PUT":
        return https_fn.Response(status=403, response="Forbidden!")
    # [END sendError]

    # [START readQueryParam]
    user_message = req.args["query"] if "query" in req.args else None
    # [END readQueryParam]

    # Reading user message from request body query parameter, if provided
    if user_message is None:
        # [START readBodyParam]
        body_data = req.get_json(silent=True)
        if body_data is None or "query" not in body_data:
            return https_fn.Response(
                status=400, response="Query string missing"
            )
        user_message = body_data["query"]
        # [END readBodyParam]

    # [START sendResponse]
    streetmix_json = get_streetmix_json(user_message)
    return https_fn.Response(streetmix_json)
    # [END sendResponse]

# [END all]