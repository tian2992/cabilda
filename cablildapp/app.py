from flask import Flask, _app_ctx_stack, jsonify, url_for, request
from sqlalchemy.orm import scoped_session
from twilio.twiml.messaging_response import MessagingResponse

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/messages.json")
def get_all_messages():
    messages = app.session.query(models.Message).all()
    return jsonify([mess.to_dict() for mess in messages])


def create_user(user_id, country = None):
    u = models.User(user_id = user_id, country = country)
    app.session.add(u)
    return u


def log_message(message):
    m = models.Message()
    m.user_id = message.get("From")
    m.all_message = message
    app.session.add(m)
    return


@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')
    full_form = dict(request.form)
    from_id = request.form.get('From')

    try:
        create_user(from_id)
    except:
        app.logger.error("fail logging user")

    app.session.commit()
    try:
        full_form["user_id"] = from_id
        log_message(full_form)
    except Exception as e:
        app.logger.error(f"error logging mess {e}")


    app.session.commit()
    # Create reply
    resp = MessagingResponse()
    resp.message("You said: {}".format(msg))

    return str(resp)

@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.session.remove()
    
    
if __name__ == "__main__":
    app.run(debug=True, port=8000)
