from flask_restful import Resource, reqparse, marshal_with, fields

from services.googlevisionapi import VisionApi
from services.imageutil import remove_color
from services.textextractor import extract_ticket_from_list

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

        image_clean = remove_color(image_base64)

        vapi = VisionApi()
        text_response = vapi.detect_text([image_clean])
        text_found = text_response[0][0]["description"]
        text_list = text_found.split("\n")

        ticket = extract_ticket_from_list(text_list)

        response["ticket"] = ticket

        return response

