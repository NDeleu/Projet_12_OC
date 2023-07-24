from app.models.class_models.business_models.contract_model import Contract
from app.models.class_models.business_models.customer_model import Customer
from app.models.class_models.business_models.event_model import Event
from app.controllers.auth_controllers.permission_controller import login_required_admin, login_required, login_required_seller, login_required_admin_or_seller
from app.views.class_views.contract_view import display_contract
from app.views.general_views.generic_message import display_message


@login_required_admin
def create_func(session, user, total_amount, left_to_pay, customer, signed):
    try:
        customer_instance = Customer.get_by_id(session, customer)
        if customer_instance:
            contract = Contract.create(session, total_amount, left_to_pay, customer_instance, signed)
            display_contract(contract)
        else:
            display_message("Customer not found.")
    except ValueError as e:
        display_message(f"Error creating contract: {e}")


@login_required
def read_func(session, user, mine, is_signed, with_event, is_paid):
    try:
        if mine:
            if user.role == "seller":
                contracts = Contract.read(session, user_id=user.id, signed=is_signed, event=with_event, paid=is_paid)
            else:
                display_message("Permission denied. Please log in as a seller to access the mine option for events. The full list of contracts is selected instead.")
                contracts = Contract.read(session, signed=is_signed, event=with_event, paid=is_paid)
        else:
            contracts = Contract.read(session, signed=is_signed, event=with_event, paid=is_paid)

        for contract in contracts:
            display_contract(contract)
    except ValueError as e:
        display_message(f"Error reading contracts: {e}")


@login_required
def get_by_id_func(session, user, contract_id):
    try:
        contract = Contract.get_by_id(session, contract_id)
        if contract:
            display_contract(contract)
        else:
            display_message("Contract not found.")
    except ValueError as e:
        display_message(f"Error getting contract: {e}")


@login_required_admin_or_seller
def update_func(session, user, contract_id, total_amount, left_to_pay, signed):
    try:
        contract = Contract.get_by_id(session, contract_id)
        if contract:
            if user.role == "administrator" or contract.customer.collaborator_id == user.id:
                contract.update(session, total_amount=total_amount, left_to_pay=left_to_pay, signed=signed)
                display_message("Contract updated successfully.")
                display_contract(contract)
            else:
                display_message("Only an administrator or the referring seller can update the contract.")
        else:
            display_message("Contract not found.")
    except ValueError as e:
        display_message(f"Error updating contract: {e}")


@login_required_admin
def delete_func(session, user, contract_id):
    try:
        contract = Contract.get_by_id(session, contract_id)
        if contract:
            contract.delete(session)
            display_message("Contract deleted successfully.")
        else:
            display_message("Contract not found.")
    except ValueError as e:
        display_message(f"Error deleting contract: {e}")
