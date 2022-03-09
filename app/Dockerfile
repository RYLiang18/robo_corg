FROM python:3.9-slim-buster

ENV USER appuser
RUN useradd --create-home --shell /bin/bash ${USER}
USER ${USER}
WORKDIR /home/${USER}

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
ENTRYPOINT ["sh", "init.sh"]