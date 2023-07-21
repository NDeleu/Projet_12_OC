from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.database_models.database import Base, session


class Event(Base):

    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    event_start = Column(DateTime)
    event_end = Column(DateTime)
    location = Column(String)
    attendees = Column(Integer)
    instruction = Column(String)
    support_id = Column(Integer, ForeignKey('supports.id'))
    support = relationship("Support", back_populates="events")
    contract_id = Column(Integer, ForeignKey('contracts.id'), unique=True)
    contract = relationship("Contract", uselist=False, back_populates="event")

    def __init__(self, name, event_start, event_end, location, attendees, instruction, contract):
        self.name = name
        self.event_start = event_start
        self.event_end = event_end
        self.location = location
        self.attendees = attendees
        self.instruction = instruction
        self.contract = contract

    @classmethod
    def create(cls, name, event_start, event_end, location, attendees, instruction, contract):
        event = Event(name=name, event_start=event_start, event_end=event_end,
                      location=location, attendees=attendees,
                      instruction=instruction, contract=contract)
        session.add(event)
        session.commit()
        return event

    @classmethod
    def read(cls, event_id):
        event = session.query(Event).filter_by(id=event_id).first()
        return event

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def __str__(self):
        return f'{self.name}'
