'''Use if running in terminal'''

import socket
import json

# Server connection details
HOST = '127.0.0.1'
PORT = 65432

def send_request(review_id, increment=None):
    # Create the request data
    request_data = {
        'id': review_id,
        'increment': increment
    }
    
    # Establish connection to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        
        # Send the data to the server
        client_socket.sendall(json.dumps(request_data).encode())
        
        # Receive the response from the server
        response = client_socket.recv(1024).decode()
        return json.loads(response)

def main():
    review_id = input("Enter the review ID: ")
    increment = input("Enter increment days (press Enter for default 60): ")
    increment = int(increment) if increment else None

    # Send the request and get the response
    reviews = send_request(review_id, increment)
    
    # Print the response (the entire review schedule)
    print("Review Schedule:")
    for review in reviews:
        print(f"ID: {review['id']}, Review Date: {review['review_date']}")

if __name__ == "__main__":
    main()
