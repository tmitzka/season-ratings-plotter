"""Plot season ratings from IMDB, based on scraped data."""

import os
import sys
import json

import matplotlib.pyplot as plt
import seaborn as sns

import imdb_scraper

# Get filename from scraper module.
# This ensures that we're looking for the right file to open.
FILENAME = imdb_scraper.FILENAME


class RatingsPlotter():
    """A class to create a graph of season ratings."""

    def __init__(self, filename):
        """Initialize attributes."""
        self.filename = filename
        self.series_title = ""
        # Define list for episode data.
        self.episodes = []
        # Define list for numbers of all scraped seasons.
        self.seasons = []

    def import_data(self):
        """Read scraped information from JSON file."""
        try:
            with open(self.filename) as json_file:
                series_title, episodes = json.load(json_file)
        except FileNotFoundError:
            print(f"ERROR: {self.filename} was not found!")
            sys.exit()

        first_season = episodes[0]["season"]
        last_season = episodes[-1]["season"]
        seasons = list(range(first_season, last_season+1))

        print(f"Data for \"{series_title}\"", end=" ")
        if len(seasons) == 1:
            print(f"(season {seasons[0]}) imported.\n")
        else:
            print(f"(seasons {seasons[0]}-{seasons[-1]}) imported.\n")
        return series_title, episodes, seasons

    def get_season_range(self):
        """Return season range for plot."""
        if len(self.seasons) == 1:
            season_range = range(self.seasons[0], self.seasons[0]+1)
        elif len(self.seasons) == 2:
            season_range = range(self.seasons[0], self.seasons[1]+1)
        else:
            # Ask user for min and max season to plot.
            print("\nPlease choose which seasons you want to include.\n")
            min_max_seasons = []
            required = ("first", "last")
            for req in required:
                season = ""
                while (
                        not season.isdigit() or
                        int(season) not in self.seasons
                ):
                    season = input(f"{req.title()} season number: ")
                    if not season.isdigit() or int(season) not in self.seasons:
                        print("Enter a number from", end=" ")
                        print(f"{self.seasons[0]} to {self.seasons[-1]}.\n")
                min_max_seasons.append(int(season))
                print()
            # Sort list, just in case the higher number
            # was entered first.
            min_max_seasons.sort()
            season_range = range(min_max_seasons[0], min_max_seasons[1]+1)
        return season_range

    def create_plot(self, season_range):
        """Create plot for season ratings."""
        # Use seaborn library to make the plot prettier.
        sns.set_style("darkgrid")
        colors = sns.color_palette("hls", len(season_range))

        for number in season_range:
            season = [eps for eps in self.episodes if eps["season"] == number]
            episode_numbers = [eps["episode"] for eps in season]
            season_ratings = [eps["rating"] for eps in season]
            plt.plot(
                episode_numbers,
                season_ratings,
                label=f"Season {number}",
                linewidth=3,
                color=colors.pop()
            )

        title = f"IMDB ratings for \"{self.series_title}\""
        plt.title(title)
        plt.xlabel("Episodes per season")
        plt.ylabel("Rating (1-10)")
        plt.legend()
        plt.show()

    def plot_ratings(self):
        """Call functions to scrape, store, import, and plot data."""
        print(
            "This program will create a graph to compare seasons "
            "of a series,\nbased on scraped data from the Internet "
            "Movie Database (IMDB).\n")

        scrape = False
        while True:
            # Scrape from IMDB if flag is set to True
            # or if data file isn't found.
            if scrape or not os.path.isfile(self.filename):
                imdb_scraper.main()
                scrape = False

            # Import scraped data.
            self.series_title, self.episodes, self.seasons = self.import_data()

            # Ask the user to confirm.
            print("Do you want to continue?")
            print(f"Enter \"y\" to show a graph for \"{self.series_title}\".")
            print("Enter \"n\" to scrape a different series instead.\n")
            answer = ""
            while answer not in "yn" or len(answer) != 1:
                answer = input("Your answer (y/n): ").lower()
            if answer == "n":
                print()
                scrape = True
                continue

            # Get season range and create plot.
            season_range = self.get_season_range()
            self.create_plot(season_range)
            break


def main(filename):
    """The main function."""
    srp = RatingsPlotter(filename)
    srp.plot_ratings()

if __name__ == "__main__":
    main(FILENAME)
