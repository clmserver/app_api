from apps import app
from views import app_user
from flask_cors import CORS

APP_CONFIG={
    'host': 'localhost',
    'port': 8002,
    'debug': True
}

if __name__ == '__main__':
    CORS().init_app(app)
    app.register_blueprint(app_user.blue)

    app.run(**APP_CONFIG)