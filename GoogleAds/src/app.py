from flask import Flask
from controllers.campaign_controller import campaign_bp
from controllers.customer_metrics_controller import customer_metrics_bp
from controllers.keywords_controller import all_keywords_bp
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Register Blueprints
app.register_blueprint(campaign_bp)
app.register_blueprint(customer_metrics_bp)
app.register_blueprint(all_keywords_bp)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5001)