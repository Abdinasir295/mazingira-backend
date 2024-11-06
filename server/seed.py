from app import app
from models import db, User, Donor, Organisation, Donation, Review
from datetime import datetime

def seed_database():
    with app.app_context():
        print("Clearing database...")
        db.drop_all()
        db.create_all()

        print("Creating users...")
        # Create Users
        user1 = User(username="john_donor", email="john@example.com", role="donor")
        user2 = User(username="charity_org", email="charity@example.com", role="organisation")
        user3 = User(username="jane_donor", email="jane@example.com", role="donor")
        user4 = User(username="admin_user", email="admin@example.com", role="admin")

        db.session.add_all([user1, user2, user3, user4])
        db.session.commit()

        print("Creating donors...")
        # Create Donors
        donor1 = Donor(
            user_id=user1.id,
            name="John Smith",
            phone="123-456-7890",
            address="123 Main St"
        )
        donor2 = Donor(
            user_id=user3.id,
            name="Jane Doe",
            phone="098-765-4321",
            address="456 Oak Ave"
        )

        db.session.add_all([donor1, donor2])
        db.session.commit()

        print("Creating organisations...")
        # Create Organisations
        org1 = Organisation(
            user_id=user2.id,
            name="Charity Foundation",
            description="Helping those in need",
            phone="555-555-5555",
            address="789 Charity Lane",
            registration_number="CH123456",
            verified=True
        )

        db.session.add(org1)
        db.session.commit()

        print("Creating donations...")
        # Create Donations
        donation1 = Donation(
            donor_id=donor1.id,
            organisation_id=org1.id,
            amount=100.00,
            date=datetime.utcnow(),
            status="completed",
            payment_method="credit_card",
            transaction_id="TX123456"
        )
        donation2 = Donation(
            donor_id=donor2.id,
            organisation_id=org1.id,
            amount=50.00,
            date=datetime.utcnow(),
            status="completed",
            payment_method="paypal",
            transaction_id="TX789012"
        )

        db.session.add_all([donation1, donation2])
        db.session.commit()

        print("Creating reviews...")
        # Create Reviews
        review1 = Review(
            donor_id=donor1.id,
            organisation_id=org1.id,
            rating=5,
            comment="Great organization!",
            date=datetime.utcnow()
        )
        review2 = Review(
            donor_id=donor2.id,
            organisation_id=org1.id,
            rating=4,
            comment="Good experience",
            date=datetime.utcnow()
        )

        db.session.add_all([review1, review2])
        db.session.commit()

        print("Seeding completed!")

if __name__ == '__main__':
    seed_database()