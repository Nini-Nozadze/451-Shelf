import os
from werkzeug.utils import secure_filename
from flask import current_app
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_user, logout_user, login_required
from models import User, Review, Quote
from forms import LoginForm, RegistrationForm
from ext import db
from functools import wraps



auth = Blueprint("auth", __name__)



@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        image_filename = None
        if form.profile_picture.data:
            file = form.profile_picture.data
            filename = secure_filename(file.filename)

            upload_dir = os.path.join(current_app.root_path, 'static/uploads')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)

            upload_path = os.path.join(upload_dir, filename)
            file.save(upload_path)

            image_filename = filename

        user = User(username=form.username.data, email=form.email.data, image=image_filename)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))

    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.home'))


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@auth.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)


@auth.route('/admin/delete_review/<int:review_id>', methods=['POST'])
@login_required
@admin_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    flash('Review deleted.')
    return redirect(url_for('auth.admin_dashboard'))


@auth.route('/admin/delete_quote/<int:quote_id>', methods=['POST'])
@login_required
@admin_required
def delete_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    db.session.delete(quote)
    db.session.commit()
    flash('ციტატა წაიშალა.')
    return redirect(url_for('auth.admin_dashboard'))
