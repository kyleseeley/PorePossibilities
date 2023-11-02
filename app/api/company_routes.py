from flask import Blueprint, jsonify, request
from app.models import Review, Company, db
from app.forms import CompanyForm
from flask_login import current_user, login_required
from .auth_routes import validation_errors_to_error_messages


company_routes = Blueprint('companies', __name__, url_prefix="")


@company_routes.route("/")
def all_companies():
    companies = Company.query.all()
    return {'companies': [company.to_dict() for company in companies]}


@company_routes.route("/<int:companyId>")
def get_one_company(companyId):
    company = Company.query.filter(Company.id == companyId).first()
    if not company:
        return {'error': 'Company not found'}, 404

    return company.to_dict()


@company_routes.route("/", methods=['POST'])
@login_required
def post_company():
    if not current_user.is_owner:
        return {'error': 'Only the owner can create a new company'}, 403

    form = CompanyForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        data = form.data
        new_company = Company(
            ownerId=current_user.id,
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            address=data['address'],
            city=data['city'],
            state=data['state'],
            zipCode=data['zipCode'],
        )

        db.session.add(new_company)
        db.session.commit()
        return new_company.to_dict()

    else:
        return {'errors': validation_errors_to_error_messages(form.errors)}, 401
