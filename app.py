import os
from flask import Flask
from flask import jsonify
from flask import request
import json
from cerberus import Validator
from exceptions import payLoadIsMissing
from exceptions import malformedJson
from exceptions import payloadNotMatchingSchema
from logger import Logger
import merger
LOG = Logger()

app = Flask(__name__)


@app.errorhandler(payLoadIsMissing)
@app.errorhandler(payloadNotMatchingSchema)
@app.errorhandler(malformedJson)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


payload_input_schema = {
                    'payload': {'type': 'dict', 'required': True},
                    }



@app.route("/ping")
def ping():
    return "Pong!"

@app.route("/example")
def example():
    return '{ "data": { "one": 1, "two": 2 }, "template": "ivo.docx", "bucket_name": "ah-doc-templates", "user":"1243454554545" }'

@app.route("/schema")
def schema():
    return json.dumps(dict(input=payload_input_schema))

@app.route("/", methods=['GET'])
def index():
    return 'Block-export-doc'

@app.route("/merge", methods=['POST', 'GET'])
def fn():  
    v = Validator()
    v.schema = payload_input_schema
    payload = request.form.get('payload', None)
    if not(payload):
        raise payLoadIsMissing('There is no payload', status_code=500)
    try:
        payload = json.loads(payload)
    except:
        raise malformedJson("Payload present but malformed: {}".format(payload))
    
    LOG.console(payload)

    info = dict(url = merger.merge(**payload))
    
    result = dict(success=True, payload=info)
    result = json.dumps(result)
    return result
   

if __name__ == "__main__":
    port = int(os.environ.get('PORT'))
    app.run(host='0.0.0.0', port=port)