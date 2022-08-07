from cgi import print_exception
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


# class Followers(db.Model):
#     follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
#     followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
)

user_shop = db.Table('user_shop',
    db.Column('cart_id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('ig_shop_id', db.Integer, db.ForeignKey('ig_shop.id'))
) 

# create our Models based off of our ERD
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    post = db.relationship("Post", backref='author', lazy=True)
    followed = db.relationship("User",
        primaryjoin = (followers.c.follower_id==id),
        secondaryjoin = (followers.c.followed_id==id),
        secondary = followers,
        backref = db.backref('followers', lazy='dynamic'),
        lazy = 'dynamic'
    )
    cart = db.relationship("IgShop",
        secondary = user_shop,
        backref='buyers',
        lazy = 'dynamic'
    )

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

 ######
    def to_cart(self, item):
        self.cart.append(item)
        db.session.commit()
    def del_cart (self, item):
        self.cart.remove(item)
        db.session.commit()

#######

    def follow(self, user):
        self.followed.append(user)
        db.session.commit()


    def unfollow(self, user):
        self.followed.remove(user)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
    
    def saveToDB(self):
        db.session.commit()

    # get all the posts that I am following PLUS my own
    def get_followed_posts(self):
        # all the posts i am following
        followed = Post.query.join(followers, (Post.user_id == followers.c.followed_id)).filter(followers.c.follower_id == self.id)
        # get all my posts
        mine = Post.query.filter_by(user_id = self.id)
        # put them all together
        all = followed.union(mine).order_by(Post.date_created.desc())
        return all


class Carts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    igshop_id =db.Column(db.Integer, db.ForeignKey('igshop.id'), nullable=False)

class IgShop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    img_url=db.Column(db.String(300), nullable=False)
    price=db.Column(db.String(100), nullable=False)
    description=db.Column(db.String(500), nullable=False)
    def __init__(self, title, img_url, price, description):
        self.title = title
        self.img_url = img_url
        self.price = price
        self.description = description
    def save(self):
        db.session.add(self)
        db.session.commit()
   
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    img_url = db.Column(db.String(300))
    caption = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, img_url, caption, user_id):
        self.title = title
        self.img_url = img_url
        self.caption = caption
        self.user_id = user_id

    def updatePostInfo(self, title, img_url, caption):
        self.title = title
        self.img_url = img_url
        self.caption = caption

    def save(self):
        db.session.add(self)
        db.session.commit()

    def saveUpdates(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'caption': self.caption,
            'img_url': self.img_url,
            'date_created': self.date_created,
            'user_id': self.user_id,
            'author': self.author.username
        }



    