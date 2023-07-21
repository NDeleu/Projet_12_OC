from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import text
from datetime import datetime
from app.models.database_models.database import Base, session


class Customer(Base):

    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    surname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True)
    phone = Column(Integer)
    company = Column(String)
    date_created = Column(DateTime, default=datetime.now)
    date_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    seller_id = Column(Integer, ForeignKey('sellers.id'))
    seller = relationship("Seller", back_populates="customers")
    contracts = relationship("Contract", back_populates="customer", cascade="all, delete")

    def __init__(self, surname, lastname, email, phone, company, seller):
        self.surname = surname
        self.lastname = lastname
        self.email = email
        self.phone = phone
        self.company = company
        self.seller = seller

    @classmethod
    def create(cls, surname, lastname, email, phone, company, seller):
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

        customer = Customer(surname=surname, lastname=lastname,
                            email=email, phone=phone,
                            company=company, seller=seller)
        session.add(customer)
        session.commit()
        return customer

    @classmethod
    def read(cls, customer_id):
        customer = session.query(Customer).filter_by(id=customer_id).first()
        return customer

    def set_email(self, new_email):
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

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'email':
                self.set_email(value)
            else:
                setattr(self, key, value)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def __str__(self):
        return f'{self.surname} {self.lastname}'
