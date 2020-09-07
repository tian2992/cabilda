from flask import Flask, _app_ctx_stack, jsonify, url_for, request
from twilio.twiml.messaging_response import MessagingResponse

from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)


@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')

    # Create reply
    resp = MessagingResponse()
    resp.message("You said: {}".format(msg))

    return str(resp)

@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.session.remove()
    
    
if __name__ == "__main__":
    app.run(debug=True)
