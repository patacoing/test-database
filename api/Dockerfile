FROM python:3.10-alpine

WORKDIR /app
COPY ./ ./

EXPOSE 8000

RUN python -m pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]