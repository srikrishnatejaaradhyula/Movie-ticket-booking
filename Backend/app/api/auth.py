from flask import request,jsonify
from app import app,db,cache
from app.token import token_required
import jwt
from datetime import datetime,timedelta
from app.model import UserAuth,AdminAuth
from app.mail import send_email_html
import random





@app.route("/api/user_login", methods=["POST","GET"])
def userlogin():
    data = request.get_json()
    auth = UserAuth.query.filter_by(email=data["email"]).first()

    if auth is None:
        return jsonify({"error": "Email is incorrect"}), 400
    
    elif auth.password != data["password"]:
        return jsonify({"error": "Password is incorrect"}), 400

    token = jwt.encode({'id' : auth.id, 
                        'name' : auth.name,
                        'exp' : datetime.utcnow() + timedelta(hours=24)}, 
                        app.config['SECRET_KEY'], "HS256")

    return jsonify({'token' : token}), 200



@app.route("/api/admin_login", methods=["POST","GET"])
def adminlogin():
    data = request.get_json()
    auth = AdminAuth.query.filter_by(username=data["username"]).first()
    current_time = datetime.now()
    if auth is None:
        return jsonify({"error": "username is incorrect"}), 400
    
    elif auth.password != data["password"]:
        return jsonify({"error": "Password is incorrect"}), 400

    token = jwt.encode({'id' : auth.id,
                        'name' : auth.name,
                        'exp' : datetime.utcnow() + timedelta(hours=24)}, 
                        app.config['SECRET_KEY'], "HS256")
    auth.last_login = current_time
    db.session.commit()
    return jsonify({'token' : token}), 200


@app.route("/api/user_register", methods=["POST","GET"])
def register():
    data = request.get_json()
    existing_user = UserAuth.query.filter_by(email=data['email']).first()

    # check if user already exists
    if existing_user:
        return jsonify({"error": "Email already in use"}), 400
    
    # create new user
    user = UserAuth(name=data["name"], email=data["email"], password=data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201



@app.route("/api/send_otp", methods=["POST","GET"])
def send_otp():
    data = request.get_json()
    email = data["email"]
    otp = random.randint(100000,999999)
    body = f"""
    <html>
    <body>
        <p>Don't share otp to any one</p>
        <h4>This is your otp</h4>
        <h1>{otp}</h1>
    </body>
    </html>
    """
    body2 = f"Don't share otp to any one.\nThis is your otp.\n{otp}"
    send_email_html("mad2project.ticketshow@gmail.com",email, 'Otp To Change Password',body)
    return jsonify({"message": "OTP sent successfully","otp":otp}), 200

@app.route("/api/change_password", methods=["POST","GET"])
def change_password():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    auth = UserAuth.query.filter_by(email=email).first()
    auth.password = password
    db.session.commit()
    return jsonify({"message": "Password changed successfully"}), 200





# this route for testing only
@app.route("/fun", methods=["GET"])
def fun():
    return jsonify({"message": "You are fun!"}), 200



@app.route("/api/test", methods=["GET"])
@token_required
def test(current_user):
    return  jsonify({"user": current_user.id}), 200
    

@app.route("/testing_cache", methods=["GET"])
@cache.cached(timeout=50)
def testing_cache():
    r = random.randint(1,100)
    return jsonify({"random": r}), 200