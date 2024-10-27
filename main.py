import datetime
import os
import signal
import sys
from types import FrameType

import requests
from docker import DockerClient
from dotenv import load_dotenv

load_dotenv()

docker_host = os.getenv('DOCKER_HOST', 'tcp://127.0.0.1:2375')
webhook_url = os.getenv('DISCORD_WEBHOOK_URL', '')


def send_message(payload: dict) -> None:
    response = requests.post(webhook_url, json=payload)
    if response.status_code != 204:
        print(
            f'Error sending to Discord: {response.status_code}, {response.text}'
        )


def container_listening(client: DockerClient) -> None:
    for event in client.events(decode=True, filters={'event': 'die'}):
        container_id = event.get('id', '')
        container_name = (
            event.get('Actor', {}).get('Attributes', {}).get('name', 'Unknown')
        )
        epoch_time = event.get('time', 0)
        exit_code = (
            event.get('Actor', {})
            .get('Attributes', {})
            .get('exitCode', 'Unknown')
        )

        date_time = datetime.datetime.fromtimestamp(
            epoch_time
        ) - datetime.timedelta(hours=3)

        container = client.containers.get(container_id)
        logs = container.logs(tail=10).decode('utf-8').strip()

        if exit_code == '0':
            reason = 'The container stopped successfully.'
        else:
            reason = f'The container stopped unexpectedly with exit code `{exit_code}`. Logs:\n```{logs}```'

        payload = {
            'content': f':rotating_light: The container **{container_name}** (*{container_id[:12]}*) has stopped at {date_time}. Reason: {reason}'
        }

        send_message(payload)


def exit_handler(signum: int, frame: FrameType | None) -> None:
    payload = {'content': ':disappointed: Received *SIGTERM*. Goodbye!'}

    send_message(payload)
    sys.exit(0)


if __name__ == '__main__':
    client = DockerClient(base_url=docker_host)

    signal.signal(signal.SIGTERM, exit_handler)
    signal.signal(signal.SIGINT, exit_handler)

    container_listening(client)
