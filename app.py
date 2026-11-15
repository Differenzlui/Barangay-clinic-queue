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
@app.route('/queue', methods=['GET'])
def get_queue():
    if not queue:
        return jsonify({"error": "The clinic queue is currently empty"}), 404
    return jsonify({"queue": queue}), 200

@app.route('/queue', methods=['POST'])
def add_patient():
    data = request.get_json()
    if not data or not data.get('patient_name', '').strip():
        return jsonify({"error": "patient_name is required"}), 400
    
    # Auto-increment queue_number based on the highest existing number
    next_number = max((p['queue_number'] for p in queue), default=0) + 1
    
    new_patient = {
        "queue_number": next_number,
        "patient_name": data['patient_name'].strip(),
        "status": "waiting"
    }
    queue.append(new_patient)
    return jsonify(new_patient), 201
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