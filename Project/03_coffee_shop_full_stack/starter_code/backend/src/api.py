import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
app.app_context().push()
setup_db(app)
CORS(app)


#db_drop_and_create_all()

# ROUTES

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                            'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                            'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/')
def index():
    return jsonify({
        "success":True
    })


'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks',methods=['GET'])
def drinks_short():
    drinks = Drink.query.all()
    
    return jsonify({
        "success":True,
        "drinks": [drink.short() for drink in drinks]
    }), 200


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail',methods=['GET'])
@requires_auth('get:drinks-detail')
def drinks_long(payload):
    drinks = Drink.query.all()
    
    return jsonify({
        "success":True,
        "drinks": [drink.long() for drink in drinks]
    }), 200


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks',methods=['POST'])
@requires_auth('post:drinks')
def drinks_post(payload):

    try:
        form = request.get_json()
        drink = Drink(title=form['title'],recipe=json.dumps(form['recipe']))
        drink.insert()
        
    except Exception:
        abort(422)
        
    return jsonify({
        "success":True,
        "test":drink.long()
    }), 201
    

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

@app.route("/drinks/<id>",methods=['PATCH'])
@requires_auth('patch:drinks')
def drinks_patch(payload, id):

    try:
        drink = Drink.query.filter_by(id=id).one_or_none()
        
        if drink:
            form = request.get_json()
            title = form['title']
            drink_long = json.dumps(form['recipe'])
            if len(title) != 0:
                drink.title = title    
            if len(drink_long.strip(r"\"\"").strip("[]")) != 0:
                drink.recipe = drink_long
            
            drink.update()
            
        else:
            abort(404)
        
    except Exception as error:
        print(error)
        abort(422)
        
    return jsonify({
        "success":True,
        "drinks":[drink.long()],
        "temp":drink_long.strip(r"\"\"").strip("[]")
    }), 200

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

@app.route("/drinks/<id>",methods=['DELETE'])
@requires_auth('delete:drinks')
def drinks_delete(payload, id):

    try:
        drink = Drink.query.filter_by(id=id).one_or_none()
        
        if drink:     
            drink.delete()
            
        else:
            abort(404)
        
    except Exception as error:
        print(error)
        abort(422)
        
    return jsonify({
        "success":True,
        "delete":id
    }), 200

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(404)
def res_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404




'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response