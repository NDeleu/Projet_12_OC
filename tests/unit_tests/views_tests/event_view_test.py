from unittest.mock import Mock, call
from datetime import datetime
import pytest
from app.models.class_models.user_models.collaborator_model import Collaborator
from app.models.class_models.business_models.contract_model import Contract
from app.models.class_models.business_models.event_model import Event
from app.models.class_models.business_models.customer_model import Customer
from app.views.class_views.event_view import display_event_detail

@pytest.fixture
def mock_console(monkeypatch):
    mock_console = Mock()
    monkeypatch.setattr("app.views.class_views.event_view.console", mock_console)
    return mock_console


def test_display_event_detail(mock_console, db_session, seller_user, support_user):
    customer = Customer(firstname="Customer1", lastname="Smith",
                        email="customer1@example.com", phone="1234567890",
                        company="Company A", collaborator=seller_user)
    contract = Contract(total_amount=5000, left_to_pay=2000, customer=customer, signed=True)
    event = Event(name="Event One", event_start=datetime(2023, 7, 26, 10, 0),
                  event_end=datetime(2023, 7, 26, 14, 0), location="Test Location",
                  attendees=50, instruction="Test Instruction", contract=contract,
                  collaborator=support_user)

    db_session.add_all([customer, contract, event])
    db_session.commit()

    display_event_detail(event)

    expected_output = [
        call("[bold yellow]Event Details:[/bold yellow]"),
        call(f"Event ID: {event.id}"),
        call(f"Name: {event.name}"),
        call(f"Start Time: {event.event_start}"),
        call(f"End Time: {event.event_end}"),
        call(f"Location: {event.location}"),
        call(f"Number of Attendees: {event.attendees}"),
        call(f"Instruction: {event.instruction}"),
        call("Contract:"),
        call(f"  Contract ID: {event.contract_id}"),
        call(f"  Date Created: {contract.date_created}"),
        call("Customer:"),
        call(f"  Customer ID: {customer.id}"),
        call(f"  Customer Name: {customer.firstname} - {customer.lastname}"),
        call(f"  Customer Email: {customer.email}"),
        call(f"  Customer Phone: {customer.phone}"),
        call("Support assigned:"),
        call(
            f"  Support Name assigned: {support_user.firstname} - {support_user.lastname}"),
        call(f"  Support Email assigned: {support_user.email}"),
    ]

    mock_console.print.assert_has_calls(expected_output)
