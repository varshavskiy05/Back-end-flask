from flask.views import MethodView
from flask_smorest import abort
from flask_jwt_extended import create_access_token
from passlib.hash import pbkdf2_sha256

from myapp.auth import bp
from myapp.models import db, User
from myapp.schemas import AuthRegisterSchema, AuthLoginSchema, UserSchema


@bp.route('/register')
class Register(MethodView):
    @bp.arguments(AuthRegisterSchema)
    @bp.response(201, UserSchema)
    def post(self, user_data):
        existing = User.query.filter_by(username=user_data['username']).first()
        if existing:
            abort(400, message='Username already exists')
        # обеспечить name для not null
        name_value = user_data.get('name') or user_data['username']
        user = User(
            username=user_data['username'],
            password=pbkdf2_sha256.hash(user_data['password']),
            name=name_value
        )
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message=f'Error creating user: {str(e)}')
        return user


@bp.route('/login')
class Login(MethodView):
    @bp.arguments(AuthLoginSchema)
    def post(self, user_data):
        user = User.query.filter_by(username=user_data['username']).first()
        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}, 200
        abort(401, message='Invalid credentials')


