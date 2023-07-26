from unittest.mock import Mock, call
import pytest
from datetime import datetime
from app.models.class_models.user_models.collaborator_model import Collaborator
from app.models.class_models.business_models.contract_model import Contract
from app.models.class_models.business_models.event_model import Event
from app.models.class_models.business_models.customer_model import Customer
from app.views.class_views.collaborator_view import (
    display_collaborator_detail,
    display_announce_collaborator_list,
    display_collaborator_summary,
)

@pytest.fixture
def mock_console(monkeypatch):
    mock_console = Mock()
    monkeypatch.setattr("app.views.class_views.collaborator_view.console", mock_console)
    return mock_console


def test_display_collaborator_detail(mock_console, db_session, support_user, seller_user):
    customer1 = Customer(firstname="Customer1", lastname="Smith",
                        email="customer1@example.com", phone="1234567890",
                        company="Company A", collaborator=seller_user)
    contract1 = Contract(total_amount=5000, left_to_pay=2000, customer=customer1, signed=True)
    event1 = Event(name="Event One", event_start=datetime(2023, 7, 26, 10, 0),
                  event_end=datetime(2023, 7, 26, 14, 0), location="Test Location1",
                  attendees=50, instruction="Test Instruction1", contract=contract1,
                  collaborator=support_user)

    customer2 = Customer(firstname="Customer2", lastname="Done",
                        email="customer2@example.com", phone="1234567890",
                        company="Company B", collaborator=seller_user)
    contract2 = Contract(total_amount=7500, left_to_pay=3500, customer=customer2, signed=True)
    event2 = Event(name="Event Two", event_start=datetime(2023, 7, 26, 16, 0),
                  event_end=datetime(2023, 7, 26, 18, 0), location="Test Location2",
                  attendees=80, instruction="Test Instruction2", contract=contract2,
                  collaborator=support_user)

    db_session.add_all([customer1, contract1, event1, customer2, contract2, event2])
    db_session.commit()

    display_collaborator_detail(support_user)

    expected_output_support = [
        call(f"[bold yellow]Collaborator Details:[/bold yellow]"),
        call(f"Collaborator ID: {support_user.id}"),
        call(f"Firstname: {support_user.firstname}"),
        call(f"Lastname: {support_user.lastname}"),
        call(f"Role: {support_user.role}"),
        call(f"Email: {support_user.email}"),
        call(f"Events:"),
        call(f"  Event ID: {event1.id}"),
        call(f"  Event Name: {event1.name}"),
        call(f"  Event ID: {event2.id}"),
        call(f"  Event Name: {event2.name}"),
    ]

    mock_console.print.assert_has_calls(expected_output_support)

    mock_console.reset_mock()

    display_collaborator_detail(seller_user)

    expected_output_seller = [
        call(f"[bold yellow]Collaborator Details:[/bold yellow]"),
        call(f"Collaborator ID: {seller_user.id}"),
        call(f"Firstname: {seller_user.firstname}"),
        call(f"Lastname: {seller_user.lastname}"),
        call(f"Role: {seller_user.role}"),
        call(f"Email: {seller_user.email}"),
        call(f"Customer:"),
        call(f"  Customer ID: {customer1.id}"),
        call(f"  Customer Name: {customer1.firstname} - {customer1.lastname}"),
        call(f"  Customer Email: {customer1.email}"),
        call(f"  Customer ID: {customer2.id}"),
        call(f"  Customer Name: {customer2.firstname} - {customer2.lastname}"),
        call(f"  Customer Email: {customer2.email}"),
    ]

    mock_console.print.assert_has_calls(expected_output_seller)


def test_display_announce_collaborator_list(mock_console):
    display_announce_collaborator_list()
    mock_console.print.assert_called_once_with("[bold yellow]Collaborator List:[/bold yellow]")


def test_display_collaborator_summary(mock_console, db_session, admin_user):

    display_collaborator_summary(admin_user)

    expected_output = [
        call(f" "),
        call(f"ID: {admin_user.id}"),
        call(f"Name: {admin_user.firstname} - {admin_user.lastname}"),
        call(f"Role: {admin_user.role}"),
        call(f"Email: {admin_user.email}"),
    ]

    mock_console.print.assert_has_calls(expected_output)
