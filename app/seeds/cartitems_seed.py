from app.models import db, CartItem, environment, SCHEMA
from sqlalchemy.sql import text


# Adds a demo user, you can add other users here if you want
def seed_cart_items():
    cartItem1 = CartItem(
        cartId=1,
        serviceId=4,
        quantity=1,
        price=300,
        serviceTotal=300
    )
    cartItem2 = CartItem(
        cartId=1,
        serviceId=5,
        quantity=1,
        price=300,
        serviceTotal=300
    )
    cartItem3 = CartItem(
        cartId=1,
        serviceId=6,
        quantity=1,
        price=300,
        serviceTotal=300
    )

    db.session.add(cartItem1)
    db.session.add(cartItem2)
    db.session.add(cartItem3)
    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_cart_items():
    if environment == "production":
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.cartitems RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM cartitems"))

    db.session.commit()