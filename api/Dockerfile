FROM python:3.9-alpine

ENV C_FORCE_ROOT true

ENV HOST 0.0.0.0
ENV PORT 5002
ENV DEBUG true

COPY . /api
WORKDIR /api

RUN pip install -U setuptools pip
RUN pip install -r requirements.txt

EXPOSE 5002

RUN pip install gunicorn

# CMD ["gunicorn", "--bind", "0.0.0.0:5002", "app:app"]
CMD ["python","-u","app.py"]