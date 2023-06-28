from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_cors import CORS


""" 
update
curl -X PUT -H "Content-Type: application/json" -d '{"content":"Updated content"}' http://127.0.0.1:5000/api/3

delete
curl -X DELETE http://127.0.0.1:5000/api/2

post
curl -X POST -H "Content-Type: application/json" -d '{"content":"New message content"}' http://127.0.0.1:5000/api/
"""


app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5000/", "methods": ["GET", "POST", "PUT", "DELETE"]}})
db = SQLAlchemy(app)

class Message(db.Model):
	id = db.Column('message_id', db.Integer, primary_key=True)
	content = db.Column(db.String(255), nullable=False)
	sent_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	def __repr__(self):
		return f'Message {self.content}'

	def __init__(self, content):
		self.content = content
		utc_now = datetime.utcnow()
		ph_tz_offset = timedelta(hours=8)  # Philippine timezone offset is 8 hours ahead of UTC
		self.sent_at = utc_now + ph_tz_offset


with app.app_context():
    db.create_all()




def format_message(message):
	return {
		'content': message.content,
		'id': message.id,
		'sent_at': message.sent_at
	}

@app.route('/api/', methods=['GET'])
def get_messages():
	messages = Message.query.all()
	message_list = []
	for message in messages:
		message_list.append(format_message(message))
	return {'messages': message_list}

@app.route('/api/', methods=['POST'])
def send_message():
	content = request.json['content']
	message = Message(content)
	db.session.add(message)
	db.session.commit()
	return format_message(message)

@app.route('/api/<id>', methods=['DELETE'])
def delete_message(id):
	message = Message.query.filter_by(id=id).one()
	db.session.delete(message)
	db.session.commit()
	return f'Deleted {message.content}'

@app.route('/api/<id>', methods=['PUT'])
def update_message(id):
	message = Message.query.filter_by(id=id)
	content = request.json['content']
	message.update(dict(content=content, sent_at=datetime.utcnow()))
	db.session.commit()
	return {'messsages': format_message(message.one())}

if __name__ == '__main__':
	app.run(debug=True)