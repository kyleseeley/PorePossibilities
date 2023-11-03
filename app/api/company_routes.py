from flask import Blueprint, jsonify, request
from app.models import Review, Staff, User, Cart, Company, Service, db
from app.forms import CompanyForm, ReviewForm
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


@company_routes.route("/", methods=['PUT'])
@login_required
def update_company(companyId):
    company = Company.query.filter(Company.id == companyId).first()
    if not company:
        return {'error': 'Company not found'}, 404
    if not current_user.is_owner:
        return {'error': 'Only the owner can update a company'}, 403

    form = CompanyForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        data = form.data
        company.ownerId = current_user.id,
        company.name = data['name'],
        company.email = data['email'],
        company.phone = data['phone'],
        company.address = data['address'],
        company.city = data['city'],
        company.state = data['state'],
        company.zipCode = data['zipCode'],

        db.session.commit()
        return company.to_dict()

    else:
        return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@company_routes.route("/<int:companyId>", methods=['DELETE'])
@login_required
def delete_company(companyId):
    company = Company.query.filter(Company.id == companyId).first()
    if not company:
        return {'error': 'Company not found'}, 404
    if not current_user.is_owner:
        return {'error': 'Only the owner can delete a company'}, 403

    db.session.delete(company)
    return {'message': 'Company successfully deleted'}


@company_routes.route("/<int:companyId>/reviews")
def company_reviews(companyId):
    company = Company.query.filter(Company.id == companyId).first()

    if company is None:
        return {'error': 'Company not found'}

    reviews = (
        db.session.query(Review, User)
        .join(User, User.id == Review.userId)
        .filter(Review.companyId == companyId)
        .all()
    )

    if not reviews:
        return {"message": "This company has no reviews."}

    reviews_data = [
        {
            "id": review.id,
            "userId": user.id,
            "companyId": review.companyId,
            "review": review.review,
            "stars": review.stars,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "createdAt": review.createdAt
        }
        for review, user in reviews
    ]

    return {'reviews': reviews_data}


@company_routes.route("/<int:companyId>/reviews", methods=['POST'])
@login_required
def post_review(companyId):
    company = Company.query.filter(Company.id == companyId).first()
    if not company:
        return {"error": "Restaurant does not exist!"}, 404
    if isinstance(current_user, Staff):
        return {"error": "Staff members cannot post reviews."}, 403

    existing_review = Review.query.filter(
        Review.companyId == companyId, Review.userId == current_user.id).first()
    if existing_review:
        return {"error": "You already have a review for this company."}, 403
    form = ReviewForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        data = form.data

        new_review = Review(
            userId=current_user.id,
            companyId=companyId,
            review=data["review"],
            stars=data["stars"]
        )

        db.session.add(new_review)
        db.session.commit()

        # Updating restaurant rating and number of reviews
        companyReviews = Review.query.filter(
            Review.companyId == companyId).all()
        company.numReviews += 1
        totalRating = sum(review.stars for review in companyReviews)
        company.starRating = round(totalRating / company.numReviews, 1)

        db.session.commit()

        return new_review.to_dict()
    else:
        return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@company_routes.route('/<int:companyId>/shopping-cart', methods=['POST'])
@login_required
def post_shoppingCart(companyId):
    cart = current_user.get_cart(companyId)
    if cart:
        return cart.to_dict()

    user = User.query.filter(User.id == current_user.id).first()
    if not user:
        return {"error": "User not found"}

    service_id = request.json.get('service_id')
    quantity = request.json.get('quantity')
    if service_id is None or quantity is None:
        return {"error": "Both 'service_id' and 'quantity' must be provided in the request"}

    service = Service.query.get(service_id)

    if service is None:
        return {"error": "Service not found"}

    new_cart = Cart(
        userId=current_user.id,
        companyId=companyId,
        serviceId=service.id,
        quantity=quantity,
        serviceTotal=service.price * quantity,
    )
    db.session.add(new_cart)
    db.session.commit()

    cart_items = Cart.query.filter_by(
        userId=current_user.id, companyId=companyId).all()
    total = sum(cart_item.service.price *
                cart_item.quantity for cart_item in cart_items)
    cart.cartTotal = total
    db.session.commit()

    return new_cart.to_dict()
