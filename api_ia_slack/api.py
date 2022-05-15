from app import app
from routes import message_to_slack


app.register_blueprint(message_to_slack)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5004)