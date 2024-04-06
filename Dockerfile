FROM python:3.10 as requirements-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10
WORKDIR /github_parser
COPY --from=requirements-stage /tmp/requirements.txt /github_parser/requirements.txt
COPY .env /github_parser
COPY init_db.py /github_parser
COPY setup.sh /github_parser
COPY scripts /github_parser/scripts

RUN pip install --no-cache-dir --upgrade -r /github_parser/requirements.txt
COPY ./src /github_parser/src

RUN chmod +x /github_parser/setup.sh
ENTRYPOINT ["/github_parser/setup.sh"]

CMD python -m uvicorn src:init_app --host 0.0.0.0 --port 80 --factory
