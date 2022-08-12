from flask import Flask, render_template, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcakes"
app.config['SECRET_KEY'] = 'KEY'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
connect_db(app)

@app.route('/')
def render_html():
    """making the front end (booooo)"""
    return render_template('index.html')

@app.route('/api/cupcakes')
def cupcake_data():
    """render ALL cupcake data"""
    cupcakes=[cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcake/<int:cupcake_id>')
def cupcake(cupcake_id):
    """render data on ONE cupcake"""
    cc=Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cc.to_dict())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """ADD NEW CUPCAKE TO DB AND RETURN ITS JSON"""
    d = request.json
    cupcake = Cupcake(flavor=d['flavor'], rating=d['rating'], size=d['size'], image=d['image'] or None)

    db.session.add(cupcake)
    db.session.commit()
    return (jsonify(cupcake=cupcake.to_dict()), 201)

@app.route('/api/cupcake/<int:cupcake_id>', methods=["PATCH"])
def update_cc(cupcake_id):
    """UPDATE CC BY PASSING ID - RETURN 404 IF INVALID CC_ID PASSED"""
    d = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor=d['flavor']
    cupcake.rating=d['rating']
    cupcake.size=d['size']
    cupcake.image=d['image']

    db.session.add(cupcake)
    db.session.commit()
    return jsonify(cupcake=cupcake.to_dict())

@app.route('/api/cupcake/<int:cupcake_id>', methods=["DELETE"])
def delete_cc(cupcake_id):
    """REMOVE CC FROM DB - RETURN 404 IF INVALID CC_ID PASSED"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")