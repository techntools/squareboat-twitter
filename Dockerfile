FROM python:3.7.3

RUN pip install --upgrade pip

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

RUN useradd santosh

WORKDIR /app

RUN wget -O /usr/bin/wait-for-it https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh
RUN chmod +x /usr/bin/wait-for-it

RUN chown -R santosh:santosh /app
RUN chmod -R 755 /app

COPY . .

USER santosh

EXPOSE 8080

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
