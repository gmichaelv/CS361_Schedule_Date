'''Use if running in flask'''

from flask import Flask, render_template, request, jsonify
import datetime
import json
import socket

app = Flask(__name__)

# Set the host and port for the socket server connection
HOST = '127.0.0.1'
PORT = 65432

def send_request(review_id, increment=None):
    """Send request to the server and receive the response."""
    request_data = {
        'id': review_id,
        'increment': increment
    }

    # Establish a connection to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))

        # Send data to the server
        client_socket.sendall(json.dumps(request_data).encode())

        # Receive the server's response
        response = client_socket.recv(1024).decode()

        if not response:
            return "No response from server"

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return "Error decoding server response"

@app.route('/')
def index():
    """Render the index page with the review form."""
    return render_template('index.html')

@app.route('/schedule', methods=['POST'])
def schedule():
    """Handle the form submission and send the request to the server."""
    review_id = request.form['review_id']
    increment = request.form.get('increment', 60)  # Default to 60 days if not provided
    app.logger.info(f"increment value: {increment}")

    try:
        if increment == '':
            increment = 60
        else:
            increment = int(increment)
    except ValueError:
        return "Invalid increment value. Please enter an integer."

    # Send the request to the server
    response = send_request(review_id, increment)

    # Return the result as JSON
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
