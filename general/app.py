import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from request_logging import register_request_logging
from routes.posts import posts_bp
from routes.api import api_bp


def create_app():
    load_dotenv(Path(__file__).with_name(".env"))
    app = Flask(__name__)
    app.json.ensure_ascii = False
    app.register_blueprint(posts_bp)
    app.register_blueprint(api_bp)
    register_request_logging(app)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5100")))
