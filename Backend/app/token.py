import jwt
from functools import wraps
from flask import request, jsonify
from app import app
from app.model import UserAuth





def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       if 'x-access-tokens' in request.headers:
           token = request.headers['x-access-tokens']
 
       if not token:
           return jsonify({'message': 'a valid token is missing'})
       try:
           data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
       except:
           return jsonify({'message': 'token is invalid'})
 
       return f( *args, **kwargs)
   return decorator
