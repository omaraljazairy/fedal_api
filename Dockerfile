FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /fedalapi

WORKDIR /fedalapi

COPY . /fedalapi

ADD ./ /fedalapi/

RUN python -m pip install --upgrade pip && python -m pip install -r requirements.txt

CMD ["python", "api/manage.py", "runserver", "0.0.0.0:8001"]
