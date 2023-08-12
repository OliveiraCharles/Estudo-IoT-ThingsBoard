"""
Simula um dispositivo IoT enviando periodicamente valores de temperatura e
umidade para a plataforma ThingsBoard
"""
# Imports
import json
import random
import time
from os import environ

import httpx
from dotenv import load_dotenv

load_dotenv()

# Funções


def temperature():
    return round(random.uniform(23.7, 32.4), 2)


def humidity():
    return round(random.uniform(50.7, 100.4), 2)


def send_message():
    temperatura = temperature()
    umidade = humidity()

    body = {'temperatura': temperatura, 'umidade': umidade}

    response = httpx.post(data=json.dumps(body), headers=headers, url=url)

    print(f'\nTemperatura:  {temperatura}°C')
    print(f'Umidade:  {umidade}%')
    print(f'Status Code:  {response.status_code}', response.text)


# Variáveis
ACCESS_TOKEN = environ.get('ACCESS_TOKEN')
BASE_URL = environ.get('BASE_URL')

url = f'{BASE_URL}/api/v1/{ACCESS_TOKEN}/telemetry'
print(url)
headers = {'ContentType': 'application/json'}

# Main
if __name__ == '__main__':
    while True:
        send_message()
        time.sleep(5)
