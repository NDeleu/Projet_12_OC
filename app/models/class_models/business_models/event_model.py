from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, text
from sqlalchemy.orm import relationship
from app.models.database_models.database import Base


class Event(Base):

    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    event_start = Column(DateTime)
    event_end = Column(DateTime)
    location = Column(String)
    attendees = Column(Integer)
    instruction = Column(String)
    collaborator_id = Column(Integer, ForeignKey('collaborators.id'))
    collaborator = relationship("Collaborator", back_populates="events")
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
    def create(cls, session, name, event_start, event_end, location, attendees, instruction, contract):
        event = Event(name=name, event_start=event_start, event_end=event_end,
                      location=location, attendees=attendees,
                      instruction=instruction, contract=contract)
        session.add(event)
        session.commit()
        return event

    @classmethod
    def read(cls, session, user_id=None, supported=None):
        query = session.query(Event)

        if user_id is not None:
            query = query.filter(Event.collaborator_id == user_id)

        if supported is not None:
            if supported is True:
                query = query.filter(Event.collaborator != None)
            elif supported is False:
                query = query.filter(Event.collaborator == None)

        list_events = query.distinct().all()
        return list_events

    @classmethod
    def get_by_id(cls, session, event_id):
        event = session.query(Event).filter_by(id=event_id).first()
        return event

    def update(self, session, **kwargs):
        for key, value in kwargs.items():
            if key == 'collaborator':
                is_support = session.execute(
                    text(
                        "SELECT 1 FROM collaborators WHERE id=:collaborator_id AND role=:role"
                    ),
                    {"collaborator_id": value.id, "role": "support"}
                ).scalar()

                if not is_support:
                    raise ValueError(
                        "Only collaborators with the role of 'support' can be linked to a customer.")

                self.collaborator = value
            else:
                setattr(self, key, value)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    def __str__(self):
        return f'{self.name}'
