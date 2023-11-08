from flask import Blueprint, jsonify, request
from app.models import Image, db
from app.forms import ImageForm
from flask_login import current_user, login_required
from .auth_routes import validation_errors_to_error_messages


image_routes = Blueprint('images', __name__)


@image_routes.route('')
def all_images():
    images = Image.query.all()
    if not images:
        return {'error': 'No images found'}, 404
    return {'images': [image.to_dict() for image in images]}


@image_routes.route('/<int:imageId>')
def get_one_image(imageId):
    image = Image.query.filter(Image.id == imageId).first()
    if not image:
        return {'error': 'Image not found'}, 404

    return image.to_dict()


@image_routes.route('', methods=['POST'])
@login_required
def create_image():
    if not current_user.is_owner:
        return {'error': 'Only the owner can create a new image'}, 403

    form = ImageForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        data = form.data
        new_image = Image(
            name=data['name'],
            imageFile=data['imageFile'],
        )

        db.session.add(new_image)
        db.session.commit()
        return new_image.to_dict()

    else:
        return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@image_routes.route('/<int:imageId>', methods=['PUT'])
@login_required
def edit_image(imageId):
    image = Image.query.filter(Image.id == imageId).first()
    if not image:
        return {'error': 'Image not found'}, 404
    if not current_user.is_owner:
        return {'error': 'Only the owner can edit a image'}, 403

    form = ImageForm(obj=image)
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        data = form.data
        image.name = data['name'],
        image.imageUrl = data['imageUrl'],

        db.session.commit()
        return image.to_dict()

    else:
        return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@image_routes.route('/<int:imageId>', methods=['DELETE'])
@login_required
def delete_image(imageId):
    image = Image.query.filter(Image.id == imageId).first()
    if not image:
        return {'error': 'Image not found'}, 404
    if not current_user.is_owner:
        return {'error': 'Only the owner can delete a image'}, 403

    db.session.delete(image)
    db.session.commit()
    return {'message': 'Image successfully deleted'}
