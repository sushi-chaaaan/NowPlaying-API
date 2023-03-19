FROM python:3.11-buster as builder

# set work directory
WORKDIR /app

# python environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONUTF8=1 \
    PYTHONIOENCODING=UTF-8 \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# requirements.txtをCOPY
COPY requirements.txt* ./

# pipでライブラリをインストール
RUN pip install --no-cache-dir -U pip  &&\
    pip install --no-cache-dir -U setuptools  && \
    pip install --no-cache-dir -U wheel  && \
    pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim-buster as runner

# copy python package
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# set work directory
WORKDIR /app

# permission settings
RUN groupadd -r app && useradd -r -g app app
RUN chown -R app:app /app
USER app

# プロジェクトをコピー
COPY --chown=app:app . ./

# start process
ENTRYPOINT ["python3.11", "main.py"]
