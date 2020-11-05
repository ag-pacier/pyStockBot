# Python Stock Trader DOCKERIZED
This is a mostly containerized version of psycoder17's nifty EMA Robinhood bot.
In the future, this will be a small web site that will manage both ends of setting up and running your Robinhood bot.

## Getting Started

You need [Docker Desktop](https://www.docker.com/products/docker-desktop) and [Python 3.](https://www.python.org/downloads/)
Once installed, clone this repo onto your PC (download as a ZIP, use GitHub Desktop, be fancy and CLI git*, pick your poison*).
Open up your shell of choice (Powershell for Windows, Terminal for Linux/Mac) and install the robin-stocks library:

### For Windows
```
python -m pip -Iv robin-stocks==1.5.0
```

### For Linux/Mac
```
pip3 -Iv robin-stocks==1.5.0
```

## Setup your tickers

In your terminal/Powershell prompt, go to the folder containing the populate-tickers.py script and run it.

### For Windows
```
python ./populate-tickers.py
```

### For Linux/Mac
```
python3 ./populate-tickers.py
```

The script will prompt you for stock tags and max prices you are willing to pay for each. Once done, you're going to have a CSV file called monitored-tickers.csv in the same folder as you ran the script. If you want, you can move this to another folder for cleanliness but you need to keep in mind that the script won't see your CSV file if it's not in the same folder as itself. If you are messy and/or just kicking the tires, leave it where it is.

## Run the trader
The container is the actual logic of the script and will do the actual trading based on the parameters you setout using populate-tickers.py. First thing to do is build the image. Open your terminal/Powershell prompt, go into the docker file in this github repo you cloned and run the following:
```
docker build --tag robinhoodbot:0.5 .
```

Create an .env file based on the sample_env and then run the container using the following command (**Note:** anything in <> should be replaced with info specific to you and without <>!):

```
docker run -rm -env_file ./<name of your file based on sample_env>.env -v <path/to/location/of/csv>:/logs/ robinhoodbot:0.5
```
Run the container daily at 4:10PM EST. This is shortly after the market closes for the day. This can be accomplished with a cronjob or similar task, depending on your OS.

## Why?!

- This is a work in progress. The final product will be MUCH simpler to run. My goal is to make it a single container that handles all sides of this and can just run all the time, where ever you want it (including in the cloud!)
- I was psyched when pycoder17 showed me this little project and sometimes we make minor changes to a friend's project not because we think we can do better but to pay homage to someone we respect
- I want to continue practicing turning apps not built to be containerized into containers.