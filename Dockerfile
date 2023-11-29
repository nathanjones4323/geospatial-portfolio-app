FROM python:3.11

RUN apt-get update && apt-get install -y \
  #   libgeos-dev \
  #   gcc \
  #   libc-dev \
  libgdal-dev

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

EXPOSE 8501

COPY . /app

ENTRYPOINT ["streamlit", "run"]

CMD ["00_🏠_Homepage.py", "--server.headless", "true", "--server.fileWatcherType", "none", "--browser.gatherUsageStats", "false"]