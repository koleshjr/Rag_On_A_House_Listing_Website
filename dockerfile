#use an official python runtime as a parent image
FROM python:3.9-slim 

#set the working directory to /app
WORKDIR /app

#copy the current directory contents into the container at /app
COPY requirements.txt /app/

#install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

#copy the current directory contents into the container at /app
COPY . /app/

#make port 80 available to the world outside this container
EXPOSE 80

#set environment variables
ENV NAME glo-backend-fast-api-docker

#set the maintainer label
LABEL maintainer="Koleshjr <koleshjr@gmail.com>"

#run app.py when the container launches using ASGI server uvicorn AT port 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]