from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from ext import db
from models import Review, Book, Quote
from forms import ReviewForm, QuoteForm
import os

upload = Blueprint("upload", __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@upload.route("/upload-choice")
@login_required
def upload_choice():
    return render_template("upload_choice.html")

@upload.route("/upload-review", methods=["GET", "POST"])
@login_required
def upload_review():
    form = ReviewForm()

    if form.validate_on_submit():
        book = Book.query.filter_by(
            title=form.book_title.data.strip(),
            author=form.book_author.data.strip()
        ).first()

        if not book:
            book = Book(
                title=form.book_title.data.strip(),
                author=form.book_author.data.strip()
            )
            db.session.add(book)
            db.session.commit()

        filename = None
        if form.image.data:
            file = form.image.data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
                file.save(image_path)
            else:
                flash("მხოლოდ .png, .jpg, .jpeg, .gif ფაილებია დასაშვები!", "danger")


                return render_template("upload_review.html", form=form)

        review = Review(
            content=form.content.data,
            genre=form.genre.data,
            image=filename,
            user_id=current_user.id,
            book_id=book.id
        )
        db.session.add(review)
        db.session.commit()
        flash("რეცენზია აიტვირთა!", "success")
        return redirect(url_for("blog.my_blog"))

    return render_template("upload_review.html", form=form)

@upload.route("/upload-quote", methods=["GET", "POST"])
@login_required
def upload_quote():
    form = QuoteForm()
    if form.validate_on_submit():
        book = Book.query.filter_by(title=form.book_title.data.strip()).first()
        if not book:
            book = Book(title=form.book_title.data.strip(), author="უცნობი")
            db.session.add(book)
            db.session.commit()

        quote = Quote(
            text=form.quote_text.data,
            book_title=form.book_title.data,
            user_id=current_user.id,
            book_id=book.id
        )
        db.session.add(quote)
        db.session.commit()
        flash("ციტატა აიტვირთა!", "success")
        return redirect(url_for("blog.my_blog"))

    return render_template("upload_quote.html", form=form)






