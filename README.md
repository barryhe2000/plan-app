# plan-app

Simple backend for tracking financial expenses written in Python with Flask and SQLAlchemy, and deployed through the Google
Cloud Platform.

There are three tables: User, Transactions, and Category. User and Category are tables 
that reflect many to many relationships, while User and Transactions maps one to many. The external IP is http://34.94.223.179/
but note that the home page does not have a route coded to it (so http://34.94.223.179/api/categories works).

GET: /api/categories 

Get all categories.

Post: /api/categories 

Post a new category by providing a name field in the JSON body.

{
   "name": <INPUT>
}

GET: /api/categories/{id}/

Get a specific category by id.

DELETE: /api/categories/{id}/

Delete a specific category by id.

POST: /api/users/{id}/transaction/

Post a new transaction by providing title, buy_date, and cost fields.
This will also update the corresponding user's "spent" field by adding
to it the "cost" value.

{
   "title": <INPUT>,
   "buy_date": <INPUT>,
   "cost": <INPUT>
}

POST: /api/users/

Post a new user given name, limit, and spent fields.

{
   "name": <INPUT>,
   "limit": <INPUT>,
   "spent": <INPUT>
}

GET: /api/users/{id}/

Get a specific user by id.

POST: /api/categories/{category_id}/add/

Post a user to a specific category, given the user id as a field.

{
   "user_id": <INPUT>
}