from app.models.db import db, environment, SCHEMA
from .images_seed import seed_images, undo_images
from .blogposts_seed import seed_blogposts, undo_blogposts
from .company_seed import seed_company, undo_company
from .reviews_seed import seed_reviews, undo_reviews
from .services_seed import seed_services, undo_services
from flask.cli import AppGroup
from .users_seed import seed_users, undo_users
from .staff_seed import seed_staff, undo_staff


# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')


# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    if environment == 'production':
        # Before seeding in production, you want to run the seed undo
        # command, which will  truncate all tables prefixed with
        # the schema name (see comment in users.py undo_users function).
        # Make sure to add all your other model's undo functions below
        undo_users()
        undo_staff()
        undo_company()
        undo_services()
        undo_reviews()
        undo_blogposts()
        undo_images()

        db.session.execute(
            f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.staffs RESTART IDENTITY CASCADE;")
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.companies RESTART IDENTITY CASCADE;")
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.services RESTART IDENTITY CASCADE;")
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.reviews RESTART IDENTITY CASCADE;")
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.blogposts RESTART IDENTITY CASCADE;")
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.images RESTART IDENTITY CASCADE;")

        db.session.commit()

    seed_users()
    seed_staff()
    seed_company()
    seed_services()
    seed_reviews()
    seed_blogposts()
    seed_images()
    # Add other seed functions here


# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    undo_users()
    undo_staff()
    undo_company()
    undo_services()
    undo_reviews()
    undo_blogposts()
    undo_images()
    # Add other undo functions here
