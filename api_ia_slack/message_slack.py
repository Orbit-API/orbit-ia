import requests
import json
from orbit_ia import OrbitIA
import slack_config
from base64 import b64decode
from flask import request
from app import collection
from datetime import datetime

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

  def codigo_etl(mins, risk):
    time = datetime.now()
    if mins == 0 or risk == 100:
      texto = f'*Sistema Indisponível! *  \n *Canal:* {slack_config.slack_channel} \n *Data e Hora: *  {time} :fire: '
    else:
      texto = f'*Risco de Indisponibilidade: * {risk}% \n*Previsão de Queda: * {mins} minutos \n*Canal:* {slack_config.slack_channel} \n*Data e Hora: *  {time} :fire: '
    
    # texto = f'Risco de Indisponibilidade - daqui a: {mins} minuto(s)'
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
      mins_to_predict=60
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
        slack_info = MessageSlack.codigo_etl(mins, 30)
        MessageSlack.post_message_to_slack(slack_info)
        
      except Exception as erro:
        slack_info = 'Encontramos problemas ao atualizar os dados :pleading_face:'
        MessageSlack.post_message_to_slack(slack_info)
        print('************************************************')
        print(erro)
      
    return body


