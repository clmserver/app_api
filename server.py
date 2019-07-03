from apps import app

from views import user_view, home_view, payvip_view, vip_view, shop_view, user_features_view, user_features_view
from flask_cors import CORS

APP_CONFIG={
    'host': '0.0.0.0',
    'port': 8002,
    'debug': True
}

if __name__ == '__main__':
    CORS().init_app(app)

    app.register_blueprint(user_view.blue)
    app.register_blueprint(home_view.main_blue)
    app.register_blueprint(payvip_view.blue)
    app.register_blueprint(vip_view.blue)
    app.register_blueprint(shop_view.shop_blue)
    app.register_blueprint(user_features_view.blue)
    app.register_blueprint(user_features_view.blue)

    app.run(**APP_CONFIG)
