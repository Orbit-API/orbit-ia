from flask import Blueprint
from message_slack import MessageSlack

message_to_slack = Blueprint('message_to_slack', __name__)
message_to_slack.route('/', methods=['POST'])(MessageSlack.route)
