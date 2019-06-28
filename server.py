from apps import app
from views import app_user, home_views, pay_vip, vip_view
from flask_cors import CORS

APP_CONFIG={
    'host': '0.0.0.0',
    'port': 8002,
    'debug': True
}

if __name__ == '__main__':
    CORS().init_app(app)
    app.register_blueprint(app_user.blue)
    app.register_blueprint(home_views.main_blue)
    app.register_blueprint(pay_vip.blue)
    app.register_blueprint(vip_view.blue)

    app.run(**APP_CONFIG)
