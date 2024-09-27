import os
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from src.entity.forms import RegistrationForm, LoginForm, PasswordResetRequestForm, PasswordResetForm
from src.entity.models import User
from src.db import db

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            if not user.verified:
                flash("Please verify your account before logging in.")
                return redirect(url_for('auth.login'))
            login_user(user)
            return redirect(url_for('main.product_list'))
        flash("Invalid email or password.")
    return render_template('login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        send_verification_email(user)
        flash("Registration successful. Please check your email to verify your account.")
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.product_list'))


def send_verification_email(user):
    from app import mail
    token = user.generate_confirmation_token()
    msg = Message('Confirm Your Email', sender=os.getenv('MAIL_USERNAME'), recipients=[user.email])
    msg.body = f'Please confirm your email by clicking the following link: {url_for("auth.confirm_email", token=token, _external=True)}'
    mail.send(msg)


@bp.route('/confirm_email/<token>')
def confirm_email(token):
    email = User.confirm_token(token)
    if not email:
        flash('The confirmation link is invalid or has expired.')
        return redirect(url_for('main.product_list'))

    user = User.query.filter_by(email=email).first_or_404()
    if user.verified:
        flash('Account already verified. Please log in.')
    else:
        user.verified = True
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    return redirect(url_for('auth.login'))


@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash("If your email is registered, you will receive a password reset link.")
        return redirect(url_for('auth.login'))
    return render_template('reset_request.html', form=form)


def send_reset_email(user):
    from app import mail
    token = user.generate_confirmation_token()
    msg = Message('Password Reset Request', sender=os.getenv('MAIL_USERNAME'), recipients=[user.email])
    msg.body = f'Reset your password by clicking the following link: {url_for("auth.reset_token", token=token, _external=True)}'
    mail.send(msg)



@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    email = User.confirm_token(token)
    if not email:
        flash('The reset link is invalid or has expired.')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first_or_404()
    form = PasswordResetForm()
    if request.method == 'POST':
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been updated!')
        return redirect(url_for('auth.login'))

    return render_template('reset_token.html', form=form, token=token)