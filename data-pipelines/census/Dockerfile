FROM python:3.11

RUN apt-get update && apt-get install -y \
  #   libgeos-dev \
  #   gcc \
  #   libc-dev \
  libgdal-dev

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY . /app

# Specify the entry point for your container
CMD ["python", "geographies.py"]