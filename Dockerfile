FROM python:3.10-buster
COPY . .
CMD ["bash", "start_bot.sh"]
