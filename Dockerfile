# base image  
FROM python:3.9

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies  
RUN pip install --upgrade pip
RUN apt-get update  
RUN apt-get -y upgrade
RUN apt -y install graphviz xdg-utils

# copy whole project to your docker home directory. 
COPY . .

# run this command to install all dependencies  
RUN pip install -r requirements.txt  

# port where the Django app runs  
EXPOSE 8000  
# start server 
ENTRYPOINT ["python3", "./manage.py"]
CMD [ "runserver", "0.0.0.0:8000" ]