import re
import click
from app.models.class_models.business_models.customer_model import Customer
from app.models.class_models.user_models.collaborator_model import Collaborator
from app.controllers.auth_controllers.permission_controller import login_required_admin
from app.views.class_views.customer_view import display_customer
from app.views.general_views.generic_message import display_message


@login_required_admin
def create_customer(session):
    while True:
        firstname = click.prompt("firstname", type=click.STRING)
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', firstname):
            display_message("firstname should not contain special characters. Try again.")
        else:
            break

    while True:
        lastname = click.prompt("Lastname", type=click.STRING)
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', lastname):
            display_message("Lastname should not contain special characters. Try again.")
        else:
            break

    while True:
        email = click.prompt("Email", type=click.STRING)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            display_message("Email address is not valid. Please try again.")
        else:
            break

    while True:
        phone = click.prompt("Phone", type=click.INT)
        if not phone.strip():
            display_message("Phone number cannot be empty.")
        else:
            break

    while True:
        company = click.prompt("Lastname", type=click.STRING)
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', company):
            display_message("Company should not contain special characters. Try again.")
        else:
            break

    while True:
        collaborator_email = click.prompt("Email", type=click.STRING)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            display_message("Collaborator email address is not valid. Please try again.")
        else:
            collaborator = Collaborator.get_by_email(session, collaborator_email)
            if not collaborator:
                display_message("Collaborator email address is not valid. Please try again.")
            else:
                break

    try:
        customer = Customer.create(session, firstname, lastname, email, phone, company, collaborator)
        display_message(f"Customer created: {customer}")
    except ValueError as e:
        display_message(str(e))


@login_required_admin
def read_customer(session, collaborator_id):
    customer = Customer.get_by_id(session, collaborator_id)
    if customer:
        display_customer(customer)
    else:
        display_message("Customer not found")


@login_required_admin
def update_customer(session, customer_id, firstname, lastname, email, phone, company, collaborator_email):
    customer = Customer.get_by_id(session, customer_id)
    if customer:
        # Validate the inputs for firstname and lastname
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', firstname):
            display_message("firstname should not contain special characters. Try again.")
            return

        if re.search(r'[!@#$%^&*(),.?":{}|<>]', lastname):
            display_message("Lastname should not contain special characters. Try again.")
            return

        # Validate the input for email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            display_message("Email address is not valid. Please try again.")
            return

        # Validate the input for phone
        if not str(phone).strip():
            display_message("Phone number cannot be empty. Please try again.")
            return

        # Validate the input for company
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', company):
            display_message("Company should not contain special characters. Try again.")
            return

        # Validate collaborator email and existence
        if collaborator_email:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", collaborator_email):
                display_message("Collaborator email address is not valid. Please try again.")
                return

            collaborator = Collaborator.get_by_email(session, collaborator_email)
            if not collaborator:
                display_message("Collaborator email address is not valid. Please try again.")
                return

        # Update the customer's information if any updates provided
        kwargs = {'firstname': firstname, 'lastname': lastname, 'email': email, 'phone': phone, 'company': company}

        if collaborator_email:
            kwargs['collaborator'] = collaborator

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if kwargs:
            customer.update(session, **kwargs)
            display_message("Customer updated")
        else:
            display_message("No updates provided")
    else:
        display_message("Customer not found")



@login_required_admin
def delete_customer(session, customer_id):
    customer = Customer.get_by_id(session, customer_id)
    if customer:
        customer.delete(session)
        display_message("Customer deleted")
    else:
        display_message("Customer not found")
