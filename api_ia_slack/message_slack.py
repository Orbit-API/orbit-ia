import requests
import json
from orbit_ia import OrbitIA
import slack_config
from base64 import b64decode
from flask import request
from app import collection


class MessageSlack():


  def post_message_to_slack(text, blocks = None):

    return requests.post('https://slack.com/api/chat.postMessage', {
      
      'token': b64decode(slack_config.slack_token).decode("ascii").strip(),
      'channel': slack_config.slack_channel,
      'text': text,
      'icon_emoji': slack_config.slack_icon_emoji,
      'username': slack_config.slack_user_name,
      'blocks': json.dumps(blocks) if blocks else None

    }).json()

  def codigo_etl(mins):
    texto = f'Risco de Indisponibilidade - daqui a: {mins} minuto(s)'
    return texto

  def calculate_mins(units):
    return  round(units / 6)

  def route():
    body = request.get_json()
    data = collection.find()

    print(body)

    orbit = OrbitIA(
      data=data,
      metrics=body,
      mins_to_predict=10
    )

    availability = OrbitIA.orbit(orbit)
    print(availability)

    alert = 0
    units = 0
    for a in availability:
      if a[0] == 0:
        alert = 1
        break
      units = units + 1 
    mins = MessageSlack.calculate_mins(units)

    if alert == 1:
      try:
        slack_info = MessageSlack.codigo_etl(mins)
        MessageSlack.post_message_to_slack(slack_info)
        
      except:
        slack_info = 'Encontramos problemas ao atualizar os dados :pleading_face:'
        MessageSlack.post_message_to_slack(slack_info)
      
    return body


