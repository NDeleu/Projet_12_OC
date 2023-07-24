import re
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.database_models.database import Base
from datetime import datetime


class Event(Base):

    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=100))
    event_start = Column(DateTime)
    event_end = Column(DateTime)
    location = Column(String(length=100))
    attendees = Column(Integer)
    instruction = Column(String(length=240))
    collaborator_id = Column(Integer, ForeignKey('collaborators.id'))
    collaborator = relationship("Collaborator", back_populates="events")
    contract_id = Column(Integer, ForeignKey('contracts.id'), unique=True)
    contract = relationship("Contract", uselist=False, back_populates="event")

    def __init__(self, name, event_start, event_end, location, attendees, instruction, contract, collaborator=None):
        self.set_name(name)
        self.set_event_start(event_start)
        self.set_event_end(event_end)
        self.set_location(location)
        self.set_attendees(attendees)
        self.set_instruction(instruction)
        self.contract = contract
        self.collaborator = collaborator

    def set_name(self, name):
        if not name:
            raise ValueError("Name cannot be empty.")
        if not re.match("^[a-zA-Z0-9 ]+$", name):
            raise ValueError(
                "Invalid input. Please enter a valid name without special characters.")
        self.name = name

    def set_location(self, location):
        if not location:
            raise ValueError("Location cannot be empty.")
        if not re.match("^[a-zA-Z0-9 ]+$", location):
            raise ValueError(
                "Invalid input. Please enter a valid location without special characters.")
        self.location = location

    def set_instruction(self, instruction):
        if not instruction:
            raise ValueError("Instruction cannot be empty.")
        if not re.match("^[a-zA-Z0-9 ]+$", instruction):
            raise ValueError(
                "Invalid input. Please enter a valid instruction without special characters.")
        self.instruction = instruction

    def set_attendees(self, attendees):
        if attendees is None:
            raise ValueError("Attendees cannot be empty.")
        if not isinstance(attendees, int):
            raise ValueError("Attendees must be an integer.")
        self.attendees = attendees

    def set_event_start(self, event_start):
        if not event_start:
            raise ValueError("Event start date cannot be empty.")
        if not isinstance(event_start, datetime):
            raise ValueError("Event start must be a datetime object.")
        self.event_start = event_start

    def set_event_end(self, event_end):
        if not event_end:
            raise ValueError("Event end date cannot be empty.")
        if not isinstance(event_end, datetime):
            raise ValueError("Event start must be a datetime object.")
        self.event_end = event_end

    @classmethod
    def create(cls, session, name, event_start, event_end, location, attendees, instruction, contract, collaborator=None):

        event = Event(name=name, event_start=event_start, event_end=event_end,
                      location=location, attendees=attendees,
                      instruction=instruction, contract=contract, collaborator=collaborator)

        session.add(event)

        if collaborator:
            is_support = collaborator.role == collaborator.__class__.RoleEnum.support
            if not is_support:
                raise ValueError(
                    f"Only collaborators with the role of 'support' can be linked to a customer.")

        session.commit()
        return event

    @classmethod
    def read(cls, session, user_id=None, supported=None):
        query = session.query(Event)

        if user_id is not None:
            query = query.filter(Event.collaborator_id == user_id)

        if supported is not None and not isinstance(supported, bool):
            raise ValueError("Supported must be either True, False, or None.")

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
                is_support = value.role == value.__class__.RoleEnum.support
                if not is_support:
                    raise ValueError(
                        f"Only collaborators with the role of 'support' can be linked to a customer.")

                self.collaborator = value
            else:
                setattr(self, key, value)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    def __str__(self):
        return f'{self.name}'
