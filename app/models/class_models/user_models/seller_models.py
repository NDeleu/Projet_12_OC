from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import text
from passlib.hash import bcrypt
from app.models.database_models.database import Base
from sqlalchemy.orm import relationship


class Seller(Base):

    __tablename__ = 'sellers'

    id = Column(Integer, primary_key=True)
    surname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    token = Column(String)
    token_expiration = Column(DateTime)
    customers = relationship("Customer", back_populates="seller", cascade="all, delete")

    def __init__(self, surname, lastname, email, password):
        self.surname = surname
        self.lastname = lastname
        self.email = email
        self.set_password(password)

    @classmethod
    def create(cls, session, surname, lastname, email, password):
        email_exists = session.execute(
            text(
                "SELECT EXISTS (SELECT 1 FROM administrators WHERE email=:email) "
                "OR EXISTS (SELECT 1 FROM sellers WHERE email=:email)"
                "OR EXISTS (SELECT 1 FROM supports WHERE email=:email)"
                "OR EXISTS (SELECT 1 FROM customers WHERE email=:email)"),
            {"email": email}
        ).scalar()

        if email_exists:
            raise ValueError(
                "The email address already exists for an administrator, seller, support or customer.")

        seller = Seller(surname=surname, lastname=lastname,
                        email=email, password=password)
        session.add(seller)
        session.commit()
        return seller

    @classmethod
    def read(cls, session, seller_id):
        seller = session.query(Seller).filter_by(id=seller_id).first()
        return seller

    def set_email(self, session, new_email):
        email_exists = session.execute(
            text(
                "SELECT EXISTS (SELECT 1 FROM administrators WHERE email=:new_email) "
                "OR EXISTS (SELECT 1 FROM sellers WHERE email=:new_email)"
                "OR EXISTS (SELECT 1 FROM supports WHERE email=:new_email)"
                "OR EXISTS (SELECT 1 FROM customers WHERE email=:new_email)"),
            {"new_email": new_email}
        ).scalar()

        if email_exists:
            raise ValueError(
                "The email address already exists for an administrator, seller, support or customer.")

        self.email = new_email

    def set_password(self, password):
        self.password = bcrypt.hash(password)

    def update(self, session, **kwargs):
        for key, value in kwargs.items():
            if key == 'email':
                self.set_email(session, value)
            elif key == 'password':
                self.set_password(value)  # Hash the updated password
            else:
                setattr(self, key, value)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)

    def __str__(self):
        return f'{self.surname} {self.lastname}'
