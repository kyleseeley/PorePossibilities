import os
from flask import Flask, render_template, request, session, redirect
from flask_cors import CORS
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_login import LoginManager
from .models import db, User, Employee
from .api.user_routes import user_routes
from .api.auth_routes import auth_routes
from .api.review_routes import review_routes
from .api.company_routes import company_routes
from .api.service_routes import service_routes
from .api.appointment_routes import appointment_routes
from .api.blogpost_routes import blogPost_routes
from .api.employee_routes import employee_routes
from .api.cart_routes import cart_routes
from .api.session_routes import session_routes
from .api.cartitem_routes import cartItem_routes
from .seeds import seed_commands
from .config import Config

app = Flask(__name__, static_folder='../react-app/build', static_url_path='/')

# Setup login manager
login = LoginManager(app)
login.login_view = 'auth.unauthorized'


@login.user_loader
def load_user(id):
    user_type = session.get('user_type')

    if user_type == 'user':
        return User.query.get(int(id))
    elif user_type == 'employee':
        return Employee.query.get(int(id))


# Tell flask about our seed commands
app.cli.add_command(seed_commands)

app.config.from_object(Config)
app.register_blueprint(user_routes, url_prefix='/api/users')
app.register_blueprint(auth_routes, url_prefix='/api/auth')
app.register_blueprint(review_routes, url_prefix='/api/reviews')
app.register_blueprint(company_routes, url_prefix='/api/companies')
app.register_blueprint(service_routes, url_prefix='/api/services')
app.register_blueprint(appointment_routes, url_prefix='/api/appointments')
app.register_blueprint(blogPost_routes, url_prefix='/api/blogposts')
app.register_blueprint(employee_routes, url_prefix='/api/employees')
app.register_blueprint(cart_routes, url_prefix='/api/cart')
app.register_blueprint(session_routes, url_prefix='/api/session')
app.register_blueprint(cartItem_routes, url_prefix='/api/cartitems')
db.init_app(app)
Migrate(app, db)

# Application Security
CORS(app)


# Since we are deploying with Docker and Flask,
# we won't be using a buildpack when we deploy to Heroku.
# Therefore, we need to make sure that in production any
# request made over http is redirected to https.
# Well.........
@app.before_request
def https_redirect():
    if os.environ.get('FLASK_ENV') == 'production':
        if request.headers.get('X-Forwarded-Proto') == 'http':
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)


@app.after_request
def inject_csrf_token(response):
    response.set_cookie(
        'csrf_token',
        generate_csrf(),
        secure=True if os.environ.get('FLASK_ENV') == 'production' else False,
        samesite='Strict' if os.environ.get(
            'FLASK_ENV') == 'production' else None,
        httponly=True)
    return response


@app.route("/api/docs")
def api_help():
    """
    Returns all API routes and their doc strings
    """
    acceptable_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    route_list = {rule.rule: [[method for method in rule.methods if method in acceptable_methods],
                              app.view_functions[rule.endpoint].__doc__]
                  for rule in app.url_map.iter_rules() if rule.endpoint != 'static'}
    return route_list


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def react_root(path):
    """
    This route will direct to the public directory in our
    react builds in the production environment for favicon
    or index.html requests
    """
    if path == 'favicon.ico':
        return app.send_from_directory('public', 'favicon.ico')
    return app.send_static_file('index.html')


@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')
