from flask_restful import Resource, reqparse, marshal_with, fields

from services.googlevisionapi import VisionApi

query_parser = reqparse.RequestParser()

query_parser.add_argument(
    'image64', dest='image_base64',
    required=True,
    type=str, help='The image of the ticket to extract the text',
)

class Ticket2TextResource(Resource):

    def post(self):

        response = {}
        args = query_parser.parse_args()

        image_base64 = args["image_base64"]

        try: 

            vapi = VisionApi()
            response["response"] = vapi.detect_text([image_base64])

        except Exception as e:
            response = {
                "error": str(e)
            }

        return response

