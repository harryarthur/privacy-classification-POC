from flask import Flask, request, jsonify
import requests
ProtectedKey = 3
app = Flask(__name__)

messages = []

#here we define what happens when we send a POST request to localhost:5001/receive. Only the unclassified server will send this POST request.
@app.route('/receive', methods=['POST'])
def receive_message():
    global messages
    message = request.json
    #since all messages that come through this server will be at least at the protected level, we encrypt everything up to that level:
    message['content'] = ''.join([chr(ord(c) + ProtectedKey) for c in message['content']])
    messages.append(message)

    #if the message is classified Secret, we forward it to the Secret server for more encrypting
    if message.get('Classification') == 'Secret':
        forward_message(message, 'http://localhost:5002')
        print('Message forwarded to Secret server')
    
    else:
        print('Processing...')

    return 'Message processed successfully at Protected Server', 200

def forward_message(message, server_url):
    response = requests.post(server_url + '/receive', json=message)
    print(response.text)

#here we define what happens when a GET request is sent to localhost:5001/get_messages. This is called by all users who wish to read a protected message.
@app.route('/get_messages', methods=['GET'])
def get_messages():
    global messages
    return jsonify(messages), 200

#run server on port 5001
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5001)
