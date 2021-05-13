import random
import uuid
import requests
import http.client
import pika
from urllib.request import urlopen
from http.client import RemoteDisconnected
from flask import Flask, request

app = Flask(__name__)
message_url = "http://localhost:9001"
logging_url = "http://localhost:5703"


def get_rand_logging_client():
    return random.choice(["http://localhost:5708", "http://localhost:5709", "http://localhost:5710"])

def get_rand_messaging_queue():
    return random.choice(["http://localhost:9009", "http://localhost:9010"])

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



def get_rand_logging():
    rand = get_rand_logging_client()
    print(rand)
    return rand

def get_rand_messaging():
    rand = get_rand_messaging_queue()
    print(rand)
    return rand

def get_request():
    print('send GET-like request to logging service')
    get_logging_response = requests.get(f'{get_rand_logging()}/logging-service')
    print('Received from logging service: ', get_logging_response)
    m_response = requests.get(f'{get_rand_messaging()}/messages')
    print('received from messages:', m_response.content)
    return f'Received from logging service: {str(get_logging_response.text)}, \n' \
           f'Received from messages service: {str(m_response.text)}'


def post_messages(msg: str):
    connect = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connect.channel()
    channel.queue_declare(queue='mq')
    channel.basic_publish(exchange='', routing_key="mq", body=msg,)
    print(f"[x] Sent message, please receive : {msg}")
    connect.close()

def post_request():
    print('POST request to message service')
    post_messages(request.json.get('msg'))
    print('POST request to logging service')
    l_request = {"uuid": str(uuid.uuid4()), "msg": request.json.get('msg')}
    l_response = requests.post(f'{get_rand_logging()}/logging-service', json=l_request)
    status = l_response.status_code
    print('Received status from logging service:', status)
    stat = app.response_class(status=status)
    return stat


if __name__ == '__main__':
     app.run(host='0.0.0.0', port=9002, debug=True)

