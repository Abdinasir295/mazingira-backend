from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    serialize_rules = ('-password_hash', '-donor', '-organisation')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False)  # admin, donor, organisation

    @validates('role')
    def validate_role(self, key, role):
        if role not in ['admin', 'donor', 'organisation']:
            raise ValueError('Invalid role')
        return role

class Donor(db.Model, SerializerMixin):
    __tablename__ = 'donors'
    serialize_rules = ('-user.donor', '-donations.donor', '-reviews.donor')

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))

    # Relationships
    user = db.relationship('User', backref=db.backref('donor', uselist=False))
    donations = db.relationship('Donation', back_populates='donor')
    reviews = db.relationship('Review', back_populates='donor')

    # Association proxy to get organisations directly
    organisations = association_proxy('donations', 'organisation')

class Organisation(db.Model, SerializerMixin):
    __tablename__ = 'organisations'
    serialize_rules = ('-user.organisation', '-donations.organisation', '-reviews.organisation')

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    registration_number = db.Column(db.String(50), unique=True)
    verified = db.Column(db.Boolean, default=False)

    # Relationships
    user = db.relationship('User', backref=db.backref('organisation', uselist=False))
    donations = db.relationship('Donation', back_populates='organisation')
    reviews = db.relationship('Review', back_populates='organisation')

    # Association proxy to get donors directly
    donors = association_proxy('donations', 'donor')

class Donation(db.Model, SerializerMixin):
    __tablename__ = 'donations'
    serialize_rules = ('-donor.donations', '-organisation.donations')

    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('donors.id'))
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id'))
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    is_anonymous = db.Column(db.Boolean, default=False)
    payment_method = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100), unique=True)

    # Relationships
    donor = db.relationship('Donor', back_populates='donations')
    organisation = db.relationship('Organisation', back_populates='donations')

    @validates('amount')
    def validate_amount(self, key, amount):
        if amount <= 0:
            raise ValueError('Amount must be greater than 0')
        return amount

    @validates('status')
    def validate_status(self, key, status):
        valid_statuses = ['pending', 'completed', 'failed']
        if status not in valid_statuses:
            raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}')
        return status

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    serialize_rules = ('-donor.reviews', '-organisation.reviews')

    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('donors.id'))
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id'))
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    is_anonymous = db.Column(db.Boolean, default=False)

    # Relationships
    donor = db.relationship('Donor', back_populates='reviews')
    organisation = db.relationship('Organisation', back_populates='reviews')

    @validates('rating')
    def validate_rating(self, key, rating):
        if not 1 <= rating <= 5:
            raise ValueError('Rating must be between 1 and 5')
        return rating