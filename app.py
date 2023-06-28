from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Message(db.Model):
	id = db.Column('message_id', db.Integer, primary_key=True)
	content = db.Column(db.String(255), nullable=False)
	sent_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	def __repr__(self):
		return f'Message {self.content}'

	def __init__(self, content):
		self.content = content

with app.app_context():
    db.create_all()


def format_message(message):
	return {
		'content': message.content,
		'id': message.id,
		'sent_at': message.sent_at
	}
	

@app.route('/', methods=['GET'])
def get_messages():
	messages = Message.query.all()
	message_list = []
	for message in messages:
		message_list.append(format_message(message))
	return {'message': message_list}


@app.route('/', methods=['POST'])
def send_message():
	content = request.json['content']
	message = Message(content)
	db.session.add(message)
	db.session.commit()
	return format_message(message)



if __name__ == '__main__':
	app.run()