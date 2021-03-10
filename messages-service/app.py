
from flask import Flask

app = Flask(__name__)


@app.route('/messages')
def messages():
    return 'not implemented, please visit this page later'


if __name__ == '__main__':
      app.run(host='0.0.0.0', port=9001, debug=True)

