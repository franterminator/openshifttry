FROM python:3
COPY ./* ./
RUN pip install python-telegram-bot 
CMD ["python", "./bot.py"]