from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..models import User, Category
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    categories = Category.query.all()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logado com sucesso.', category='success')
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash('Senha incorreta. Por favor tente novamente.', category='error')
        else:
            flash('E-mail não existe.', category='error')

    return render_template("login.html", user=current_user, categories=categories)

@auth.route('/esqueceu-senha', methods=['GET', 'POST'])
def forget():
    categories = Category.query.all()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if password != password2:
            flash('Senhas não batem.', category='error')
        elif len(password) < 4: 
            flash('Senha deve conter pelo menos 5 caractéres.', category='error')
        else:
            user.password = generate_password_hash(password, method='sha256')
            db.session.commit()
            login_user(user, remember=True)
            flash('Senha alterada com sucesso!', category='success')

            return redirect(url_for('views.home'))

    return render_template("forget.html", user=current_user, categories=categories)

@auth.route('/logout')
@login_required
def logout():
    flash('Deslogado com sucesso!', category='success')
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/cadastro', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('E-mail já existe.', category='error')
        elif len(first_name) < 2:
            flash('Nome deve ser pelo menos 3 caractéres.', category='error')
        elif len(last_name) < 2:
            flash('Sobrenome deve ser pelo menos 3 caractéres.', category='error')
        elif password != password2:
            flash('Senhas não batem.', category='error')
        elif len(password) < 4: 
            flash('Senha deve conter pelo menos 5 caractéres.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password, method='sha256'), is_admin=False)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Conta criada!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)