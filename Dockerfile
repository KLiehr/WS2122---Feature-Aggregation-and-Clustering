FROM python:3.7.9
COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

#RUN apt-get update  
#RUN apt-get -y upgrade
RUN pip install --upgrade pip
#RUN apt -y install graphviz xdg-utils  
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python3", "./manage.py", "runserver", "0.0.0.0:8000" ]