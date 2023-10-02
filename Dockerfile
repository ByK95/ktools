# Use an official Ubuntu as a parent image
FROM ubuntu:latest

# Set the maintainer label
LABEL maintainer="youremail@example.com"

# Set environment variables to non-interactive (this prevents some prompts)
ENV DEBIAN_FRONTEND=non-interactive

# Run package updates and install packages
RUN apt-get update \
    && apt-get -y install cmake imagemagick libmagick++-dev build-essential libzip-dev git python3 python3-pip

# Install Flask
RUN pip3 install Flask
RUN pip3 install ipdb

# Set the working directory in the container
WORKDIR /project

# Copy the current directory contents into the container at /project
COPY . /project

# Build the project
RUN cmake -DBUNDLED_DEPENDENCIES=ON -DCMAKE_BUILD_TYPE=Release /project && make

# Expose port 5000
EXPOSE 5000

# Run manage.py when the container launches
CMD ["python3", "manage.py"]
