# stage 2: run 
FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /runtime/
COPY . .

CMD [ "python3", "slow_tcp.py" ]