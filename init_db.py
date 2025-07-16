from app import create_app
from ext import db
from models import User, Book, Review, Quote

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # მომხმარებლები
    user1 = User(username="mkitxveli123", email="mkitxveli123@example.com", password_hash="dummy")
    user2 = User(username="elo_reader", email="elo_reader@example.com", password_hash="dummy")
    user3 = User(username="newbie_critic", email="newbie@example.com", password_hash="dummy")

    # წიგნები
    book1 = Book(title="1984", author="George Orwell", cover_url="/static/1984.jpg")
    book2 = Book(title="ვეფხისტყაოსანი", author="შოთა რუსთაველი", cover_url="/static/vefxistkaosani.jpg")
    book3 = Book(title="Dune", author="Frank Herbert", cover_url="/static/dune.jpg")

    # რევიუები
    review1 = Review(content="ძალიან საინტერესო წიგნია!", genre="მხატვრული", user=user1, book=book1)
    review2 = Review(content="არ ველოდი ასეთ ფინალს.", genre="მხატვრული", user=user1, book=book2)
    review3 = Review(content="შესანიშნავი სამეცნიერო ფანტასტიკა", genre="სამეცნიერო", user=user2, book=book3)
    review4 = Review(content="პროლოგი ცოტა გაიწელა", genre="სამეცნიერო", user=user3, book=book3)

    # ციტატები
    quote1 = Quote(text="War is peace. Freedom is slavery. Ignorance is strength.",
                   author="George Orwell", book_title="1984", user=user1, book=book1, likes=15)

    quote2 = Quote(text="ქვეყნის ძლიერება სამართალშია.",
                   author="შოთა რუსთაველი", book_title="ვეფხისტყაოსანი", user=user2, book=book2, likes=10)

    quote3 = Quote(text="Fear is the mind-killer.",
                   author="Frank Herbert", book_title="Dune", user=user3, book=book3, likes=25)

    admin_user = User(username='editor', email='admineditor@example.com')
    image = 'default.png'
    admin_user.set_password('87654321')
    admin_user.is_admin = True
    db.session.add(admin_user)
    db.session.commit()

    db.session.add_all([user1, user2, user3,admin_user, book1, book2, book3,
                        review1, review2, review3, review4,
                        quote1, quote2, quote3])
    db.session.commit()

    print(" მონაცემები წარმატებით ჩაიტვირთა.")

