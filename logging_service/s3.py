from flask import request, Flask
import hazelcast
app = Flask(__name__)


client = hazelcast.HazelcastClient(
        cluster_name="dev",
        cluster_members=[
            "127.0.0.1:5703",
            "127.0.0.1:5704",
            "127.0.0.1:5705"
        ],
        lifecycle_listeners=[lambda state: print("Lifecycle:", state), ]
    )


distributed_map=client.get_map("map")

@app.route('/logging-service', methods=['GET', 'POST'])
def loggingService():
    if request.method == 'GET':
        return ','.join([msg for msg in distributed_map.values().result()])
    else:
        return post_request()

def post_request():
    print(f'Received request: {request}..............')
    uuid = request.json.get("uuid")
    msg = request.json.get("msg")
    distributed_map.set(str(uuid), str(msg))
    #dictionary.update({request.json["uuid"]: request.json["msg"]})
    print(f'saved .............')
    return app.response_class(status=200)


def getLogging():
    # print(f'Return messages:', self.messages_dict.values())
    distributed_map = client.get_map("map")
    messages = distributed_map.values().result()
    print('messages:', messages)
    return app.response_class(
        messages=messages
    )
if __name__ == '__main__':
      app.run(host='0.0.0.0', port=5710, debug=True)


