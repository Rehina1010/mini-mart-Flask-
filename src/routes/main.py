import os
import stripe
from flask import current_app, jsonify, request
from flask import Blueprint, render_template, flash, redirect, url_for, session
from flask_login import login_required, current_user
from src.entity.models import Product

bp = Blueprint('main', __name__)

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


@bp.route('/')
def product_list():
    products = Product.query.all()
    return render_template('product_list.html', products=products)


@bp.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    return render_template('product_detail.html', product=product)


@bp.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    product = Product.query.get_or_404(id)
    cart = session.get('cart', [])
    cart.append(id)
    session['cart'] = cart
    flash(f'{product.name} Added to cart!')
    return redirect(url_for('main.product_list'))


@bp.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    cart_items_count = len(cart_items)
    products = Product.query.filter(Product.id.in_(cart_items)).all()
    products_dict = {product.id: product for product in products}
    return render_template('cart.html', cart_items=cart_items, cart_items_count=cart_items_count,
                           products=products_dict)


@bp.route('/remove_from_cart/<int:id>', methods=['POST'])
def remove_from_cart(id):
    cart = session.get('cart', [])
    if id in cart:
        cart.remove(id)
        session['cart'] = cart
        flash('Item removed from cart!')
    else:
        flash('Item not found in cart!', 'error')
    return redirect(url_for('main.cart'))


@bp.route('/about')
def about():
    return render_template('about.html')


@bp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    if not current_user.is_authenticated:
        return jsonify({'error': 'not_authenticated'}), 401

    try:
        cart_items = session.get('cart', [])
        products = Product.query.filter(Product.id.in_(cart_items)).all()

        line_items = []
        for product in products:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.name,
                    },
                    'unit_amount': int(product.price * 100),
                },
                'quantity': 1,
            })

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=f"{current_app.config['BASE_URL']}/checkout?success=true",
            cancel_url=f"{current_app.config['BASE_URL']}/checkout?success=false",
        )

        return jsonify({'sessionId': checkout_session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403


@bp.route('/checkout')
@login_required
def checkout():
    success = request.args.get('success', 'false') == 'true'

    if success:
        flash('Thank you for your purchase!', 'success')
    else:
        flash('Your payment was canceled.', 'error')

    session.pop('cart', None)
    return redirect(url_for('main.product_list'))


@bp.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')


@bp.route('/cookies-policy')
def cookies_policy():
    return render_template('cookies-policy.html')


@bp.route('/terms')
def terms():
    return render_template('terms.html')
