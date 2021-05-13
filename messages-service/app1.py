
#from flask import Flask

#app = Flask(__name__)


#@app.route('/messages')
#def messages():
    #return 'not implemented, please visit this page later'


#if __name__ == '__main__':
      #app.run(host='0.0.0.0', port=9001, debug=True)

import threading
import pika
from flask import Flask

app = Flask(__name__)


@app.route('/messages',  methods=['GET'])
def messages():
    print(msg_1)
    return str(msg_1)


def thread_receive(target):
    def run(*args, **kwargs):
        thr = threading.Thread(target=target, args=args, kwargs=kwargs)
        thr.start()
        return thr
    return run

@thread_receive
def main_consume(msg):
    connect = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connect.channel()
    channel.queue_declare(queue='mq')
    for method_frame, properties, body in channel.consume('mq'):
        print("Received messages to this service %r" % body)
        print('Old messages: ', msg)
        msg.append(str(body))
        print('Newest messages', msg)

if __name__ == '__main__':
    msg_1 = []
    main_consume(msg_1)
    print('Second message service is working................................')
    app.run(host='0.0.0.0', port=9010, debug=False)