from unittest.mock import Mock, call
from datetime import datetime
import pytest
from app.models.class_models.user_models.collaborator_model import Collaborator
from app.models.class_models.business_models.contract_model import Contract
from app.models.class_models.business_models.event_model import Event
from app.models.class_models.business_models.customer_model import Customer
from app.views.class_views.contract_view import display_contract_detail
@pytest.fixture
def mock_console(monkeypatch):
    mock_console = Mock()
    monkeypatch.setattr("app.views.class_views.contract_view.console", mock_console)
    return mock_console

def test_display_contract_detail(mock_console, db_session, seller_user, support_user):
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

    display_contract_detail(contract)

    expected_output = [
        call("[bold yellow]Contract Details:[/bold yellow]"),
        call(f"Contract ID: {contract.id}"),
        call(f"Total Amount: {contract.total_amount}"),
        call(f"Left to Pay: {contract.left_to_pay}"),
        call(f"Date Created: {contract.date_created}"),
        call("Signed: Yes"),
        call("Customer:"),
        call(f"  Customer ID: {contract.customer_id}"),
        call(f"  Customer Name: {contract.customer.firstname} - {contract.customer.lastname}"),
        call(f"  Customer Email: {contract.customer.email}"),
        call("Seller assigned:"),
        call(f"  Seller ID assigned: {contract.customer.collaborator_id}"),
        call(f"  Seller Name assigned: {contract.customer.collaborator.firstname} - {contract.customer.collaborator.lastname}"),
        call(f"  Seller Email assigned: {contract.customer.collaborator.email}"),
        call("Event:"),
        call(f"  Event ID: {event.id}"),
        call(f"  Event Name: {event.name}"),
        call(f"  Event Start Time: {event.event_start}"),
        call(f"  Event End Time: {event.event_end}"),
    ]

    mock_console.print.assert_has_calls(expected_output)
