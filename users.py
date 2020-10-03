from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, jsonify
from starlette.requests import Request


class users:
    def __init__(self, db, request):
        self.db = db
        self.request = request

    def addUser(self, db):
        _json = self.request.json
        _email = _json['email']
        _name = _json['name']
        _password = _json['password']

        if _name and _password and _email and request.method == 'POST':
            _hashed_password = generate_password_hash(_password)

            try:
                if not db.db.collection.find_one({'name': _name}):
                    id = self.db.db.collection.insert_one({
                        'name': _name,
                        'email': _email,
                        'password': _hashed_password,
                    })
                    return jsonify("User added successfully")
                else:
                    return jsonify("User already exists")
            except:
                return {'message': 'Something went wrong'}, 500
        else:
            return self.not_found()

    def not_found(self, error=None):
        return jsonify({
            'status': 404,
            'message': 'Not found' + request.url
        })

    def updateuser(self, id, ObjectId):
        _id = id
        _json = self.request.json
        _email = _json['email']
        _name = _json['name']
        _password = _json['password']

        if _name and _password and _email and request.method == 'PUT':
            _hashed_password = generate_password_hash(_password)
            self.db.db.collection.update_one(
                {'_id': ObjectId(_id['$oid'])
                 if '$oid' in _id else ObjectId(_id)},
                {'$set': {
                    'name': _name,
                    'email': _email,
                    'password': _hashed_password,
                }})
            return "User got updated successfully"

    async def validateUser(self):
        _json = self.request.get()
        _email = _json['email']
        if self.db.db.collection.find_one({'email': _email}):
            _response = self.db.db.collection.find_one({'email': _email})
            _password = check_password_hash(
                _response['password'], _json['password'])
            if _password:
                resp = jsonify("Validation Successful")
                resp.status_code = 200
                return resp
            else:
                return jsonify("Invalid Username / Password")
        else:
            return jsonify("No user found")
