FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /fedal_api

WORKDIR /fedal_api

COPY . /fedal_api

ADD ./ /fedal_api/

RUN python -m pip install --upgrade pip && python -m pip install -r requirements.txt

CMD ["python", "api/manage.py", "runserver", "0.0.0.0:8001"]
