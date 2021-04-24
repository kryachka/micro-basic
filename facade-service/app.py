import random
import uuid
import requests
import http.client
from urllib.request import urlopen
from http.client import RemoteDisconnected
from flask import Flask, request

app = Flask(__name__)
message_url = "http://localhost:9001"
logging_url = "http://localhost:5703"


def get_rand_logging_client():
    return random.choice(["http://localhost:5708", "http://localhost:5709", "http://localhost:5710"])


@app.route('/facade-service', methods=['GET', 'POST'])
def facadeService():
    try:
        if request.method == 'GET':
            return get_request()
        else:
            return post_request()
    except http.client.HTTPException as e:
        return ("HTTPException")
    except RemoteDisconnected:
        "continue"



def get_rand():
    rand = get_rand_logging_client()
    print(rand)
    return rand



def get_request():
    print('send GET-like request to logging service')
    get_logging_response = requests.get(f'{get_rand()}/logging-service')
    print('Received from logging service: ', get_logging_response)
    m_response = requests.get(f'{message_url}/messages')
    print('received from messages:', m_response.content)
    return f'Received from logging service: {str(get_logging_response.text)}, \n' \
           f'Received from messages service: {str(m_response.text)}'


def post_request():
    print('POST request to logging service')
    l_request = {"uuid": str(uuid.uuid4()), "msg": request.json.get('msg')}
    l_response = requests.post(f'{get_rand()}/logging-service', json=l_request)
    status = l_response.status_code
    print('Received status from logging service:', status)
    stat = app.response_class(status=status)
    return stat


if __name__ == '__main__':
     app.run(host='0.0.0.0', port=9002, debug=True)

