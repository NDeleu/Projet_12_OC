from unittest.mock import Mock, call
from datetime import datetime
import pytest
from app.models.class_models.user_models.collaborator_model import Collaborator
from app.models.class_models.business_models.contract_model import Contract
from app.models.class_models.business_models.event_model import Event
from app.models.class_models.business_models.customer_model import Customer
from app.views.class_views.customer_view import display_customer_detail, display_announce_customer_list, display_customer_summary

@pytest.fixture
def mock_console(monkeypatch):
    mock_console = Mock()
    monkeypatch.setattr("app.views.class_views.customer_view.console", mock_console)
    return mock_console

def test_display_customer_detail(mock_console, db_session, seller_user, support_user):
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

    display_customer_detail(customer)

    expected_output = [
        call("[bold yellow]Customer Details:[/bold yellow]"),
        call(f"ID: {customer.id}"),
        call(f"Firstname: {customer.firstname}"),
        call(f"Lastname: {customer.lastname}"),
        call(f"Email: {customer.email}"),
        call(f"Phone: {customer.phone}"),
        call(f"Company: {customer.company}"),
        call(f"Creation Date: {customer.date_created}"),
        call(f"Update Date: {customer.date_updated}"),
        call("Seller:"),
        call(f"  Seller ID: {customer.collaborator_id}"),
        call(f"  Seller Name: {customer.collaborator.firstname} - {customer.collaborator.lastname}"),
        call(f"  Seller Email: {customer.collaborator.email}"),
        call("Contracts:"),
        call(f"  Contract ID: {contract.id}"),
        call(f"  Total Amount: {contract.total_amount}"),
        call(f"  Left to Pay: {contract.left_to_pay}"),
        call(f"  Date Created: {contract.date_created}"),
        call("  Signed: Yes"),
        call("  Event:"),
        call(f"    Event ID: {event.id}"),
        call(f"    Event Name: {event.name}"),
    ]

    mock_console.print.assert_has_calls(expected_output)


def test_display_announce_customer_list(mock_console):
    display_announce_customer_list()
    mock_console.print.assert_called_once_with("[bold yellow]Customers List:[/bold yellow]")


def test_display_customer_summary(mock_console, db_session, seller_user, support_user):
    customer = Customer(firstname="Customer1", lastname="Smith",
                        email="customer1@example.com", phone="1234567890",
                        company="Company A", collaborator=seller_user)
    contract = Contract(total_amount=5000, left_to_pay=2000, customer=customer, signed=True)

    db_session.add_all([customer, contract])
    db_session.commit()

    display_customer_summary(customer)

    expected_output = [
        call(" "),
        call(f"ID: {customer.id}"),
        call(f"Name: {customer.firstname} - {customer.lastname}"),
        call(f"Email: {customer.email}"),
        call(f"Phone: {customer.phone}"),
        call(f"Company: {customer.company}"),
        call(f"  Seller Email: {customer.collaborator.email}"),
    ]

    mock_console.print.assert_has_calls(expected_output)
