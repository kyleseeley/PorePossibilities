from flask import Blueprint, jsonify, request
from app.models import Review, Company, db
from app.forms.review_form import ReviewForm
from flask_login import current_user, login_required
from .auth_routes import validation_errors_to_error_messages


review_routes = Blueprint('reviews', __name__)


@review_routes.route('/<int:reviewId>')
def get_one_review(reviewId):
    review = Review.query.filter(Review.id == reviewId)

    if not review:
        return {'message': 'No reviews found'}, 404

    return review.to_dict()


@review_routes.route('/<int:reviewId>', methods=['PUT'])
@login_required
def edit_review(reviewId):
    review = Review.query.get(reviewId)

    if review is None:
        return {'error': 'Review not found'}, 404
    if review.userId != current_user.id:
        return {'error': 'User does not have permission to edit this review'}, 404

    form = ReviewForm(obj=review)

    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        data = form.data
        review.review = data['review']
        review.stars = data['stars']

        db.session.commit()

        reviews = Review.query.filter(Review.company == review.company).all()

        total_stars = sum(review.stars for review in reviews)
        average_rating = total_stars / len(reviews) if len(reviews) > 0 else 0

        company = review.company
        company.starRating = average_rating

        db.session.commit()

        return review.to_dict()
    else:
        return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@review_routes.route('/<int:reviewId>', methods=['DELETE'])
@login_required
def delete_review(reviewId):
    review = Review.query.get(reviewId)

    if review is None:
        return {'error': 'Review not found'}, 404

    if review.userId != current_user.id:
        return {'error': 'User does not have permission to delete this review'}, 403

    company = Company.query.get(review.company)

    db.session.delete(review)
    db.session.commit()

    reviews = Review.query.filter_by(company=company.id).all()
    num_reviews = len(reviews)
    total_stars = sum(review.stars for review in reviews)
    avg_rating = total_stars / num_reviews if num_reviews > 0 else 0

    # Update the restaurant record with the new numReviews and starRating
    company.numReviews = num_reviews
    company.starRating = avg_rating

    db.session.commit()

    return {'message': 'Review deleted successfully'}
