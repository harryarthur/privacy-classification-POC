from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

messages = []

#define what happens when the POST method is called on localhost:5000/receive. Alice (or nay sender) will call this function
@app.route('/receive', methods=['POST'])
def receive_message():
    global messages
    message = request.json
    classification = message.get('Classification')
    #forward message to protected server if classification is higher than Unclassified
    if classification != 'Unclassified':
        forward_message(message, 'http://localhost:5001')
    else:
        messages.append(message)
    return 'Message processed successfully at Unclassified Server', 200

#define what happens when the GET method is called on localhost5000/get_messages. All receivers of unclassified messages will call this.
@app.route('/get_messages', methods=['GET'])
def get_messages():
    global messages
    return jsonify(messages), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5000)
