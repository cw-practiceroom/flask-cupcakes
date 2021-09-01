from flask import Flask, render_template, jsonify, request
from models import Cupcake, db, connect_db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = 'col3'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)


@app.route('/api/cupcakes')
def home_route():
    cupcakes = Cupcake.query.all()
    all_cupcakes = [ cupcake.serialize() for cupcake in cupcakes ]
    return jsonify(all_cupcakes)


@app.route('/api/cupcakes/<int:id>')
def view_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake.serialize())


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    new_cupcake = Cupcake(flavor=request.json['flavor'], rating=request.json['rating'], size=request.json['size'],  image=request.json['image'] or None)

    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(new_cupcake.serialize(), 201))


@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake.serialize())


@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message='deleted')


@app.route('/')
def home_page():
    cupcakes = Cupcake.query.all()
    return render_template('home.html', cupcakes=cupcakes)