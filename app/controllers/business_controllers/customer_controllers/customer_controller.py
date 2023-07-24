from app.models.class_models.business_models.customer_model import Customer
from app.models.class_models.user_models.collaborator_model import Collaborator
from app.controllers.auth_controllers.permission_controller import login_required_seller, login_required
from app.views.class_views.customer_view import display_customer
from app.views.general_views.generic_message import display_message


@login_required_seller
def create_func(session, user, firstname, lastname, email, phone, company):
    try:
        collaborator = Collaborator.get_by_id(session, user.id)
        customer = Customer.create(session, firstname, lastname, email, phone, company, collaborator)
        display_customer(customer)
    except ValueError as e:
        display_message(f"Error creating customer: {e}")


@login_required
def read_func(session, user, mine):
    try:
        if mine:
            if user.role == 'seller':
                list_customers = Customer.read(session, user.id)
            else:
                display_message(
                    "Permission denied. Please login as a seller to access the mine option for customers. The full list of customers is selected instead.")
                list_customers = Customer.read(session)
        else:
            list_customers = Customer.read(session)
        for customer in list_customers:
            display_customer(customer)
    except Exception as e:
        display_message(f"Error reading customers: {e}")


@login_required
def get_by_id_func(session, user, customer_id):
    try:
        customer = Customer.get_by_id(session, customer_id)
        if customer:
            display_customer(customer)
        else:
            display_message("Customer not found.")
    except Exception as e:
        display_message(f"Error getting customer by ID: {e}")


@login_required
def get_by_email_func(session, user, customer_email):
    try:
        customer = Customer.get_by_email(session, customer_email)
        if customer:
            display_customer(customer)
        else:
            display_message("Customer not found.")
    except Exception as e:
        display_message(f"Error getting customer by email: {e}")


@login_required_seller
def update_func(session, user, customer_id, firstname, lastname, email, phone, company):
    try:
        customer = Customer.get_by_id(session, customer_id)
        if customer:
            if customer.collaborator_id == user.id:
                customer.update(session, firstname=firstname, lastname=lastname, email=email, phone=phone, company=company)
                display_customer(customer)
            else:
                display_message("Only the seller assigned to the customer can edit the customer's profile.")
        else:
            display_message("Customer not found.")
    except ValueError as e:
        display_message(f"Error updating customer: {e}")


@login_required_seller
def delete_func(session, user, customer_id):
    try:
        customer = Customer.get_by_id(session, customer_id)
        if customer:
            customer.delete(session)
            display_message("Customer deleted successfully.")
        else:
            display_message("Customer not found.")
    except Exception as e:
        display_message(f"Error deleting customer: {e}")
