from flask import Blueprint, jsonify, request
from app.models import Review, Company, db
from flask_login import current_user, login_required
from .auth_routes import validation_errors_to_error_messages


company_routes = Blueprint('companies', __name__, url_prefix="")


@company_routes.route("/")
def all_companies():
    companies = Company.query.all()
    return {'companies': [company.to_dict() for company in companies]}


# @company_routes.route("/")
