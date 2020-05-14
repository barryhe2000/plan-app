from db import db, Category, Transactions, User

# Category


def get_all_categories():
    return [c.serialize() for c in Category.query.all()]


def create_category(name):
    new_category = Category(name=name)
    db.session.add(new_category)
    db.session.commit()
    return new_category.serialize()


def get_category_by_id(c_id):
    c = Category.query.filter_by(id=c_id).first()
    if c is None:
        return None
    return c.serialize()


def delete_category_by_id(c_id):
    c = Category.query.filter_by(id=c_id).first()
    if c is None:
        return None
    db.session.delete(c)
    db.session.commit()
    return c.serialize()

# Transactions


def create_transaction(title, buy_date, cost, user_id):
    new_txn = Transactions(title=title, buy_date=buy_date, cost=cost,
                           user_id=user_id)
    db.session.add(new_txn)
    db.session.commit()
    return new_txn.serialize()

# User


def create_user(name, limit, spent):
    new_user = User(name=name, limit=limit, spent=spent)
    db.session.add(new_user)
    db.session.commit()
    return new_user.serialize()


def get_user_by_id(u_id):
    u = User.query.filter_by(id=u_id).first()
    if u is None:
        return None
    return u.serialize()


def delete_user_by_id(u_id):
    u = User.query.filter_by(id=u_id).first()
    if u is None:
        return None
    db.session.delete(u)
    db.session.commit()
    return u.serialize()


def add_user_to_category(user_id, category_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return None
    category = Category.query.filter_by(id=category_id).first()
    if category is None:
        return None
    category.users.append(user)
    db.session.commit()
    return category.serialize()
