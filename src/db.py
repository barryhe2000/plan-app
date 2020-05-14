from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
cat_table = db.Table("c_table", db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("category_id", db.Integer, db.ForeignKey("category.id"))
)

class Category(db.Model):
    __tablename__="category"
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String, nullable=False)
    users=db.relationship("User",
        secondary=cat_table,
        back_populates="categories"
    )

    def __init__(self, **kwargs):
        self.name=kwargs.get("name", "")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "users": [u.mini_serialize() for u in self.users]
        }

class Transactions(db.Model):
     __tablename__="transactions"
     id=db.Column(db.Integer, primary_key=True)
     title=db.Column(db.String, nullable=False)
     buy_date=db.Column(db.Integer, nullable=False)
     cost=db.Column(db.Integer, nullable=False)
     user_id=db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

     def __init__(self, **kwargs):
         self.title=kwargs.get("title", "")
         self.buy_date=kwargs.get("buy_date", 0)
         self.cost=kwargs.get("cost", 0)
         self.user_id=kwargs.get("user_id")

     def serialize(self):
         return {
             "id": self.id,
             "title": self.title,
             "buy_date": self.buy_date,
             "cost": self.cost
         }

class User(db.Model):
    __tablename__="user"
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String, nullable=False)
    limit=db.Column(db.Integer, nullable=False)
    spent=db.Column(db.Integer, nullable=False)
    txns=db.relationship("Transactions", cascade="delete")
    categories=db.relationship("Category",
        secondary=cat_table,
        back_populates="users"
    )

    def __init__(self, **kwargs):
        self.name=kwargs.get("name", "")
        self.limit=kwargs.get("limit", 0)
        self.spent=kwargs.get("spent", 0)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "limit": self.limit,
            "spent": self.spent,
            "transactions": [t.serialize() for t in self.txns],
            "categories": [c.serialize() for c in self.categories]
        }
    def mini_serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "limit": self.limit,
            "spent": self.spent
        }
