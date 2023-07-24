from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.database_models.database import Base


class Contract(Base):

    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, default=datetime.now)
    total_amount = Column(Numeric(precision=10, scale=2))
    left_to_pay = Column(Numeric(precision=10, scale=2))
    signed = Column(Boolean, default=False)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship("Customer", back_populates="contracts")
    event = relationship("Event", uselist=False, back_populates="contract")

    def __init__(self, total_amount, left_to_pay, customer, signed=False):
        self.set_total_amount(total_amount)
        self.set_left_to_pay(left_to_pay)
        self.set_signed(signed)
        self.customer = customer

    def set_total_amount(self, total_amount):
        if not isinstance(total_amount, (int, float)):
            raise ValueError("Total amount must be a numeric value.")
        self.total_amount = total_amount

    def set_left_to_pay(self, left_to_pay):
        if not isinstance(left_to_pay, (int, float)):
            raise ValueError("Left to pay must be a numeric value.")
        self.left_to_pay = left_to_pay

    def set_signed(self, signed):
        if not isinstance(signed, bool):
            raise ValueError("Signed must be a boolean value.")
        self.signed = signed

    @classmethod
    def create(cls, session, total_amount, left_to_pay, customer, signed=False):
        contract = Contract(total_amount=total_amount, left_to_pay=left_to_pay,
                            customer=customer, signed=signed)
        session.add(contract)
        session.commit()
        return contract

    @classmethod
    def read(cls, session, user_id=None, signed=None, event=None, paid=None):
        query = session.query(Contract)

        if user_id is not None:
            query = query.filter(
                Contract.customer.has(collaborator_id=user_id))

        if signed is not None and not isinstance(signed, bool):
            raise ValueError("Signed must be either True, False, or None.")

        if signed is not None:
            query = query.filter(Contract.signed == signed)

        if event is not None and not isinstance(event, bool):
            raise ValueError("Event must be either True, False, or None.")

        if event is True:
            query = query.filter(Contract.event != None)
        elif event is False:
            query = query.filter(Contract.event == None)
        else:
            pass

        if paid is not None and not isinstance(paid, bool):
            raise ValueError("Paid must be either True, False, or None.")

        if paid is True:
            query = query.filter(Contract.left_to_pay <= 0)
        elif paid is False:
            query = query.filter(Contract.left_to_pay > 0)
        else:
            pass

        list_contracts = query.distinct().all()
        return list_contracts

    @classmethod
    def get_by_id(cls, session, contract_id):
        contract = session.query(Contract).filter_by(id=contract_id).first()
        return contract

    def update(self, session, **kwargs):
        for key, value in kwargs.items():
            if value is not None:
                setattr(self, key, value)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    def __str__(self):
        return f'contract ID : {self.id}'
