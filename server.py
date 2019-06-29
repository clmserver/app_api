from apps import app
from views import app_user, home_view, pay_vip, shop_view
from views import app_user, home_view
from flask_cors import CORS

APP_CONFIG={
    'host': '0.0.0.0',
    'port': 8002,
    'debug': True
}

if __name__ == '__main__':
    CORS().init_app(app)
    app.register_blueprint(app_user.blue)
    app.register_blueprint(home_view.main_blue)
    app.register_blueprint(pay_vip.blue)
    app.register_blueprint(shop_view.shop_blue)

    app.run(**APP_CONFIG)
