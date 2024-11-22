import os
import time
from dotenv import load_dotenv
from flask import Blueprint, app, current_app, render_template, redirect, request, send_from_directory, url_for, flash
from flask_login import login_user, logout_user, login_required, UserMixin, current_user
# from .managerconf import managers_login_manager
# from .models import Owner
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import Account
from . import db
from flask import current_app
from .forms import AddCatForm, AddDCatForm, AddDepartmentForm, CreateRestaurantForm, EditAccountForm, AccountForm, EditCattForm, EditDCattForm, EditDepartmentForm, EditRestaurantForm, EditStaffForm, SALoginForm, StaffForm


managers = Blueprint('managers', __name__)

@managers.route('/')
def index():
    return render_template('index.html')

@managers.route('/rest-auth')
def restAuth():
    return render_template('manager/restauth.html')

@managers.route('/login', methods=['GET', 'POST'])
def mlogin():
    form = SALoginForm()
    return render_template('manager/login.html', form=form)


@managers.route('/mdashboard', methods=['GET', 'POST'])
def mDashboard():
    accounts = Account.query.all()

    form = AccountForm()
    forms = EditAccountForm()

    if form.validate_on_submit():  # Check if form is submitted and validated
        # Extract data from the form
        account_name = form.account_name.data
        owner = form.owner.data
        phone = form.phone.data
        email = form.email.data
        location = form.location.data
        password = form.password.data

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create a new Account instance
        new_account = Account(
            account_name=account_name,
            owner=owner,
            phone=phone,
            email=email,
            location=location,
            password=hashed_password,
            status="Active"  # You can set a default status or manage dynamically
        )

        # Save the new account to the database
        try:
            db.session.add(new_account)
            db.session.commit()
            flash("Account successfully created!", "success")
            return redirect(url_for('managers.mDashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "danger")

    return render_template('manager/dashboard.html', form=form, forms=forms, accounts=accounts)

@managers.route('/edit_account/<int:account_id>', methods=['GET', 'POST'])
def edit_account(account_id):
    # Fetch the account or return 404 if not found
    account = Account.query.get_or_404(account_id)

    # Initialize the form, pre-populated with current account data
    form = EditAccountForm(obj=account)

    if request.method == 'POST':
        if form.validate_on_submit():
            # Update the account with new values from the form
            form.populate_obj(account)

            try:
                # Commit changes to the database
                db.session.commit()
                flash('Account updated successfully!', 'success')
                return redirect(url_for('managers.mDashboard'))  # Adjust URL if needed
            except Exception as e:
                db.session.rollback()
                flash(f'Error updating account: {e}', 'danger')

    # Render the edit account form
    return render_template('manager/edit_acc.html', form=form, account=account)


@managers.route('/delete_account/<int:id>', methods=['DELETE'])
def delete_account(id):
    account = Account.query.get(id)
    if account:
        db.session.delete(account)
        db.session.commit()
        return '', 204  # No content, successfully deleted
    return 'Account not found', 404

@managers.route('/crudrest', methods=['GET', 'POST'])
def crudrest():
    form = CreateRestaurantForm()
    return render_template('manager/crudrest.html',form=form)

@managers.route('/staff', methods=['GET', 'POST'])
def staff():
    forms = StaffForm()
    form = EditStaffForm()
    return render_template('manager/staff.html',form=form, forms=forms)

@managers.route('/deps', methods=['GET', 'POST'])
def deps():
    forms = AddDepartmentForm()
    form = EditDepartmentForm()
    return render_template('manager/deps.html',form=form, forms=forms)

@managers.route('/cat', methods=['GET', 'POST'])
def cat():
    forms = AddCatForm()
    form = EditCattForm()
    return render_template('manager/cat.html',form=form, forms=forms)

@managers.route('/dcat', methods=['GET', 'POST'])
def dcat():
    forms = AddDCatForm()
    form = EditDCattForm()
    return render_template('manager/dcat.html',form=form, forms=forms)


@managers.route('/manager-obr-report', methods=['GET', 'POST'])
def lsd_obr_report():
    return render_template('manager/lsd-obr-report.html')

@managers.route('/atr-obr-report', methods=['POST', 'GET'])
def atr_obr_report():
    return render_template('manager/atr-obr-report.html')

@managers.route('/shiftOne', methods=['POST', 'GET'])
def shiftOne():
    return render_template('manager/shift1.html')

@managers.route('/shiftTwo', methods=['POST', 'GET'])
def shiftTwo():
    return render_template('manager/shift2.html')

@managers.route('/stockStatus')
def stockStatus():
    return render_template('manager/stock-status.html')

@managers.route('/myMenu')
def myMenu():
    return render_template('manager/mymenu.html')

@managers.route('/crnt-sup', methods=['POST', 'GET'])
def crnt_sup():
    last_supplies = [
        {'product_name': 'Olive Oil', 'product_type': 'Ingredient', 'quantity': 20, 'price_bought': 50, 'supplier_name': 'Fresh Produce Inc.', 'time_supplied': '2024-11-05 14:30', 'recorded_by': 'Store Manager'},
        {'product_name': 'Beer', 'product_type': 'Ready Product', 'quantity': 100, 'price_bought': 200, 'supplier_name': 'Beverages Ltd.', 'time_supplied': '2024-11-04 12:00', 'recorded_by': 'Restaurant Owner'},
        {'product_name': 'Tomato Sauce', 'product_type': 'Ingredient', 'quantity': 30, 'price_bought': 60, 'supplier_name': 'Condiments Co.', 'time_supplied': '2024-11-03 10:00', 'recorded_by': 'Store Manager'},
        {'product_name': 'Pasta', 'product_type': 'Ingredient', 'quantity': 50, 'price_bought': 40, 'supplier_name': 'Italian Goods', 'time_supplied': '2024-11-02 09:30', 'recorded_by': 'Store Manager'},
        {'product_name': 'Soda', 'product_type': 'Ready Product', 'quantity': 200, 'price_bought': 150, 'supplier_name': 'Beverages Ltd.', 'time_supplied': '2024-11-01 14:00', 'recorded_by': 'Restaurant Owner'},
        {'product_name': 'Bottled Water', 'product_type': 'Ready Product', 'quantity': 300, 'price_bought': 100, 'supplier_name': 'Aqua Suppliers', 'time_supplied': '2024-10-31 16:00', 'recorded_by': 'Store Manager'},
        {'product_name': 'Cheese', 'product_type': 'Ingredient', 'quantity': 25, 'price_bought': 75, 'supplier_name': 'Dairy Farmers', 'time_supplied': '2024-10-30 11:00', 'recorded_by': 'Store Manager'},
        {'product_name': 'Wine', 'product_type': 'Ready Product', 'quantity': 50, 'price_bought': 500, 'supplier_name': 'Vineyard Co.', 'time_supplied': '2024-10-29 15:30', 'recorded_by': 'Restaurant Owner'},
        {'product_name': 'Chicken', 'product_type': 'Ingredient', 'quantity': 40, 'price_bought': 200, 'supplier_name': 'Poultry Farms', 'time_supplied': '2024-10-28 13:00', 'recorded_by': 'Store Manager'},
        {'product_name': 'Flour', 'product_type': 'Ingredient', 'quantity': 100, 'price_bought': 50, 'supplier_name': 'Grain Suppliers', 'time_supplied': '2024-10-27 10:30', 'recorded_by': 'Store Manager'}
    ]
    return render_template('manager/crnt-sup.html', last_supplies=last_supplies)

    