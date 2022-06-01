FROM python:3.8
 ## гарантирует, что наш вывод консоли выглядит знакомым и не буферизируется Docker, что нам не нужно
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1
RUN mkdir /code
WORKDIR /code
COPY blog/requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY blog /code/
ADD blog /blog/
CMD python3 manage.py runserver 0.0.0.0:$PORT
## delete last


