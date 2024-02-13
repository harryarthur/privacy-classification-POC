from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

messages = []

@app.route('/receive', methods=['POST'])
def receive_message():
    global messages
    message = request.json
    classification = message.get('Classification')
    if classification != 'Unclassified':
        forward_message(message, 'http://localhost:5001')
    else:
        messages.append(message)
#        distribute_message(message)
    return 'Message processed successfully at Unclassified Server', 200

def forward_message(message, server_url):
    response = requests.post(server_url + '/receive', json=message)
    print(response.text)

@app.route('/get_messages', methods=['GET'])
def get_messages():
    global messages
    return jsonify(messages), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5000)
