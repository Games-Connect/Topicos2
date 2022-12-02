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

@views.route('/admin-produto', methods=['GET','POST'])
@login_required
def admin_product():
    return render_template("admin_product.html", user=current_user, categories=Category.query.all())

@views.route('/admin-produto-editar', methods=['GET', 'POST'])
@login_required
def admin_product_edit():

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
        return redirect(url_for('views.admin_product'))


    return render_template("admin_prod_edit.html", user=current_user, categories=categories, categories_product=categories_product, product=product)

@views.route('/admin-prod-adicionar', methods=['GET', 'POST'])
@login_required
def admin_products_add():

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
        flash('Produto adicionado com sucesso!', category='success')
        return redirect(url_for('views.admin_product'))


    return render_template("admin_prod_add.html", user=current_user, categories=Category.query.all())

@views.route('/admin-produto-remover', methods=['GET', 'POST'])
@login_required
def admin_product_delete():

    id_product = request.args.get('id')
    product = Product.query.get(id_product)

    db.session.delete(product)  
    db.session.commit()
    flash('Jogo removida com sucesso!', category='success')
    return redirect(url_for('views.admin_product'))

@views.route('/admin-prod-importar', methods=['GET', 'POST'])
@login_required
def admin_products_import():

    categories = Category.query.all()

    if request.method == 'POST':
        file = request.files['prod_import']

        content = json.loads(file.read())
        # new_product = Product(name=name,description=description, studio=studio, date_launch=datetime.datetime.strptime(date_launch, '%Y-%m-%d'), price=price, category_id=category)

        for product in content['product']:
            new_product = Product(name=product["name"],status=product["status"],description=product["description"],price=product["price"],category_id=product["category_id"],studio=product["studio"],date_launch=datetime.datetime.strptime(product["date_launch"], '%Y-%m-%d'))
            db.session.add(new_product)


        db.session.commit()

        flash('Produtos importados com sucesso!', category='success')
        return redirect(url_for('views.admin'))


    return render_template("admin_prod_import.html", user=current_user, categories=categories)

@views.route('/admin-usuario', methods=['GET', 'POST'])
@login_required
def admin_user():
    return render_template("admin_user.html", user=current_user, categories=Category.query.all(), users=User.query.all())

@views.route('/admin-usuario-editar', methods=['GET', 'POST'])
@login_required
def admin_user_edit():

    id_user = request.args.get('id')
    user = User.query.get(id_user)

    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        is_admin = request.form.get('is_admin')

        user = User.query.filter_by(email=email).first()
        
        if len(first_name) < 2:
            flash('Nome deve ser pelo menos 3 caractéres.', category='error')
        elif len(last_name) < 2:
            flash('Sobrenome deve ser pelo menos 3 caractéres.', category='error')
        else:
            user.email=email
            user.first_name=first_name
            user.last_name=last_name
            if is_admin:
                user.is_admin=True
            else:
                user.is_admin=False

            db.session.commit()
            flash('Dados salvos com sucesso!', category='success')
            return redirect(url_for('views.admin_user'))


    return render_template("admin_user_edit.html", user=current_user, categories=Category.query.all(), user_db=user)

@views.route('/admin-usuario-remover', methods=['GET', 'POST'])
@login_required
def admin_user_delete():

    id_user = request.args.get('id')
    user = User.query.get(id_user)

    db.session.delete(user)  
    db.session.commit()
    flash('Usuário removida com sucesso!', category='success')
    return redirect(url_for('views.admin_user'))

@views.route('/admin-categoria', methods=['GET', 'POST'])
@login_required
def admin_category():
    return render_template("admin_category.html", user=current_user, categories=Category.query.all())

@views.route('/admin-categoria-editar', methods=['GET', 'POST'])
@login_required
def admin_category_edit():

    id_category = request.args.get('id')
    category = Category.query.get(id_category)

    if request.method == 'POST':
        name = request.form.get('name')
        status = request.form.get('status')

        if len(name) < 2:
            flash('Nome deve ser pelo menos 3 caractéres.', category='error')
        else:
            category.name=name
            if status:
                category.status=True
            else:
                category.status=False
 
            db.session.commit()
            flash('Categoria editada com sucesso!', category='success')
            return redirect(url_for('views.admin_category'))


    return render_template("admin_category_edit.html", user=current_user, categories=Category.query.all(), category=category)

@views.route('/admin-categoria-adicionar', methods=['GET', 'POST'])
@login_required
def admin_category_add():

    if request.method == 'POST':
        name = request.form.get('name')
        status = request.form.get('status')

        if len(name) < 2:
            flash('Nome deve ser pelo menos 3 caractéres.', category='error')
        else:
            if status:
                status=True
            else:
                status=False

            new_category = Category(name=name,status=status)
            db.session.add(new_category)  
            db.session.commit()
            flash('Categoria criada com sucesso!', category='success')
            return redirect(url_for('views.admin_category'))


    return render_template("admin_category_edit.html", user=current_user, categories=Category.query.all(), category=category)

@views.route('/admin-categoria-remover', methods=['GET', 'POST'])
@login_required
def admin_category_delete():

    id_category = request.args.get('id')
    category = Category.query.get(id_category)

    db.session.delete(category)  
    db.session.commit()
    flash('Categoria removida com sucesso!', category='success')
    return redirect(url_for('views.admin_category'))



