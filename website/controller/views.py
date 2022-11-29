from flask import Blueprint, flash, render_template, request, flash, redirect, url_for
from ..models import Category, Product, User
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

import urllib.request
import os
import collections
import datetime
import json

from .. import db

views = Blueprint('views', __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg','jpeg'])
UPLOAD_FOLDER = './website/static/img'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

def allowed_file(filetype):
    aux = filetype.rsplit('/',1)[1].lower()
    return '/' in filetype and aux in ALLOWED_EXTENSIONS

def get_filetype(filetype):
    return filetype.rsplit('/',1)[1].lower()

@views.route('/', methods=['GET', 'POST'])
def home():
    categories = Category.query.all()
    # if (len(categories) == 0):
    #     db.session.add(Category(id=1, name="Ação"))
    #     db.session.add(Category(id=2, name="Aventura"))

    #     db.session.add(Product(id=1, name="Jogo 1", description="Descrição do jogo 1", category_id=1))
    #     db.session.add(Product(id=2, name="Jogo 2", description="Descrição do jogo 2", category_id=1))
    #     db.session.add(Product(id=3, name="Jogo 3", description="Descrição do jogo 3", category_id=2))
    #     db.session.add(Product(id=4, name="Jogo 4", description="Descrição do jogo 4", category_id=1))
    #     db.session.add(Product(id=5, name="Jogo 5", description="Descrição do jogo 5", category_id=1))
    #     db.session.add(Product(id=6, name="Jogo 6", description="Descrição do jogo 6", category_id=2))
    #     db.session.add(Product(id=7, name="Jogo 7", description="Descrição do jogo 7", category_id=1))
    #     db.session.add(Product(id=8, name="Jogo 8", description="Descrição do jogo 8", category_id=1))
    #     db.session.add(Product(id=9, name="Jogo 9", description="Descrição do jogo 9", category_id=2))
        
    #     db.session.add(Subcategory(id=1, name="Ação em 3ª pessoa", product_id=1))
    #     db.session.add(Subcategory(id=2, name="Simulador", product_id=1))
    #     db.session.add(Subcategory(id=3, name="Ação em 1ª pessoa", product_id=2))
    #     db.session.add(Subcategory(id=4, name="Hack & Slash", product_id=2))
    #     db.session.add(Subcategory(id=5, name="Casual", product_id=3))
    #     db.session.add(Subcategory(id=6, name="RPG", product_id=3))

    #     db.session.commit()


    #     categories.append(Category(id=1, name="Ação"))

    return render_template("home.html", user=current_user, categories=categories)

@views.route('/categoria', methods=['GET', 'POST'])
def category():
    id_category = request.args.get('id')
    categories = Category.query.all()
    # if id_categoria:
    #     categorias = Category.query.filter_by(id=id_categoria)
    # else:
    #     categorias = Category.query.all()

    return render_template("category.html", user=current_user, id_category=id_category, categories=categories)

@views.route('/produtos-detalhes', methods=['GET', 'POST'])
@login_required
def product_details():
    id_product = request.args.get('id')
    product = Product.query.get(id_product)
    categories_product = Category.query.filter_by(id = product.category_id)
    categories = Category.query.all()

    return render_template("product_details.html", user=current_user, categories=categories, categories_product=categories_product, product=product)

@views.route('/sobre')
@login_required
def about():
    categories = Category.query.all()

    return render_template("about.html", user=current_user, categories=categories)


@views.route('/conta', methods=['GET', 'POST'])
@login_required
def account():
    id_user = request.args.get('id')
    user = User.query.filter_by(id=id_user).first()
    categories = Category.query.all()
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password') if request.form.get('password') != '' else None
        password2 = request.form.get('password2') if request.form.get('password2') != '' else None

        user = User.query.filter_by(email=email).first()
        
        if len(first_name) < 2:
            flash('Nome deve ser pelo menos 3 caractéres.', category='error')
        elif len(last_name) < 2:
            flash('Sobrenome deve ser pelo menos 3 caractéres.', category='error')
        elif password != password2:
            flash('Senhas não batem.', category='error')
        elif password != None and len(password) < 4: 
            flash('Senha deve conter pelo menos 5 caractéres.', category='error')
        else:
            user.email=email
            user.first_name=first_name
            user.last_name=last_name
            if(password != None):
                user.password=generate_password_hash(password, method='sha256')
            db.session.commit()
            flash('Dados alterados com sucesso!', category='success')
            return redirect(url_for('views.home'))

    return render_template("account.html", user=current_user, categories=categories)

@views.route('/admin', methods=['GET','POST'])
@login_required
def admin():
    categories = Category.query.all()

    return render_template("admin.html", user=current_user, categories=categories)

@views.route('/adm-prod-editar', methods=['GET', 'POST'])
@login_required
def adm_products_edit():

    id_product = request.args.get('id')
    product = Product.query.get(id_product)
    categories_product = Category.query.filter_by(id = product.category_id)
    categories = Category.query.all()

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        studio = request.form.get('studio')
        date_launch = request.form.get('date_launch')
        price = request.form.get('price')
        category = request.form.get('prod_categ')

        product.name=name
        product.description=description
        product.studio=studio
        product.date_launch=datetime.datetime.strptime(date_launch, '%Y-%m-%d')
        product.price=price
        product.name=name
        product.category_id = category

        file = request.files['prod_img']
        if file and allowed_file(file.mimetype):
            file.filename = str(product.id) + '.' +  get_filetype(file.mimetype)
            filename = secure_filename(file.filename)
            file.save(UPLOAD_FOLDER + '/' + filename)
            product.file_type=get_filetype(file.mimetype)

        db.session.commit()
        flash('Produto alterado com sucesso!', category='success')
        return redirect(url_for('views.admin'))


    return render_template("adm_prod_edit.html", user=current_user, categories=categories, categories_product=categories_product, product=product)

@views.route('/adm-prod-adicionar', methods=['GET', 'POST'])
@login_required
def adm_products_add():

    categories = Category.query.all()

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        studio = request.form.get('studio')
        date_launch = request.form.get('date_launch')
        price = request.form.get('price')
        category = request.form.get('prod_categ')

        new_product = Product(name=name,description=description, studio=studio, date_launch=datetime.datetime.strptime(date_launch, '%Y-%m-%d'), price=price, category_id=category)
        db.session.add(new_product)            
        db.session.flush()
        db.session.refresh(new_product)

        file = request.files['prod_img']
        if file and allowed_file(file.mimetype):
            file.filename = str(new_product.id) + '.' +  get_filetype(file.mimetype)
            filename = secure_filename(file.filename)
            file.save(UPLOAD_FOLDER + '/' + filename)
            new_product.file_type=get_filetype(file.mimetype)

        db.session.commit()
        flash('Produto alterado com sucesso!', category='success')
        return redirect(url_for('views.admin'))


    return render_template("adm_prod_add.html", user=current_user, categories=categories)

@views.route('/adm-prod-importar', methods=['GET', 'POST'])
@login_required
def adm_products_import():

    categories = Category.query.all()

    if request.method == 'POST':
        file = request.files['prod_import']

        db.session.execute('DELETE FROM product')

        content = json.loads(file.read())
        # new_product = Product(name=name,description=description, studio=studio, date_launch=datetime.datetime.strptime(date_launch, '%Y-%m-%d'), price=price, category_id=category)

        for product in content['product']:
            new_product = Product(name=product["name"],status=product["status"],description=product["description"],price=product["price"],category_id=product["category_id"],studio=product["studio"],date_launch=datetime.datetime.strptime(product["date_launch"], '%Y-%m-%d'))
            db.session.add(new_product)


        db.session.commit()

        flash('Produtos importados com sucesso!', category='success')
        return redirect(url_for('views.admin'))


    return render_template("adm_prod_import.html", user=current_user, categories=categories)


