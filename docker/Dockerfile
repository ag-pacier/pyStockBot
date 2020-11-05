#Pull using Python 3.8
FROM python:3.8-slim

#Create the folders and user to run the app, give the user access to folders
RUN mkdir -m 0700 /app && mkdir -m 0600 /logs && useradd -u 1010 trade \
    && chown 1010 /app && chown 1010 /logs

#Copy in needed files for the app to work
COPY ["../requirements.txt", "../trader.py", "/app/"]

#Mark /logs as a possible volume
VOLUME [ "/logs" ]

#Install requirements
RUN ["pip", "-install", "--no-cache-dir", "-r" "/app/requirements.txt"]

#Environmental variables
ENV ROBINHOOD_USERNAME="base"
ENV ROBINHOOD_PASSWORD="base"
ENV ALPHA_VANTAGE_API_KEY="base"

#Switch to the app folder
WORKDIR /app/

#Switch to the trade user
USER trade

#Run the script
CMD [ "python", "./trader.py" ]