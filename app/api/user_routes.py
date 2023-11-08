from flask import Blueprint, jsonify
from flask_login import login_required
from app.models import User, Review, Appointment

user_routes = Blueprint('users', __name__)


@user_routes.route('')
@login_required
def users():
    users = User.query.all()
    if not users:
        {'error': 'No users found'}, 404
    return {'users': [user.to_dict() for user in users]}


@user_routes.route('/<int:userId>')
@login_required
def get_one_user(userId):
    user = User.query.get(userId)
    if not user:
        return {'error': 'User does not exist'}, 404
    return user.to_dict()


@user_routes.route('/<int:userId>/reviews')
@login_required
def get_reviews_by_user(userId):
    reviews = Review.query.filter(Review.userId == userId).all()
    if not reviews:
        return {'error': 'User does not have any reviews'}, 404

    review_list = [review.to_dict() for review in reviews]

    return {'user reviews': review_list}


@user_routes.route('/<int:userId>/appointments')
@login_required
def get_appointments_by_user(userId):
    appointments = Appointment.query.filter(Appointment.userId == userId).all()
    if not appointments:
        return {'error': 'User does not have any appointments'}, 404

    appointment_list = [appointment.to_dict() for appointment in appointments]

    return {'user appointments': appointment_list}
