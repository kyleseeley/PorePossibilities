from flask import Blueprint, jsonify
from flask_login import login_required
from app.models import User, Review

user_routes = Blueprint('users', __name__)


@user_routes.route('/')
@login_required
def users():
    """
    Query for all users and returns them in a list of user dictionaries
    """
    users = User.query.all()
    return {'users': [user.to_dict() for user in users]}


@user_routes.route('/<int:userId>')
@login_required
def user(userId):
    """
    Query for a user by id and returns that user in a dictionary
    """
    user = User.query.get(id)
    if not user:
        return {"error": "User does not exist"}
    return user.to_dict()


@user_routes.route('/<int:userId>/reviews')
@login_required
def get_user_reviews(userId):
    reviews = Review.query.filter(Review.userId == userId).all()
    if not reviews:
        return {"error": "User does not have any reviews"}, 404

    review_list = [review.to_dict() for review in reviews]

    return jsonify({'reviews': review_list})
