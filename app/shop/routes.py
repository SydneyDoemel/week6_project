from flask import Blueprint, render_template, request, redirect, url_for, flash, session


#import login funcitonality
from flask_login import login_required, current_user


# import models
from app.models import IgShop, User, user_shop, Carts

shop = Blueprint('shop', __name__, template_folder='shoptemplates')

from app.models import db


@shop.route('/shop')
def shopPage():
    x = IgShop.query.all()
    return render_template('shop.html', x=x)




@shop.route('/add/<string:title>')
def addToCart(title):
    item = IgShop.query.filter_by(title=title).first()
    current_user.cart.append(item)
    db.session.commit()
  
    flash('Succesfully added to cart.', 'success')
    return redirect(url_for('shop.shopPage'))

@shop.route('/cart')
def cartPage():
    user = User.query.get(current_user.id)
    items=user.cart.all()
    # SELECT * FROM "user_shop" WHERE user_id =  1;
    print(items)
    return render_template('cart.html', items = items)

@shop.route('/remove/<int:id>')
def removeFromCart(id):
    
    item = IgShop.query.filter_by(id=id).all()
    print(item)
    for each in item:
        current_user.cart.remove(each)
        db.session.commit()
    flash('Succesfully removed to cart.', 'danger')
    return redirect(url_for('shop.shopPage'))