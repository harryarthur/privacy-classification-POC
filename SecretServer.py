from flask import Flask, request, jsonify
import requests
SecretKey = 4

app = Flask(__name__)

messages = []

#only the Protected server will be calling this method. Only Secret messages will come through. Therefore we encrypt it straight away.
@app.route('/receive', methods=['POST'])
def receive_message():
    global messages
    message = request.json
    #Encrypt with secret key
    message['content'] = ''.join([chr(ord(c) + (SecretKey)) for c in message['content']])
    messages.append(message)
    return 'Message processed successfully at Secret Server', 200

#users attempting to receive a secret message will call this
@app.route('/get_messages', methods=['GET'])
def get_messages():
    global messages
    return jsonify(messages), 200

#Run on port 5002
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5002)
