from flask import request, Flask
import hazelcast
app = Flask(__name__)

dictionary = {}
client = hazelcast.HazelcastClient(
        cluster_name="dev",
        cluster_members=[
            "127.0.0.1:5703",
            "127.0.0.1:5704",
            "127.0.0.1:5705"
        ],
        lifecycle_listeners=[lambda state: print("Lifecycle:", state), ]
    )

@app.route('/logging-service', methods=['GET', 'POST'])
def loggingService():
    if request.method == 'GET':
        return ','.join([msg for msg in dictionary.values()])
    else:
        return post_request()
distributed_map=client.get_map("map")

def post_request():
    print(f'Received request: {request}..............')
    uuid = request.uuid
    msg = request.msg
    distributed_map.put(uuid, msg)
    #dictionary.update({request.json["uuid"]: request.json["msg"]})
    print(f'saved .............')
    return app.response_class(status=200)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5703, debug=True)

