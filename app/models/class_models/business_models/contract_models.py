from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.database_models.database import Base, session


class Contract(Base):

    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, default=datetime.now)
    total_amount = Column(Float)
    left_to_pay = Column(Float)
    signed = Column(Boolean, default=False)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship("Customer", back_populates="contracts")
    event = relationship("Event", uselist=False, back_populates="contract")

    def __init__(self, total_amount, left_to_pay, customer):
        self.total_amount = total_amount
        self.left_to_pay = left_to_pay
        self.customer = customer


    @classmethod
    def create(cls, total_amount, left_to_pay, customer):
        contract = Contract(total_amount=total_amount, left_to_pay=left_to_pay,
                            customer=customer)
        session.add(contract)
        session.commit()
        return contract

    @classmethod
    def read(cls, contract_id):
        contract = session.query(Contract).filter_by(id=contract_id).first()
        return contract

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def __str__(self):
        return f'contract ID : {self.id}'
