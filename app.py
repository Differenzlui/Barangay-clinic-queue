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
@app.route('/queue/<int:queue_number>', methods=['GET'])
def get_patient(queue_number):
    patient = next((p for p in queue if p['queue_number'] == queue_number), None)
    if not patient:
        return jsonify({"error": f"Patient with queue number {queue_number} not found"}), 404
    return jsonify(patient), 200

@app.route('/queue/<int:queue_number>', methods=['PUT'])
def update_patient(queue_number):
    patient = next((p for p in queue if p['queue_number'] == queue_number), None)
    if not patient:
        return jsonify({"error": f"Patient with queue number {queue_number} not found"}), 404
    
    data = request.get_json()
    valid_statuses = ["waiting", "in_consultation", "completed"]
    if not data or data.get('status') not in valid_statuses:
        return jsonify({"error": f"Invalid status. Must be one of: {valid_statuses}"}), 400
    
    patient['status'] = data['status']
    return jsonify(patient), 200
# Member 3: DELETE /queue/<int:queue_number>

if __name__ == "__main__":
    app.run(debug=True)