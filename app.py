#Adding to pythonpath
from flask import Flask
from flask_restful import Api
from resources.ticket2text import Ticket2TextResource
from resources.verifier import VerifierResource

# Version
major = 0
minor = 1

app = Flask(__name__)
api = Api(app)

# This function enables CORS in all requests
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET')
  return response

prefix = '/ticket/' + str(major) + '.' + str(minor)

api.add_resource(Ticket2TextResource, prefix+'/image')
api.add_resource(VerifierResource, prefix+'/verify')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)

