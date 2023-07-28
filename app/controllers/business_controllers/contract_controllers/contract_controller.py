from app.models.class_models.business_models.contract_model import Contract
from app.models.class_models.business_models.customer_model import Customer
from app.models.class_models.user_models.collaborator_model import Collaborator
from app.controllers.auth_controllers.permission_controller import login_required_admin, login_required, login_required_admin_or_seller
from app.views.class_views.contract_view import display_contract_detail, display_list_contracts
from app.views.general_views.generic_message import display_message_success, display_message_error, display_message_correction
import sentry_sdk


@login_required_admin
def create_func(session, user, total_amount, left_to_pay, customer_id, signed):
    try:
        customer_instance = Customer.get_by_id(session, customer_id)
        if customer_instance:
            contract = Contract.create(session, total_amount, left_to_pay, customer_instance, signed)
            display_message_success("Contract created successfully.")
            display_contract_detail(contract)
            sentry_sdk.capture_message(
                f"Collaborator with id : {user.id} has create a contract with id : {contract.id}")
        else:
            display_message_error("Customer not found.")
    except ValueError as e:
        display_message_error(f"Error creating contract: {e}")


@login_required
def read_func(session, user, mine, is_signed, with_event, is_paid):
    try:
        if mine:
            if user.role == Collaborator.RoleEnum.seller:
                contracts = Contract.read(session, user_id=user.id, signed=is_signed, event=with_event, paid=is_paid)
            else:
                display_message_correction("Permission denied. Please log in as a seller to access the mine option for events. The full list of contracts is selected instead.")
                contracts = Contract.read(session, signed=is_signed, event=with_event, paid=is_paid)
        else:
            contracts = Contract.read(session, signed=is_signed, event=with_event, paid=is_paid)

        display_list_contracts(contracts)
    except ValueError as e:
        display_message_error(f"Error reading contracts: {e}")


@login_required
def get_by_id_func(session, user, contract_id):
    try:
        contract = Contract.get_by_id(session, contract_id)
        if contract:
            display_contract_detail(contract)
        else:
            display_message_error("Contract not found.")
    except ValueError as e:
        display_message_error(f"Error getting contract: {e}")


@login_required_admin_or_seller
def update_func(session, user, contract_id, total_amount, left_to_pay, signed):
    try:
        contract = Contract.get_by_id(session, contract_id)

        if contract:
            last_sign_register = contract.signed

            if user.role == Collaborator.RoleEnum.administrator or contract.customer.collaborator_id == user.id:
                contract.update(session, total_amount=total_amount, left_to_pay=left_to_pay, signed=signed)
                display_message_success("Contract updated successfully.")
                display_contract_detail(contract)
                if last_sign_register != contract.signed:
                    sentry_sdk.capture_message(
                        f"Collaborator with id : {user.id} has update a collaborator with id : {contract.id} and the signature status changed to:{contract.signed}")
                else:
                    sentry_sdk.capture_message(f"Collaborator with id : {user.id} has update a contract with id : {contract.id} but no change about signature status")
            else:
                display_message_error("Only an administrator or the referring seller can update the contract.")
        else:
            display_message_error("Contract not found.")
    except ValueError as e:
        display_message_error(f"Error updating contract: {e}")


@login_required_admin
def delete_func(session, user, contract_id):
    try:
        contract = Contract.get_by_id(session, contract_id)
        if contract:
            contract.delete(session)
            display_message_success("Contract deleted successfully.")
            sentry_sdk.capture_message(
                f"Collaborator with id : {user.id} has delete a contract with id : {contract.id}")
        else:
            display_message_error("Contract not found.")
    except ValueError as e:
        display_message_error(f"Error deleting contract: {e}")
