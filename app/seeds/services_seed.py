from app.models import db, Service, environment, SCHEMA
from sqlalchemy.sql import text


# Adds a demo user, you can add other users here if you want
def seed_services():
    consultation = Service(
        type='Consultation',
        name='Consultation',
        price=0,
        description='Let\'s chat! After getting better acquainted with you and your skin health goals, we will educate you on the best treatments and skin care. We will get you on a skin health plan that will work with your goals, schedule, and budget. This appointment is complimentary.',
        duration=30)
    signature = Service(
        type='Skincare Treatments',
        name='Pore Possibilities Signature',
        price=160,
        description='Gentle extractions clarify the skin while specialized, focused lift + tone massage to detoxify and leave skin sculpted. Custom blended treatment masks leave the skin radiant, smooth, and bright.',
        duration=60)
    botanicalBeaute = Service(
        type='Skincare Treatments',
        name='Botanical Beautē',
        price=160,
        description='Treat your skin with the purest, organic & clean ingredients, handpicked to cater to your unique skin. This results-oriented facial harnesses the power of organic botanicals to deeply cleanse, nourish, and revitalize your skin, leaving it glowing from within.',
        duration=60)
    oxytheore = Service(
        type='Skincare Treatments',
        name='Oxytheorē',
        price=200,
        description='This innovative treatment does it all. OxyTheorē harnesses the power of oxygen to create transformation within the skin and delivers instant results that you can see and feel.',
        duration=60)
    nanoglow = Service(
        type='Skincare Treatments',
        name='Nanoglow',
        price=200,
        description='Experience the cutting-edge of skincare with our revolutionary Nanoneedling Infusion. This advanced treatment takes your skin restoration journey to new heights, leaving you with a complexion that is hydrated, bright, and irresistibly smooth, aka Glass Skin.',
        duration=75)
    everythingLaser = Service(
        type='Advanced Skincare Treatments',
        name='Everything Laser',
        price=300,
        description='This no-downtime laser facial is nothing short of an aesthetic treatment miracle. This gentle and effective laser treatment addresses: wrinkles, acne scarring, uneven skin texture, dark spots, melasma, rosacea, and more. Skin is left bright and healthier.',
        duration=60)
    microneedle = Service(
        type='Advanced Skincare Treatments',
        name='Microneedle',
        price=300,
        description='The aging process naturally slows our collagen and elastin production as we age. Harness your own body’s ability to stimulate collagen and elastin production back to its old self. Microneedling naturally encourages healthier, smoother, brighter skin.',
        duration=60)
    noPeelPeel = Service(
        type='Advanced Skincare Treatments',
        name='No-Peel Peel',
        price=300,
        description='The latest innovation in skin resurfacing - a unique, painless peel that stimulates the production of collagen and elastin in the skin which revitalizes the skin. Zero downtime. Phenomenal results. Within a few days, your skin will appear brighter, smoother & plumper.',
        duration=45)
    microneedleRF = Service(
        type='Signature Skin Therapies',
        name='Microneedle RF',
        price=550,
        description='Microneedling is an amazing, results-oriented treatment. Taking it to the next level by adding Radio Frequency will dramatically tighten lax, loose skin that’s lost its elasticity, in addition to smoothing and restoring your skin to the healthiest version of itself.',
        duration=60)
    nanoGlowRenewel = Service(
        type='Signature Skin Therapies',
        name='NanoGlow Renewal',
        price=350,
        description='Indulge in the ultimate skin rejuvenation with our NanoGlow Renewal treatment. Using cutting-edge nanotechnology, we target and address a range of skin concerns, from fine lines and wrinkles to uneven pigmentation.',
        duration=75)
    complexionCorrection = Service(
        type='Signature Skin Therapies',
        name='Complexion Correction',
        price=450,
        description='This customized procedure targets specific skin concerns, such as pigmentation issues, fine lines, and uneven texture. Through a combination of advanced techniques and tailored skincare, we work to reveal a smoother, more radiant complexion.',
        duration=90)
    oxytheoreSculpt = Service(
        type='Signature Skin Therapies',
        name='Oxytheorē Sculpt',
        price=350,
        description='Our OxyTheorē Sculpt treatment is a non-invasive, painless procedure that delivers multiple benefits to your skin. It enhances oxygenation, promotes hydration, stimulates collagen production, and reduces the signs of aging.',
        duration=90)
    wrinkleRelax = Service(
        type='Injectables',
        name='Wrinkle Relax',
        price=12,
        description='Say goodbye to fine lines and wrinkles and embrace a more youthful, refreshed appearance with our wrinkle relaxer treatments. During your pre-treatment consultation, we\'ll discuss your goals and craft a personalized plan that aligns with your desired results.',
        duration=15)
    lipFiller = Service(
        type='Injectables',
        name='Lip Filler',
        price=700,
        description='Our skilled injectors use high-quality dermal fillers to enhance lip volume, shape, and definition. Whether you desire fuller lips, reduced fine lines around the mouth, or enhanced lip contour, our team will consult with you to understand your vision. Rediscover your confidence with beautifully enhanced lips.',
        duration=30)
    midFaceFiller = Service(
        type='Injectables',
        name='Midface Filler',
        price=120,
        description='We understand the importance of a harmonious facial balance, and our team will create a tailored treatment plan to rejuvenate your mid-face region. Unlock the potential for lasting transformation and embrace a revitalized, more youthful appearance.',
        duration=15)
    lowerFaceFiller = Service(
        type='Injectables',
        name='Lower Face Filler',
        price=120,
        description='Whether you\'re looking to redefine your jawline, smooth out marionette lines, or restore volume in the chin area, our skilled team will work with you to create a customized treatment plan. Rejuvenate your lower face and enjoy long-lasting, transformative results.',
        duration=15)

    db.session.add(consultation)
    db.session.add(signature)
    db.session.add(botanicalBeaute)
    db.session.add(oxytheore)
    db.session.add(nanoglow)
    db.session.add(everythingLaser)
    db.session.add(microneedle)
    db.session.add(noPeelPeel)
    db.session.add(microneedleRF)
    db.session.add(nanoGlowRenewel)
    db.session.add(complexionCorrection)
    db.session.add(oxytheoreSculpt)
    db.session.add(wrinkleRelax)
    db.session.add(lipFiller)
    db.session.add(midFaceFiller)
    db.session.add(lowerFaceFiller)
    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_services():
    if environment == "production":
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.services RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM services"))

    db.session.commit()
