from flask import Flask, jsonify, request, abort
import uuid

app = Flask(__name__)

# Dictionary to store mobile phone details
mobile_phones = {}

# Helper function to generate a random ID
def generate_id():
    return str(uuid.uuid4())

# Populate the dictionary with 10 sample mobile phones
for _ in range(10):
    phone_id = generate_id()
    mobile_phones[phone_id] = {
        "name": f"Phone {len(mobile_phones) + 1}",
        "companyname": f"Company {len(mobile_phones) + 1}",
        "price": 500 + (len(mobile_phones) * 50),
        "year_of_manufacture": 2020 + len(mobile_phones),
        "os": "Android" if len(mobile_phones) % 2 == 0 else "iOS"
    }

# Endpoint to get all mobile phone details
@app.route('/phones', methods=['GET'])
def get_all_phones():
    return jsonify(mobile_phones)

# Endpoint to get details of a specific mobile phone by ID
@app.route('/phones/<string:phone_id>', methods=['GET'])
def get_phone(phone_id):
    if phone_id not in mobile_phones:
        abort(404, description="Phone not found")
    return jsonify(mobile_phones[phone_id])

# Endpoint to add a new mobile phone
@app.route('/phones', methods=['POST'])
def add_phone():
    new_phone = request.json
    if not new_phone or not all(key in new_phone for key in ["name", "companyname", "price", "year_of_manufacture", "os"]):
        abort(400, description="Invalid input: Missing required fields")
    
    phone_id = generate_id()
    mobile_phones[phone_id] = new_phone
    return jsonify({"message": "Phone added successfully", "phone_id": phone_id}), 201

# Endpoint to delete a mobile phone by ID
@app.route('/phones/<string:phone_id>', methods=['DELETE'])
def delete_phone(phone_id):
    if phone_id not in mobile_phones:
        abort(404, description="Phone not found")
    
    del mobile_phones[phone_id]
    return jsonify({"message": "Phone deleted successfully"}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=2080)

