from flask import Flask, jsonify, request

app = Flask(__name__)

# Shared in-memory data store for the barangay clinic queue
queue = [
    {
        "queue_number": 1, 
        "patient_name": "Kris Guevarra", 
        "status": "waiting"
    }
]

# --- ADD ENDPOINTS BELOW ---
# Member 1: GET /queue & POST /queue
# Member 2: GET /queue/<int:queue_number> & PUT /queue/<int:queue_number>
# Member 3: DELETE /queue/<int:queue_number>

if __name__ == "__main__":
    app.run(debug=True)