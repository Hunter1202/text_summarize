FROM openjdk:17-jdk-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the JAR file from the host machine to the container
COPY target/ml-0.0.1-SNAPSHOT.jar /app/app.jar

# Install Python and required dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install nltk bs4

# Copy the Python script and stopword file
COPY ./src/main/python/TextSum.py /app/TextSum.py
COPY ./src/main/python/ArticleSum.py /app/ArticleSum.py
COPY ./src/main/resources/templates/vietnamese-stopwords.txt /app/vietnamese-stopwords.txt

# Set the entrypoint command to execute the JAR file
CMD ["java", "-jar", "app.jar"]
