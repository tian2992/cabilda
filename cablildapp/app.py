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


def log_message(message):
    m = models.Message(message)
    app.session.add(m)
    return


@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')

    try:
        log_message(request.form)
    except:
        app.logger.error("error logging mess")
    # Create reply
    resp = MessagingResponse()
    resp.message("You said: {}".format(msg))

    return str(resp)

@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.session.remove()
    
    
if __name__ == "__main__":
    app.run(debug=True)
