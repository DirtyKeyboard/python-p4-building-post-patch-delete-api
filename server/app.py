#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

@app.route('/games')
def games():

    games = []
    for game in Game.query.all():
        game_dict = {
            "title": game.title,
            "genre": game.genre,
            "platform": game.platform,
            "price": game.price,
        }
        games.append(game_dict)

    response = make_response(
        games,
        200
    )

    return response

@app.route('/games/<int:id>', methods=['GET', 'DELETE', 'PATCH'])
def game_by_id(id):
    if request.method == 'GET':
        game = Game.query.filter(Game.id == id).first()    
        game_dict = game.to_dict()
        response = make_response(
            game_dict,
            200
        )
        return response
    elif request.method == 'DELETE':
        to_delete = Game.query.filter(Game.id == id).first()
        resp = to_delete.id
        db.session.delete(to_delete)
        db.session.commit()
        return make_response(f"ID: {resp}", 200)
    else:
        to_patch = Game.query.filter(Game.id == id).first()
        for atr in request.form:
            setattr(to_patch, atr, request.form.get(atr))
        db.session.commit()
        return make_response(f"{to_patch}",202)

@app.route('/games', methods=['POST'])
def post_game():
    # genre = db.Column(db.String)
    # platform = db.Column(db.String)
    # price = db.Column(db.Integer)
    new_game = Game(title=request.form.get('title'), genre=request.form.get('genre'),platform=request.form.get('platform'), price=request.form.get('price'))
    db.session.add(new_game)
    db.session.commit()
    r = Game.query.filter(Game.title == new_game.title).first()
    return f'<h1>Added {r}</h1>'
    


@app.route('/reviews')
def reviews():

    reviews = []
    for review in Review.query.all():
        review_dict = review.to_dict()
        reviews.append(review_dict)

    response = make_response(
        reviews,
        200
    )

    return response

@app.route('/users')
def users():

    users = []
    for user in User.query.all():
        user_dict = user.to_dict()
        users.append(user_dict)

    response = make_response(
        users,
        200
    )

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
