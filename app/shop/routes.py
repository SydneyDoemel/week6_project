from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from collections import Counter


#import login funcitonality
from flask_login import login_required, current_user


# import models
from app.models import IgShop, User, Carts
shop = Blueprint('shop', __name__, template_folder='shoptemplates')
from app.models import db


@shop.route('/shop')
def shopPage():
    x = IgShop.query.all()
    return render_template('shop.html', x=x)


@shop.route('/add/<string:title>')
@login_required
def addToCart(title):
    item = IgShop.query.filter_by(title=title).first()
    x = Carts(user_id=current_user.id, ig_shop_id=item.id)
    print(x)
    x.save()
    flash('Succesfully added to cart.', 'success')
    return redirect(url_for('shop.shopPage'))


 

@shop.route('/cart')
def cartPage():
    items =Carts.query.filter_by(user_id=current_user.id).all()
    items_lst = []
    qty = 0
    for each in items:
        item = IgShop.query.get(each.ig_shop_id)
        items_lst.append(item)
    grand_total = 0
    for each in items_lst:
        grand_total += int(each.price)
    print(items)
    return render_template('cart.html', items_lst = items_lst, grand_total = grand_total)

@shop.route('/cart/<string:title>')
@login_required
def seeItem(title):
    item = IgShop.query.filter_by(title=title).first()
    see =Carts.query.filter_by(user_id=current_user.id, ig_shop_id = item.id).first()
    return render_template('see.html', item = item)



@shop.route('/del/<string:title>')
@login_required
def removeFromCart(title):
    item = IgShop.query.filter_by(title=title).first()
    x =Carts.query.filter_by(user_id=current_user.id, ig_shop_id = item.id).first()
    x.delete()
    flash('Succesfully removed from cart.', 'danger')
    return redirect(url_for('shop.cartPage'))


@shop.route('/del')
@login_required
def removeAll():
    x = Carts.query.filter_by(user_id = current_user.id).all()
    for each in x:
        each.delete()
    flash('Succesfully removed from cart.', 'danger')
    return redirect(url_for('shop.cartPage'))


# DELETE FROM Carts WHERE user_id = current_user.id


