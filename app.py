import connexion
import datetime
import logging
from sqlalchemy import exc
from connexion import NoContent
import database
from marshmallow import Schema, fields

db_session = None


def get_user(user_id):
    user = db_session.query(database.User).filter(database.User.id == user_id)
    if not user.first():
        return ('Not found', 404)
    else:
        user_response_schema = database.UserResponseSchema()
        return user_response_schema.dump(user.first()),200



def put_user(user_id, user_obj):
    user = db_session.query(database.User).filter(database.User.id == user_id) 
    if user.first():
        user_dict = database.UserSchema().dump(user_obj)
        user.update(user_dict)
        db_session.commit()
        return user_dict,200
    else:
        user_obj = database.User(**user_obj)
        user_obj.id = user_id
        user_obj.date = datetime.datetime.utcnow()
        try:
            db_session.add(user_obj)
            db_session.commit()
            db_session.refresh(user_obj)
            user_response_schema = database.UserResponseSchema()
            user_dict = user_response_schema.dump(user_obj)
        except exc.IntegrityError:
            db_session.rollback()
            return {}, 422
        return user_dict, 201


def delete_user(user_id):
    user = db_session.query(database.User).filter(database.User.id == user_id)
    if user.first():
        user.delete()
        db_session.commit()
        return NoContent,204
    else:
        return NoContent, 404


logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__)
app.add_api('my_api.yaml')
db_session = database.init_db("sqlite:///sql_add.db")



application = app.app


@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

application = app.app

if __name__ == '__main__':
    app.run(port=8080, server='gevent')