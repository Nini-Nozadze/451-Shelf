from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from models import User, Book, Review, Quote
from flask_login import login_required, current_user
from ext import db
from sqlalchemy import func
from functools import wraps
from flask import abort

main = Blueprint("main", __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@main.route("/")
def home():
    popular_books = (
        Book.query
        .outerjoin(Review)
        .group_by(Book.id)
        .order_by(func.count(Review.id).desc())
        .limit(3)
        .all()
    )

    popular_quotes = Quote.query.order_by(Quote.likes.desc()).limit(3).all()
    popular_reviews = sorted(Review.query.all(), key=lambda r: len(r.liked_by_users), reverse=True)[:3]

    top_critics = (
        User.query
        .join(Review)
        .group_by(User.id)
        .having(func.count(Review.id) >= 20)
        .order_by(func.count(Review.id).desc())
        .limit(3)
        .all()
    )
    top_quoters = (
        User.query
        .join(Quote)
        .group_by(User.id)
        .having(func.count(Quote.id) >= 20)
        .order_by(func.count(Quote.id).desc())
        .limit(3)
        .all()
    )

    return render_template(
        'home.html',
        popular_books=popular_books,
        popular_quotes=popular_quotes,
        popular_reviews=popular_reviews,
        top_critics=top_critics,
        top_quoters=top_quoters
    )


@main.route("/books/<int:book_id>")
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    reviews = Review.query.filter_by(book_id=book.id).order_by(Review.timestamp.desc()).all()
    quotes = Quote.query.filter_by(book_id=book.id).order_by(Quote.likes.desc()).all()
    return render_template("book.html", book=book, reviews=reviews, quotes=quotes)


@main.route('/popular')
def popular():
    reviews = sorted(Review.query.all(), key=lambda r: len(r.liked_by_users), reverse=True)
    quotes = sorted(Quote.query.all(), key=lambda q: len(q.liked_by_users), reverse=True)
    return render_template('popular.html', reviews=reviews, quotes=quotes)



@main.route('/top-critics')
def top_critics():
    critics = (
        User.query
        .join(Review)
        .group_by(User.id)
        .having(db.func.count(Review.id) >= 0)
        .order_by(db.func.count(Review.id).desc())
        .all()
    )
    return render_template("top_critics.html", critics=critics)


@main.route("/top-quoters")
def top_quoters():
    users = User.query.all()
    quoters = [user for user in users if user.quote_count >= 0]
    quoters.sort(key=lambda u: u.quote_count, reverse=True)
    return render_template("top_quoters.html", quoters=quoters)


@main.route('/quotes/author/<username>')
def quotes_by_author(username):
    user = User.query.filter_by(username=username).first_or_404()
    quotes = Quote.query.filter_by(user_id=user.id).all()
    return render_template('quotes_by_author.html', user=user, quotes=quotes)


@main.route("/quote/<int:quote_id>")
def view_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    return render_template("view_quote.html", quote=quote)


@main.route("/quotes")
def all_quotes():
    quotes = Quote.query.order_by(Quote.timestamp.desc()).all()
    return render_template("all_quotes.html", quotes=quotes)


@main.route("/about")
def about():
    return render_template("about.html")


@main.route('/favorites')
@login_required
def favorites():
    favorite_reviews = current_user.favorite_reviews
    favorite_quotes = current_user.favorite_quotes
    return render_template('favorites.html', favorite_reviews=favorite_reviews, favorite_quotes=favorite_quotes)


@main.route('/search')
def search():
    query = request.args.get('q', '')
    results = Book.query.filter(Book.title.ilike(f"%{query}%")).all() if query else []
    return render_template("search_results.html", query=query, results=results)


@main.route('/toggle_favorite_review/<int:review_id>', methods=['POST'])
@login_required
def toggle_favorite_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review in current_user.favorite_reviews:
        current_user.favorite_reviews.remove(review)
        flash('ფავორიტებიდან წაიშალა.')
    else:
        current_user.favorite_reviews.append(review)
        flash('ფავორიტებში დაემატა.')
    db.session.commit()
    return redirect(request.referrer or url_for('main.home'))


@main.route('/favorite/quote/<int:quote_id>', methods=['POST'])
@login_required
def toggle_favorite_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    if quote in current_user.favorite_quotes:
        current_user.favorite_quotes.remove(quote)
        flash('ციტატა ფავორიტებიდან წაიშალა.')
    else:
        current_user.favorite_quotes.append(quote)
        flash('ციტატა ფავორიტებში დაემატა.')
    db.session.commit()
    return redirect(request.referrer or url_for('main.home'))




@main.route('/reviews/<username>')
def reviews_by_author(username):
    user = User.query.filter_by(username=username).first_or_404()
    reviews = Review.query.filter_by(user_id=user.id).all()
    return render_template("reviews_by_author.html", user=user, reviews=reviews)



@main.route('/review/<int:review_id>/delete', methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    if current_user.is_admin or current_user.id == review.user_id:
        db.session.delete(review)
        db.session.commit()
        flash("რეცენზია წარმატებით წაიშალა.")
    else:
        flash("თქვენ არ გაქვთ წაშლის უფლება.")
    return redirect(url_for('main.home'))


@main.route('/quote/<int:quote_id>/delete', methods=['POST'])
@login_required
def delete_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    if current_user.is_admin or current_user.id == quote.user_id:
        db.session.delete(quote)
        db.session.commit()
        flash("ციტატა წარმატებით წაიშალა.")
    else:
        flash("თქვენ არ გაქვთ წაშლის უფლება.")
    return redirect(url_for('main.home'))


@main.route('/review/<int:review_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)
    if not (current_user.is_admin or current_user.id == review.user_id):
        flash("თქვენ არ გაქვთ რედაქტირების უფლება.")
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        review.content = request.form['content']
        review.genre = request.form['genre']
        db.session.commit()
        flash("რეცენზია წარმატებით განახლდა.")
        return redirect(url_for('main.book_detail', book_id=review.book_id))


    return render_template('edit_review.html', review=review)



@main.route('/quote/<int:quote_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_quote(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    if not (current_user.is_admin or current_user.id == quote.user_id):
        flash("თქვენ არ გაქვთ რედაქტირების უფლება.")
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        quote.text = request.form['text']
        db.session.commit()
        flash("ციტატა წარმატებით განახლდა.")
        return redirect(url_for('main.book_detail', book_id=review.book_id))


    return render_template('edit_quote.html', quote=quote)
