from flask import request, Flask

app = Flask(__name__)

dictionary = {}
@app.route('/logging-service', methods=['GET', 'POST'])
def loggingService():
    if request.method == 'GET':
        return ','.join([msg for msg in dictionary.values()])
    else:
        return post_request()


def post_request():
    print(f'Received request: {request}..............')
    dictionary.update({request.json["uuid"]: request.json["msg"]})
    print(f'saved .............')
    return app.response_class(status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
