FROM python:latest

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 8000

CMD ["gunicorn", "rssreader.wsgi", ":8000"]