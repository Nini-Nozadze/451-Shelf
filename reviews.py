from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

from ext import db
from models import Review, Book
from forms import ReviewForm

reviews = Blueprint("reviews", __name__)

@reviews.route("/add_review/<int:book_id>", methods=["GET", "POST"])
@login_required
def add_review(book_id):
    form = ReviewForm()
    book = Book.query.get_or_404(book_id)

    if form.validate_on_submit():
        image_filename = None

        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            image_path = os.path.join(current_app.root_path, 'static/uploads', filename)
            form.image.data.save(image_path)
            image_filename = filename

        new_review = Review(
            content=form.content.data,
            genre=form.genre.data,
            image=image_filename,
            user_id=current_user.id,
            book_id=book.id
        )
        db.session.add(new_review)
        db.session.commit()
        flash("რეცენზია წარმატებით დაემატა!")
        return redirect(url_for("main.home"))

    return render_template("add_review.html", form=form, book=book)
