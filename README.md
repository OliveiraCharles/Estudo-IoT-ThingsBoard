# Estudo IoT - ThingsBoard

Este estudo foi feito usando [WSL2](https://learn.microsoft.com/pt-br/windows/wsl/install) e [Docker](https://www.docker.com/) rodando em Windows 11

## Subindo containers

1. Crie o diretório do projeto

    ```sh
    mkdir estudo-iot
    cd estudo-iot
    ```

2. Crie o arquivo `docker-compose`

    ```sh
    nano docker-compose.yml
    ```

3. Faça alterações se julgar necessário

    ```yaml
    version: '3.0'
    services:
    mytb:
        restart: always
        image: "thingsboard/tb-postgres"
        ports:
        - "8080:9090"
        - "1883:1883"
        - "7070:7070"
        - "5683-5688:5683-5688/udp"
        environment:
        TB_QUEUE_TYPE: in-memory
        volumes:
        - ./.mytb-data:/data
        - ./.mytb-logs:/var/log/thingsboard

    mkdir -p ./.mytb-data && chown -R 799:799 ./.mytb-data
    mkdir -p ./.mytb-logs && chown -R 799:799 ./.mytb-logs
    ```

4. Coloque os containers no "ar"

    Execute os comandos abaixo e aguarde até que os serviços estejam rodando, pode demorar alguns minutos para serem inicializados

    ```sh
    docker compose up -d
    docker compose logs -f mytb
    ```

5. acesse a aplicação

    Com os containers devidamente utilize seu navegador para acessar `http://localhost:8080`
    acesse usando as credenciais:
    - System Administrator: <sysadmin@thingsboard.org> / sysadmin
    - Tenant Administrator: <tenant@thingsboard.org> / tenant
    - Customer User: <customer@thingsboard.org> / customer

## Simulando o dispositivo com aplicação em python

1. crie um ambiente virtual

    ```sh
    python -m venv .venv
    .venv/Scripts/activate
    ```

2. instale as dependências

    ```sh
    python -m pip install -U pip
    pip install -r requirements.txt
    ```

3. crie o arquivo `dispositivo.py`

    ```sh
    nano dispositivo.py
    ```

    ```py
    """
    Este script simula um dispositivo IoT enviando requisições HTTP POST para aplicação ThingsBoard
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

    if __name__ == '__main__':
        while True:
            send_message()
            time.sleep(5)

    ```

### Configure as variáveis de ambiente

1. Crie o arquivo .env na pasta raiz do projeto

    ```sh
    nano .env
    ```

2. Altere o valor do ACCESS_TOKEN de acordo com a configuração do dispositivo criado em `http://localhost:8080/entities/devices`

    ```.env
    ACCESS_TOKEN=abc123
    BASE_URL=http://localhost:8080
    ```

## Execute a aplicação

```sh
python dispositivo.py
```

## Referencias

[Thingsboard](https://thingsboard.io/)
[Installing ThingsBoard using Docker (Linux or Mac OS)](https://thingsboard.io/docs/user-guide/install/docker/?ubuntuThingsboardQueue=inmemory)
[CiberSecIOT-Material](https://ensinoiptbr-my.sharepoint.com/personal/lavanco_ipt_br/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Flavanco%5Fipt%5Fbr%2FDocuments%2FAulas%2FSeguran%C3%A7a%20em%20IoT%2FCiberSecIoT%2DMaterial&ga=1)
