FROM python:3.10

RUN groupadd -r pyuser && useradd -r -g pyuser pyuser

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./app /code/app

RUN chown -R pyuser:pyuser /code

USER pyuser

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]