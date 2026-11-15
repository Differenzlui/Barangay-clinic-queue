from flask import Flask, jsonify, request

app = Flask(__name__)

# Shared in-memory data store for the barangay clinic queue
queue = [
    {
     "queue_number": 1, 
     "patient_name": "Kris Guevarra", 
     "status": "waiting"
    },
    {
     "queue_number": 2, 
     "patient_name": "Lhei Dayrit", 
     "status": "in_consultation"
    }
]

# --- ADD ENDPOINTS BELOW ---
# Member 1: GET /queue & POST /queue
# Member 2: GET /queue/<int:queue_number> & PUT /queue/<int:queue_number>
# Member 3: DELETE /queue/<int:queue_number>
@app.route('/queue/<int:queue_number>', methods=['DELETE'])
def delete_patient(queue_number):
    global queue
    patient = next((p for p in queue if p['queue_number'] == queue_number), None)
    if not patient:
        return jsonify({"error": f"Patient with queue number {queue_number} not found"}), 404
    
    queue = [p for p in queue if p['queue_number'] != queue_number]
    return jsonify({"message": f"Queue number {queue_number} removed successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)