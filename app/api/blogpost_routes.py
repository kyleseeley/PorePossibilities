from flask import Blueprint, jsonify, request
from app.models import BlogPost, Staff, User, Cart, Company, Service, db
from app.forms import BlogPostForm
from flask_login import current_user, login_required
from .auth_routes import validation_errors_to_error_messages


blogpost_routes = Blueprint('blogposts', __name__)


@blogpost_routes.route('/')
def all_blogposts():
    blogposts = BlogPost.query.all()
    return {'blogposts': [blogpost.to_dict() for blogpost in blogposts]}


@blogpost_routes.route('/<int:blogpostId>')
def get_one_blogpost(blogpostId):
    blogpost = BlogPost.query.filter(BlogPost.id == blogpostId).first()
    if not blogpost:
        return {'error': 'Blogpost not found'}, 404

    return blogpost.to_dict()


@blogpost_routes.route('/', methods=['POST'])
@login_required
def post_blogpost():
    if not current_user.authorized:
        return {'error': 'Only the authorized staff can create a new blogpost'}, 403

    form = BlogPostForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        data = form.data
        new_blogpost = BlogPost(
            staffId=data['staffId'],
            title=data['title'],
            blog=data['blog'],
        )

        db.session.add(new_blogpost)
        db.session.commit()
        return new_blogpost.to_dict()

    else:
        return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@blogpost_routes.route('/<int:<blogpostId>', methods=['PUT'])
@login_required
def edit_blogpost(blogpostId):
    blogpost = BlogPost.query.filter(BlogPost.id == blogpostId).first()
    if not blogpost:
        return {'error': 'Blogpost not found'}, 404
    if not current_user.authorized:
        return {'error': 'Only the authorized staff can edit a blogpost'}, 403

    form = BlogPostForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        data = form.data
        blogpost.staffId = data['staffId'],
        blogpost.title = data['title'],
        blogpost.blog = data['blog'],

        db.session.commit()
        return blogpost.to_dict()

    else:
        return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@blogpost_routes.route('/<int:blogpostId>', methods=['DELETE'])
@login_required
def delete_blogpost(blogpostId):
    blogpost = BlogPost.query.filter(BlogPost.id == blogpostId).first()
    if not blogpost:
        return {'error': 'Blogpost not found'}, 404
    if not current_user.authorized:
        return {'error': 'Only authorized staff can delete a blogpost'}, 403

    db.session.delete(blogpost)
    return {'message': 'Blogpost successfully deleted'}
