import requests
import json
import slack_config
from flask import request


class MessageSlack():


  def post_message_to_slack(text, blocks = None):

    return requests.post('https://slack.com/api/chat.postMessage', {
      
      'token': slack_config.slack_token,
      'channel': slack_config.slack_channel,
      'text': text,
      'icon_emoji': slack_config.slack_icon_emoji,
      'username': slack_config.slack_user_name,
      'blocks': json.dumps(blocks) if blocks else None

    }).json()

  def codigo_etl():
    texto = 'Teste 15/05/22 - Flask - Acessando pela rota'
    return texto

  def route():
    body = request.get_json()

    if body['cpu_usage'] < 1:
      try:
        slack_info = MessageSlack.codigo_etl()
        MessageSlack.post_message_to_slack(slack_info)
        
      except:
        slack_info = 'Encontramos problemas ao atualizar os dados :pleading_face:'
        MessageSlack.post_message_to_slack(slack_info)
      
    return body


