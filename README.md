# Python Stock Trader DOCKERIZED
This is a containerized version of psycoder17's nifty EMA Robinhood bot.

## Getting Started

You need [Docker Desktop](https://www.docker.com/products/docker-desktop) or another place to host Docker containers.
Clone this repo onto your PC (download as a ZIP, use GitHub Desktop, be fancy and CLI git, *pick your poison*).

## Run the trader
The container is the actual logic of the script and will do the actual trading based on the parameters you setout using an environmental file. First thing to do is build the image. Open your terminal/Powershell prompt, go into the docker file in this github repo you cloned and run the following:
```
docker build --tag robinhoodbot:0.8 .
```

Create an .env file based on the sample_env and then run the container using the following command (**Note:** anything in <> should be replaced with info specific to you and without <>!):

```
docker run -env_file ./<name of your file based on sample_env>.env -v <path/to/location/of/csv>:/logs/ robinhoodbot:0.8
```
Run the container daily at 4:10PM EST. This is shortly after the market closes for the day. This can be accomplished with a cronjob or similar task, depending on your OS.

## Why?!

- This is a work in progress. The final product will be MUCH simpler to run.
- I was psyched when psycoder17 showed me this little project and sometimes we make minor changes to a friend's project not because we think we can do better but to pay homage to someone we respect
- I want to continue practicing turning apps not built to be containerized into containers.
