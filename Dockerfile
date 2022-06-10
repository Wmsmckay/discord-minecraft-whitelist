# FROM python:3.6.12-alpine3.12
FROM python:3.8-slim-buster
# FROM python:3
# FROM gorialis/discord.py

RUN mkdir -p /usr/src/bot

WORKDIR /usr/src/bot

COPY . .

RUN apt-get update 
# && \
    # apt-get add bash && \
    # bash && \
    # apt-get install nano

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD [ "python3", "discord_bot.py" ]