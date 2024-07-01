FROM joyzoursky/python-chromedriver:3.8-selenium

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code


# Ensure requirements.txt is in the Docker context and copy it
COPY requirements.txt /code/

# Upgrade pip and install requirements from requirements.txt in one RUN to reduce layers
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt


COPY . /code/


COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]


#  working
# FROM python:3
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# WORKDIR /code
# COPY requirements.txt /code/
# RUN pip install -r requirements.txt
# RUN pip install seleniumbase
# RUN pip install selenium
# RUN pip install webdriver_manager
# RUN pip install pytube
# RUN pip install validators
# RUN pip install djangorestframework
# RUN pip install webdriver_manager
# COPY . /code/

# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh
# ENTRYPOINT ["/entrypoint.sh"]
