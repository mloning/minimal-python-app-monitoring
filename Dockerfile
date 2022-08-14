FROM python:3.10

ENV WORKDIR app

WORKDIR ${WORKDIR}
COPY app/ ${WORKDIR}

RUN pip install --no-cache-dir --upgrade -r ${WORKDIR}/requirements.txt

EXPOSE 5000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]