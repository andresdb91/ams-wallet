FROM python:3.5-alpine

WORKDIR /wallet

RUN pip install gunicorn

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

CMD ["gunicorn", "-b", "0.0.0.0:3101", "application.app:MainApp.wsgi"]
