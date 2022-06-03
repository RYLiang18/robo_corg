FROM python:3.9-slim-buster

ENV USER appuser
RUN useradd --create-home --shell /bin/bash ${USER}
USER ${USER}
WORKDIR /home/${USER}

COPY requirements.txt .
RUN python -m pip install -U pip

RUN pip install -r requirements.txt

COPY . .
CMD ["sh", "init.sh"]