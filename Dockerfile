FROM python:3.10
  
WORKDIR /usr/src/

RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

COPY app.py .

ENTRYPOINT FLASK_APP=/usr/src/app.py flask run --host=0.0.0.0