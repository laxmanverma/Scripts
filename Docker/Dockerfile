FROM python:3
MAINTAINER Laxman Verma
ADD testingUrlResponse.py /
RUN pip install Pyrebase
RUN pip install urllib3
RUN pip install xmltodict
RUN pip install schedule
CMD [ "python", "./testingUrlResponse.py" ]
