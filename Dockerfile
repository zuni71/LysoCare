FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN pip3 install --upgrade pip;


WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt;

COPY --chown=root:app . /app

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
