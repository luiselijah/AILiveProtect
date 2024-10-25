from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample in-memory database for demonstration purposes
transaction_history = {}
alerts = {}


# Root endpoint
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Fraud Detection API!"}), 200


# Endpoint to analyze a transaction
@app.route('/api/v1/transaction/analyze', methods=['POST'])
def analyze_transaction():
    data = request.json
    transaction_id = data.get("transaction_id")
    amount = data.get("amount")

    # Simple mock fraud detection logic
    fraud_score = min(amount / 10000.0, 1.0)  # Example: larger amounts have higher fraud scores
    risk_level = "Low" if fraud_score < 0.3 else "Medium" if fraud_score < 0.7 else "High"
    recommendation = "Accept" if risk_level == "Low" else "Review" if risk_level == "Medium" else "Decline"

    # Store the transaction in the history
    account_id = data.get("account_id")
    if account_id not in transaction_history:
        transaction_history[account_id] = []
    transaction_history[account_id].append({
        "transaction_id": transaction_id,
        "amount": amount,
        "timestamp": data.get("timestamp"),
        "location": data.get("location"),
        "risk_level": risk_level
    })

    response = {
        "transaction_id": transaction_id,
        "fraud_score": fraud_score,
        "risk_level": risk_level,
        "recommendation": recommendation
    }
    return jsonify(response), 200


# Endpoint to create an alert
@app.route('/api/v1/alerts', methods=['POST'])
def create_alert():
    data = request.json
    alert_id = data.get("alert_id")
    transaction_id = data.get("transaction_id")
    risk_level = data.get("risk_level")

    # Add alert to the in-memory database
    alerts[alert_id] = {
        "transaction_id": transaction_id,
        "risk_level": risk_level,
        "description": data.get("description"),
        "timestamp": data.get("timestamp"),
        "status": "Under Review"
    }

    response = {
        "alert_id": alert_id,
        "status": alerts[alert_id]["status"]
    }
    return jsonify(response), 201


# Endpoint to get transaction history for an account
@app.route('/api/v1/transaction/history/<account_id>', methods=['GET'])
def get_transaction_history(account_id):
    if account_id in transaction_history:
        response = {
            "account_id": account_id,
            "transactions": transaction_history[account_id]
        }
        return jsonify(response), 200
    else:
        return jsonify({"error": "Account not found"}), 404


# Run the application
if __name__ == '__main__':
    app.run(debug=True)

