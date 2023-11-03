from app.models import db, BlogPost, environment, SCHEMA
from sqlalchemy.sql import text


# Adds a demo user, you can add other users here if you want
def seed_blogposts():
    blogpost1 = BlogPost(
        employeeId=1,
        title='What Is Salt Therapy?',
        blog='So what’s the big deal about Salt Therapy? You have probably heard about it or maybe your friend brought it up in conversation once, but you don’t know exactly what it is. Let’s take it back to a couple of centuries ago when a doctor by the name of Feliks Boczkowski discovered that miners in the salt mines in eastern Europe, specifically, Poland didn’t have lung issues like workers in other mines. Because of Dr. Boczkowski’s discovery, we can thank him for today’s therapeutic salt rooms. He believed that salt has a great healing power, bringing lots of benefits and is the foundation of the growing wellness trend of halotherapy, or salt therapy. There are countless claims of how salt therapy rooms have helped people with a variety of breathing issues or infections they are experiencing, although there is not a mountain of evidence to support these claims. People still come out of salt rooms claiming there is a difference and that it has improved their overall well-being.',
    )
    blogpost2 = BlogPost(
        employeeId=2,
        title='THE SCIENCE OF FILLERS: WHY EXPERIENCE MATTERS?',
        blog='See a wrinkle, you might think fillers. And you could be right. However, you might also be surprised at just how a gifted injector will use fillers to treat all kinds of facial imperfections. For instance, if you have jowls that are bothering you, filler treatments in the cheek could be the answer. In fact, injections in the jowls might be counterproductive and leave you very disappointed. Filling the cheeks could do the trick to correct the sagging in the lower face.\n\nThis type of work is called anatomic filling. Replacing volume loss with injectable products like Juvederm, and Voluma can restore youthfulness to the face. It\'s very important that you choose an injector who can see wrinkles and sagging skin in tandem and not in isolation. These practitioners understand how volume loss affects the surrounding skin, and they treat the entire face (not holistically) to restore balance, symmetry and volume.',
    )

    db.session.add(blogpost1)
    db.session.add(blogpost2)
    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_blogposts():
    if environment == "production":
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.blogposts RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM blogposts"))

    db.session.commit()
