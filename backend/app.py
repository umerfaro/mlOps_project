from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import os
import pickle
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS properly
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# MongoDB Configuration
app.config["MONGO_URI"] = os.getenv("MONGODB_URI", "mongodb://localhost:27017/weather_app")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "your-secret-key")

mongo = PyMongo(app)
jwt = JWTManager(app)

# Load the trained model
try:
    with open('models/model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Authentication routes
@app.route("/api/auth/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        
        # Check if user already exists
        if mongo.db.users.find_one({"email": data["email"]}):
            return jsonify({"message": "Email already registered"}), 400
        
        # Hash password and create user
        hashed_password = generate_password_hash(data["password"])
        mongo.db.users.insert_one({
            "email": data["email"],
            "password": hashed_password
        })
        
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/auth/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        user = mongo.db.users.find_one({"email": data["email"]})
        
        if user and check_password_hash(user["password"], data["password"]):
            token = create_access_token(identity=str(user["_id"]))
            return jsonify({"token": token}), 200
        
        return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Weather prediction route
@app.route("/api/weather/predict", methods=["POST"])
@jwt_required()
def predict_weather():
    try:
        if model is None:
            return jsonify({"error": "Model not loaded"}), 500
            
        data = request.get_json()
        
        # Get input features
        humidity = float(data.get('humidity'))
        wind_speed = float(data.get('wind_speed'))
        
        # Validate input ranges
        if not (0 <= humidity <= 100):
            return jsonify({"error": "Humidity must be between 0 and 100"}), 400
        if wind_speed < 0:
            return jsonify({"error": "Wind speed cannot be negative"}), 400
            
        # Make prediction using the trained model
        features = [[humidity, wind_speed]]
        predicted_temp = model.predict(features)[0]
        
        # Prepare response
        prediction = {
            "temperature": float(predicted_temp),
            "humidity": humidity,
            "wind_speed": wind_speed
        }
        
        # Save prediction to MongoDB
        mongo.db.predictions.insert_one({
            "user_id": get_jwt_identity(),
            "features": {
                "humidity": humidity,
                "wind_speed": wind_speed
            },
            "predicted_temperature": float(predicted_temp),
            "timestamp": datetime.now()
        })
        
        return jsonify(prediction)
        
    except ValueError as e:
        return jsonify({"error": "Invalid input values. Please provide valid numbers."}), 400
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({"error": str(e)}), 500

# Get prediction history
@app.route("/api/weather/history", methods=["GET"])
@jwt_required()
def get_prediction_history():
    try:
        user_id = get_jwt_identity()
        predictions = list(mongo.db.predictions.find(
            {"user_id": user_id},
            {"_id": 0, "user_id": 0}
        ).sort("timestamp", -1))
        
        return jsonify(predictions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Health check route
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    if model is None:
        print("Warning: Model not loaded. Predictions will not work!")
    app.run(debug=True)