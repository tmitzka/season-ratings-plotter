# Season Ratings Plotter
**NOTE: The program stopped working a while ago and is no longer maintained.**

This program creates a plot graph that shows user ratings for one or several
seasons of a TV series. Ratings and other data are scraped (downloaded) from the
[Internet Movie Database (IMDb)](https://www.imdb.com). You can include as many
seasons in the plot graph as you like.

## Getting Started
### Prerequisites
Here is what you need:
- Python version 3.6 or higher
- Python library **requests**
- Python library **beautifulsoup4**
- Python library **matplotlib**
- Python library **seaborn**

These four libraries are not included in the Python Standard Library. An easy
way to install them is by using *pip*. Open a terminal and enter the following
commands:
```
pip install requests
pip install beautifulsoup4
pip install matplotlib
pip install seaborn
```
### Run ratings_plotter.py
To get things going, run the script *ratings_plotter.py* in this repository.
That's the main program. It will automatically import the module
*imdb_scraper.py* to scrape the required data. If you want you can use the
scraper module on its own, but you don't have to.

### Scraping Data
The program will ask you for the URL of an episode. For every TV series,
IMDb.com has a summary page as well as pages for each episode. It's
important that you look up the IMDb page of an *episode*. Preferably you should
choose the first one in a season, but that's up to you. Here is an
[example](https://www.imdb.com/title/tt4593118/?ref_=ttep_ep1). Copy the URL and
paste it to the prompt in your terminal.

Starting with the episode from the URL you provided, the program will collect
data on every following episode, one season after another. When it reaches the
end of the series, it saves all gathered data in a file named *scraped.json*.

### Creating the Plot Graph
If you scraped more than one season, you can choose which of them you want
to include in the graph. The graph is displayed in a new window. When you close
it, the program ends. You can **adjust the size** of the window by dragging its
borders, and you can **save the graph** by clicking the disk icon below.

When you run the program again, it will find and import the data file. So if
you want to create a new graph for the same series, you can skip the scraping
part. The file is overwritten after the scraping of a new series is finished.

## Good to Know
- If you're only interested in, say, season 8 and newer, start with the first
episode of that season.
- Episodes with a future release date won't be scraped.
- For some episodes, the IMDb shows no rating yet. The program will insert an
episode rating of 0 (zero) instead.
