FROM python:3.6-alpine

ARG project_dir=/python/app/markov-twitter
ADD . ${project_dir}
WORKDIR ${project_dir}

RUN set -x && \
    apk update --no-cache && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python3", "main.py"]
