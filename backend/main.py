from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages

from itea_library.library import Library
from itea_library.library_storage.sqlstorage.sqlstorage import SQLStorage

from email_validator import validate_email
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

import os

# from dotenv import load_dotenv
# load_dotenv('.env')

app = Flask(__name__,
            template_folder='../site/templates',
            static_folder='../site/static')

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'a very very secret string =)'

login_manager = LoginManager(app)
login_manager.login_view = 'api_login'


@login_manager.user_loader
def load_user(user_id):
    return lib.get_reader_by_id(user_id)


storage = SQLStorage(
    db_user='postgres',
    db_password='123',
    db_name='postgres',
    db_address='localhost',
    db_port=5432
)

lib = Library(storage)
if not lib.get_all_books():
    lib.load_books_from_txt_file('books.txt', sep='$!$')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/books', methods=['GET'])
def api_get_all_books():
    page = request.args.get('page')
    if not page or page.isnumeric() or int(page) < 1:
        page = 1

    sort = request.args.get('sort')
    if not sort:
        sort = 'id'

    return render_template('books.html',
                           books=lib.get_several_book(page=int(page) - 1, page_size=3),
                           page_count=len(lib.get_all_books()) // 3,
                           current_page=int(page),
                           sort=sort)


    @app.route('/add_book', methods=['GET', 'POST'])
    @login_required  # декоратор опаределяющий то что не доступно не зарегестрироаным юзерам
    def api_add_book():
        if request.method == 'POST':
            title_book = request.form.get('title')
            author_book = request.form.get('author')
            year_book = request.form.get('year')

            if not (title_book and author_book and year_book):
                flash('Введены некорректные данные', 'error')
                return render_template('add_book.html')
            if not year_book.isnumeric():
                flash('Введен некорректный год издания!', 'error')
                return render_template('add_book.html')

            ret_code, ret_msg = lib.add_book(title_book, author_book, int(year_book))
            flash(ret_msg, 'done')
            return render_template('add_book.html')

        return render_template('add_book.html')

    @app.route('/delete_book', methods=['GET', 'POST'])
    @login_required
    def api_delete_book():
        if request.method == 'POST':
            id_books = [int(i) for i in request.form.keys() if i.isnumeric()]

            if len(id_books):
                ret_msg = lib.remove_books(id_books)
                flash(ret_msg, 'done')
                return render_template('delete_book.html',
                                       books=sorted(lib.get_all_books(), key=lambda book: book.id))

        return render_template('delete_book.html', books=sorted(lib.get_all_books(), key=lambda book: book.id))

    @app.route('/take_book', methods=['GET', 'POST'])
    @login_required
    def api_take_book():
        if request.method == 'POST':
            id_books = [int(i) for i in request.form.keys() if i.isnumeric()]

            if len(id_books):
                message = lib.give_books(id_books, current_user.get_id())
                if message:
                    flash(message, 'error')

                return render_template('take_book.html',
                                       books=sorted(lib.get_available_books(), key=lambda book: book.id))

        return render_template('take_book.html', books=sorted(lib.get_available_books(), key=lambda book: book.id))

    @app.route('/return_book', methods=['GET', 'POST'])
    @login_required
    def api_return_book():
        if request.method == 'POST':
            id_books = [int(i) for i in request.form.keys() if i.isnumeric()]

            if len(id_books):
                message = lib.return_books(id_books, current_user.get_id())
                if message:
                    flash(message, 'error')
                return render_template('return_book.html',
                                       books=sorted(lib.get_all_book_from_reader(current_user.get_id()),
                                                    key=lambda book: book.id))

        return render_template('return_book.html',
                               books=sorted(lib.get_all_book_from_reader(current_user.get_id()),
                                            key=lambda book: book.id))

    @app.route('/registration', methods=['GET', 'POST'])
    def api_registration():
        if current_user.is_authenticated:  # если зареганый юзер захочет попасть на форму регистрации
            return redirect(url_for('index'))

        if request.method == 'POST':
            email = request.form.get('email')
            psw = request.form.get('psw')
            name = request.form.get('name')
            surname = request.form.get('surname')
            year = request.form.get('year')

            if not (email and psw and name and surname and year):
                flash('Введены некоректные данные!', 'error')
                return render_template('registration.html')
            if not year.isnumeric():
                flash('Введён некоректный год рождения!', 'error')
                return render_template('registration.html')

            try:
                validate_email(email)
            except:
                flash('Введён некоректный email!', 'error')
                return render_template('registration.html')

            if lib.get_reader_by_email(email):
                flash('Введён некоректный email! Уже существует!', 'error')
                return render_template('registration.html')

            if lib.add_reader(name, surname, year, email, psw):
                flash("Теперь вы можете войти 😁", 'done')
                return redirect(url_for('api_login'))
            else:
                flash('Произощла неизвестная ошибка!', 'error')
                return render_template('registration.html')

        return render_template('registration.html')

    @app.route('/login', methods=['GET', 'POST'])
    def api_login():
        if current_user.is_authenticated:  # если зареганый юзер захочет попасть
            return redirect(url_for('index'))

        if request.method == 'POST':
            email = request.form.get('email')
            psw = request.form.get('psw')
            next_url = request.args.get('next')

            if not (email and psw):
                flash('Введены некоректные данныые!', 'error')
                return render_template('login.html')

            reader = lib.get_reader_by_email(email)
            if reader and reader.check_psw(psw):
                login_user(reader)

                if next_url:
                    return redirect(next_url)

                return redirect(url_for('index'))

            else:
                flash('Введён неверный пароль!', 'error')
                return render_template('login.html')

        return render_template('login.html')

    @app.route('/logout', methods=['GET'])
    @login_required
    def api_logout():
        logout_user()
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
