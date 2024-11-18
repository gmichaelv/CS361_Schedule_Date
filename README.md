# CS361_Schedule_Date
---

# Microservice for Scheduling Review Dates

This microservice allows clients to request a review date for a given review ID, with an optional increment (default is 60 days). The server checks if there is any conflict with the proposed review date, and if there is, it increments the date by one day until no conflict exists. The review date is then saved to a database, and the server responds with the entire review schedule.

---

## How to Programmatically Request Data from the Microservice

### 1. **Overview**:

To request data from the microservice, the client sends a JSON-encoded HTTP POST request containing the review ID and an optional increment (in days). The microservice processes the request, checks for conflicts, schedules the review date, and returns the entire review schedule.

### 2. **Request Format**:

You need to send a JSON payload with the following fields:
- `id`: (required) The unique identifier for the review.
- `increment`: (optional) The number of days to increment the review date from today (default is 60 if not provided).

Example of a request:

```json
{
    "id": "review_12345",
    "increment": 45
}
```

If no increment is provided, the microservice will assume a default increment of 60 days.

### 3. **How to Send the Request**:

Here’s an example of how to send a request programmatically using Python and the `requests` library.

**Install `requests` if you don't have it already**:

```bash
pip install requests
```

**Example Code (sending request)**:

```python
import requests
import json

# The URL of the Flask app (assuming the microservice is running locally on port 5000)
url = "http://127.0.0.1:5000/schedule"

# Data to send in the request
data = {
    "id": "review_12345",  # Unique review identifier
    "increment": 30  # Optional increment (in days)
}

# Send the POST request with JSON payload
response = requests.post(url, json=data)

# Print the response from the server
if response.status_code == 200:
    print("Server Response:", response.json())
else:
    print("Error:", response.status_code, response.text)
```

### 4. **Expected Response**:

If the request is successful, the server will return a JSON response containing the full review schedule.

Example response:

```json
[
    {
        "id": "review_12345",
        "review_date": "2024-12-01"
    },
    {
        "id": "review_67890",
        "review_date": "2024-11-15"
    }
]
```

This response contains an array of scheduled reviews with their corresponding `id` and `review_date`.

---

## How to Programmatically Receive Data from the Microservice

### 1. **Overview**:

When the client sends a request, the server processes it and returns the entire review schedule in JSON format. The client then receives the data in the response and can use it as needed.

### 2. **Receiving the Response**:

The microservice will return the response as a JSON object. Here’s how you can handle and process the received data programmatically.

### 3. **How to Handle the Response**:

You can use Python's `requests` library to receive and parse the response from the microservice.

Example of handling the response:

```python
import requests

# The URL of the Flask app (assuming the microservice is running locally on port 5000)
url = "http://127.0.0.1:5000/schedule"

# Data to send in the request
data = {
    "id": "review_12345",  # Unique review identifier
    "increment": 30  # Optional increment (in days)
}

# Send the POST request with JSON payload
response = requests.post(url, json=data)

# Check if the response is successful
if response.status_code == 200:
    reviews = response.json()  # This will parse the JSON response into a Python list
    print("Scheduled Reviews:")
    for review in reviews:
        print(f"Review ID: {review['id']}, Date: {review['review_date']}")
else:
    print("Error:", response.status_code, response.text)
```

### 4. **Response Example**:

For the example request above, the response you would receive might look like this:

```json
[
    {
        "id": "review_12345",
        "review_date": "2024-12-01"
    },
    {
        "id": "review_67890",
        "review_date": "2024-11-15"
    }
]
```

You can process the JSON response in your program as needed, extracting the review dates and IDs for further use.

---

## Notes:
1. **Error Handling**: Make sure to handle potential errors such as network issues, invalid input data, and server errors (e.g., 500 Internal Server Error or 400 Bad Request).
2. **Database**: The server uses a local SQLite database (`reviews.db`) to store the review schedule. The schedule is updated each time a new review is added.
3. **Port and Host**: The Flask app runs on `localhost:5000` by default. If you change the host or port, update the `url` in the examples accordingly.

---

## Running the Microservice Locally

To run the microservice locally:

1. **Start the Server**:
   - Run `server.py` to start the socket-based backend server.
   - Ensure the database (`reviews.db`) is created and initialized.
   
   ```bash
   python server.py
   ```

2. **Start the Flask Web App**:
   - Run `app.py` to start the Flask web app.
   
   ```bash
   python app.py
   ```

The Flask app will be available at `http://127.0.0.1:5000/`.

---

## Additional Information

- The `server.py` is responsible for managing the review schedule and conflicts, while the Flask web app (`app.py`) handles HTTP requests and responses.
- If you need to modify the default behavior (such as the increment value or conflict handling), you can adjust the logic in `server.py`.




The following program has two input methods to schedule a forward looking review date based on the software developers requirements: 
    The first is a front-end app using VsCode Terminal where the user provides the id and increment date.
        This is accessed by running client.py in the VSCode terminal
    
    The second is a flask app where the user submits the id and increment date using a form. 
        This is the primary way of using the app based on the request of the developer. 



## UML Sequence Diagram
```plaintext
+--------------------+              +--------------------+            +-------------------------+
|    FlaskApp        |              |      Server        |            |   ReviewSchedule        |
+--------------------+              +--------------------+            +-------------------------+
| - app: Flask       |<>----------->| - HOST: str        |            | - id: int               |
| - HOST: str        |              | - PORT: int        |            | - review_id: str        |
| - PORT: int        |              +--------------------+            | - review_date: datetime |
+--------------------+              | + get_review_date()|            +-------------------------+
| + send_request()   |              | + check_for_conflict()|         |                         |
| + index()          |              | + handle_client_connection() |  |                         |
| + schedule()       |              | + start_server()    |           |                         |
+--------------------+              +--------------------+            +-------------------------+
        |                                 |                                |
        | Uses                            | Has-a                          | Uses
        |                                 |                                |
        V                                 V                                V
+-------------------------+      +------------------------+      +------------------------+
|    HTTPRequest          |      |    Engine (SQLite)     |      |  Session (SQLAlchemy)  |
+-------------------------+      +------------------------+      +------------------------+
| - form data (review_id) |      |  (SQLAlchemy Engine)   |      | (SQLAlchemy Session)   |
| - increment (optional)  |      +------------------------+      +------------------------+
+-------------------------+
```