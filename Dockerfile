FROM python:3.11-slim

WORKDIR /main

COPY . /main

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=jail.py
ENV FLASK_ENV=development

CMD ["flask", "run", "--host=0.0.0.0"]
