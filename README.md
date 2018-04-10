# Season Ratings Plotter
This program creates a graph that shows user ratings for one or several seasons
of a TV series. The ratings and other data are scraped (downloaded) from the
[Internet Movie Database (IMDb)](http://www.imdb.com). You can include as many
seasons in the plot graph as you like.

## Getting started
### Prerequisites
Here is what you need:
- Python version 3.6 or higher
- Python libraries **matplotlib** and **seaborn**
These two libraries are not included in the Python Standard Library. An easy way
to install them is by using *pip*. Open a terminal and enter these commands:
```
pip install matplotlib
pip install seaborn
```
### ratings_plotter.py
To get things going, run the script *ratings_plotter.py* in this repository.
That's the main program. It will automatically import the module
*imdb_scraper.py* to scrape the required data. If you want, you can use the
scraper module on its own, but you don't have to.

### Scraping Data
The program will ask you for the URL of the first episode in a season. 
For every TV series there is a summary page on IMDb.com, and there's also a
page for every single episode. It's important that you look up the IMDb page
of an episode, preferably the first one. Here is an
[example](http://www.imdb.com/title/tt4593118/?ref_=ttep_ep1). Copy the URL and
 paste it to the prompt in your terminal.

First, you have to confirm that this is the right series. Starting with the
episode from the URL you provided, the program will then collect data on every
following episode, one season after another. When it reaches the end of the
series, it saves all gathered data in a file named *scraped.py*.

### Creating the Plot Graph
The scraping module has done its task, now it's time to create the graph.
If you scraped more than two seasons, you can choose which of them you want
to include in the graph. The graph is displayed in a new window. When you close
it, the program ends. You can **adjust the size** of the window by dragging the
borders, and you can **save the graph** by clicking the disk icon below.

When you run the program again, it will find and import the data file. So if
you want to create a new graph for the same series, you can skip the scraping
part. The file is overwritten after the scraping of a new series is finished.
