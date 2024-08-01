from flask_cors import CORS
from hexagon.http.cache_config import configure_no_caching


def default_setup(app):
    app.config['CORS_SUPPORTS_CREDENTIALS'] = True
    if 'CORS_ORIGINS' not in app.config:
        app.config['CORS_ORIGINS'] = [
            "http://localhost",
            "http://localhost:80",
            "http://localhost:5173",
            "http://localhost:8080",
        ]
    CORS(app)
    configure_no_caching(app)
    return app
