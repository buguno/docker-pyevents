import datetime
import os

import docker
import requests
from dotenv import load_dotenv

load_dotenv()

docker_host = os.getenv('DOCKER_HOST', 'tcp://127.0.0.1:2375')
webhook_url = os.getenv('DISCORD_WEBHOOK_URL', '')

client = docker.DockerClient(base_url=docker_host)

for event in client.events(decode=True, filters={'event': 'die'}):
    container_id = event.get('id', '')
    container_name = event.get('Actor', {}).get('Attributes', {}).get('name', 'Unknown')
    epoch_time = event.get('time', 0)
    exit_code = event.get('Actor', {}).get('Attributes', {}).get('exitCode', 'Unknown')

    date_time = datetime.datetime.fromtimestamp(epoch_time) - datetime.timedelta(hours=3)

    container = client.containers.get(container_id)
    logs = container.logs(tail=10).decode('utf-8').strip()

    if exit_code == '0':
        reason = 'The container stopped successfully.'
    else:
        reason = f'The container stopped unexpectedly with exit code `{exit_code}`. Logs:\n```{logs}```'

    payload = {
        'content': f'The container **{container_name}** (*{container_id}*) has stopped at {date_time}. Reason: {reason}'
    }

    print(payload)

    response = requests.post(webhook_url, json=payload)
    if response.status_code != 204:
        print(f'Error sending to Discord: {response.status_code}, {response.text}')