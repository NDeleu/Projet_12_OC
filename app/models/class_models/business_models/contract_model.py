from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.database_models.database import Base


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
    def create(cls, session, total_amount, left_to_pay, customer):
        contract = Contract(total_amount=total_amount, left_to_pay=left_to_pay,
                            customer=customer)
        session.add(contract)
        session.commit()
        return contract

    @classmethod
    def read(cls, session, user_id=None, signed=None, event=None, paid=None):
        query = session.query(Contract)

        if user_id is not None:
            query = query.filter(Contract.customer.has(collaborator_id=user_id))

        if signed is not None:
            query = query.filter(Contract.signed == signed)

        if event is not None:
            if event is True:
                query = query.filter(Contract.event != None)
            elif event is False:
                query = query.filter(Contract.event == None)

        if paid is not None:
            if paid is True:
                query = query.filter(Contract.left_to_pay <= 0)
            elif paid is False:
                query = query.filter(Contract.left_to_pay > 0)

        list_contracts = query.distinct().all()
        return list_contracts

    @classmethod
    def get_by_id(cls, session, contract_id):
        contract = session.query(Contract).filter_by(id=contract_id).first()
        return contract

    def update(self, session, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    def __str__(self):
        return f'contract ID : {self.id}'
