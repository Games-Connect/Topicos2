from flask import Blueprint, flash, render_template, request
from ..models import Category, Product, Subcategory
from flask_login import current_user, login_required
import collections

from .. import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    categories = Category.query.all()
    if (len(categories) == 0):
        db.session.add(Category(id=1, name="Ação"))
        db.session.add(Category(id=2, name="Aventura"))

        db.session.add(Product(id=1, name="Jogo 1", description="Descrição do jogo 1", category_id=1))
        db.session.add(Product(id=2, name="Jogo 2", description="Descrição do jogo 2", category_id=1))
        db.session.add(Product(id=3, name="Jogo 3", description="Descrição do jogo 3", category_id=2))
        db.session.add(Product(id=4, name="Jogo 4", description="Descrição do jogo 4", category_id=1))
        db.session.add(Product(id=5, name="Jogo 5", description="Descrição do jogo 5", category_id=1))
        db.session.add(Product(id=6, name="Jogo 6", description="Descrição do jogo 6", category_id=2))
        db.session.add(Product(id=7, name="Jogo 7", description="Descrição do jogo 7", category_id=1))
        db.session.add(Product(id=8, name="Jogo 8", description="Descrição do jogo 8", category_id=1))
        db.session.add(Product(id=9, name="Jogo 9", description="Descrição do jogo 9", category_id=2))
        
        db.session.add(Subcategory(id=1, name="Ação em 3ª pessoa", product_id=1))
        db.session.add(Subcategory(id=2, name="Simulador", product_id=1))
        db.session.add(Subcategory(id=3, name="Ação em 1ª pessoa", product_id=2))
        db.session.add(Subcategory(id=4, name="Hack & Slash", product_id=2))
        db.session.add(Subcategory(id=5, name="Casual", product_id=3))
        db.session.add(Subcategory(id=6, name="RPG", product_id=3))

        db.session.commit()


        categories.append(Category(id=1, name="Ação"))
        categories.append(Category(id=1, name="Ação"))

    # if request.method == 'POST':
        # note = request.form.get('note')

        # if len(note) < 1:
        #     flash('Note is too short!', category='error')
        # else:
        #     new_note = Note(data=note, user_id=current_user.id)
        #     db.session.add(new_note)
        #     db.session.commit()
        #     flash('Note added!', category='success')

    return render_template("home.html", user=current_user, categories=categories)

@views.route('/categoria', methods=['GET', 'POST'])
def categoria():
    id_category = request.args.get('id')
    categories = Category.query.all()
    # if id_categoria:
    #     categorias = Category.query.filter_by(id=id_categoria)
    # else:
    #     categorias = Category.query.all()

    return render_template("categoria.html", user=current_user, id_category=id_category, categories=categories)
