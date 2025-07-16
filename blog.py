from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app as app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from ext import db
from forms import ChoiceForm, ReviewForm, QuoteForm
from models import Book, Review, Quote

blog = Blueprint("blog", __name__)

@blog.route('/my-blog', methods=['GET', 'POST'])
@login_required
def my_blog():
    post_type = request.args.get('type')  # 'review' ან 'quote'

    choice_form = ChoiceForm()
    review_form = ReviewForm()
    quote_form = QuoteForm()

    if request.method == 'POST':
        if post_type == 'review' and review_form.validate_on_submit():
            # ახალი წიგნი ან მოძებნა
            book_title = review_form.book_title.data.strip()
            book_author = review_form.book_author.data.strip()
            book = Book.query.filter_by(title=book_title, author=book_author).first()
            if not book:
                book = Book(title=book_title, author=book_author)
                db.session.add(book)
                db.session.commit()

            # სურათის შენახვა
            filename = None
            if review_form.image.data:
                filename = secure_filename(review_form.image.data.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                review_form.image.data.save(image_path)

            # რეცენზიის შენახვა
            review = Review(
                content=review_form.content.data,
                genre=review_form.genre.data,
                image=filename,
                user_id=current_user.id,
                book_id=book.id
            )
            db.session.add(review)
            db.session.commit()
            flash("რეცენზია დაემატა!", "success")
            return redirect(url_for('blog.my_blog'))

        elif post_type == 'quote' and quote_form.validate_on_submit():
            quote = Quote(
                text=quote_form.text.data,
                author=quote_form.author.data,
                book_title=quote_form.book_title.data.strip(),
                user_id=current_user.id
            )
            db.session.add(quote)
            db.session.commit()
            flash("ციტატა დაემატა!", "success")
            return redirect(url_for('blog.my_blog'))

    # რეცენზიების/ციტატების ჩვენება
    reviews = Review.query.filter_by(user_id=current_user.id).all()
    quotes = Quote.query.filter_by(user_id=current_user.id).all()
    review_count = len(reviews)
    quote_count = len(quotes)
    is_critic = review_count >= 5

    return render_template("my_blog.html",
        choice_form=choice_form,
        review_form=review_form,
        quote_form=quote_form,
        reviews=reviews,
        quotes=quotes,
        review_count=review_count,
        quote_count=quote_count,
        is_critic=is_critic,
        post_type=post_type
    )

@blog.route('/all-blogs')
def all_blogs():
    posts = Review.query.order_by(Review.timestamp.desc()).all()
    return render_template("all_blogs.html", posts=posts)

@blog.route("/book/<int:book_id>")
def book_reviews(book_id):
    book = Book.query.get_or_404(book_id)
    reviews = Review.query.filter_by(book_id=book.id).order_by(Review.timestamp.desc()).all()
    quotes = Quote.query.filter_by(book_id=book.id).all()
    return render_template("book_reviews.html", book=book, reviews=reviews, quotes=quotes)
