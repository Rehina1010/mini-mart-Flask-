import os
from flask import Flask
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_admin import Admin
from dotenv import load_dotenv
from src.db import db
from src.entity.models import User, Product, ProductImage

load_dotenv()

app = Flask(__name__, static_url_path='', static_folder='src/static', template_folder='src/templates')

app.config['SECRET_KEY'] = os.getenv('SESSION_SECRET_KEY')
app.config['SECURITY_PASSWORD_SALT'] = os.urandom(16).hex()

app.config['STRIPE_PUBLIC_KEY'] = os.getenv('STRIPE_PUBLIC_KEY')
app.config['STRIPE_SECRET_KEY'] = os.getenv('STRIPE_SECRET_KEY')

app.config['BASE_URL'] = os.getenv('BASE_URL', 'http://127.0.0.1:5000')

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"

admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
app.config['MAIL_DEBUG'] = True

mail = Mail(app)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from src.routes.auth import bp as auth_bp
from src.routes.main import bp as main_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(main_bp)


class ProductView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    column_list = ('id', 'name', 'description', 'price', 'main_image', 'additional_images')


admin.add_view(ProductView(Product, db.session))


class ProductImageView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    column_list = ('id', 'image_name', 'image_url', 'product_id')


admin.add_view(ProductImageView(ProductImage, db.session))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
