"""Collect information on a series from the Internet Movie Database."""

import json
from urllib.parse import urljoin
from time import sleep
import sys

import requests
from bs4 import BeautifulSoup

# Define constants.
IMDB_URL = "http://www.imdb.com"
FILENAME = "scraped.json"
HTML_ERROR = (
    "\nAn important HTML code element wasn't found!\n"
    "Check again whether you entered the correct URL."
)


class IMDbScraper():
    """Scrape and export data from imdb.com."""

    def __init__(self, filename):
        """Set attributes."""
        self.filename = filename
        self.first_episode, self.series_title = self.get_input()
        self.episodes = []

    @staticmethod
    def get_input():
        """Get series title and URL of the first episode."""
        while True:
            # Get URL from user.
            print("Please enter the URL of the first episode in a season.")
            first_episode = ""
            while not first_episode.startswith(IMDB_URL):
                first_episode = input("\nURL: ").strip()
                if not first_episode.startswith(IMDB_URL):
                    print(f"The URL has to start with \"{IMDB_URL}\".")
            # Get series title.
            request = requests.get(first_episode).text
            soup = BeautifulSoup(request, "html.parser")
            # If the HTML element containing the title is not found,
            # the program ends.
            try:
                titlediv = soup.find("div", class_="titleParent")
                series_title = titlediv.find("a")["title"]
            except AttributeError:
                print(HTML_ERROR)
                sys.exit()
            # Check to make sure we have the series the user wants.
            print(f"\nDo you want to scrape \"{series_title}\"?")
            answer = ""
            while answer not in ("yn") or len(answer) != 1:
                answer = input("Your answer (y/n): ").lower()
            if answer == "y":
                break
            else:
                print()
        return first_episode, series_title

    def scrape(self):
        """Scrape information on all episodes from every season.

        Scraped data for every episode:
        - episode title
        - episode number
        - season number
        - IMDb rating

        The series title is included as well.
        """
        url = self.first_episode
        print("\nPlease wait while episodes are scraped.\n")

        while url:
            request = requests.get(url).text
            soup = BeautifulSoup(request, "html.parser")
            # Create a dictionary to store episode data.
            episode = {}

            try:
                # Scrape header div with all revelant information.
                headerdiv = soup.find("div", class_="vital")
                # Get string containing broadcast date.
                # If the episode was not breadcast yet, skip it.
                bc_str = headerdiv.find("a", title="See more release dates")
            except AttributeError:
                print(HTML_ERROR)
                sys.exit()
            else:
                if "Episode airs" in bc_str.text:
                    url = ""
                    continue

            # Get episode title.
            episode_title = headerdiv.find("h1", itemprop="name").text.strip()
            episode["title"] = episode_title

            # Get episode and season number.
            se_ep = headerdiv.find("div", class_="bp_heading").text.split("|")
            season_number = se_ep[0].strip().split(" ")[-1]
            episode["season"] = int(season_number)
            episode_number = se_ep[1].strip().split(" ")[-1]
            episode["episode"] = int(episode_number)

            # Get IMDb rating.
            # For some episodes, IMDb shows no rating yet.
            # In that case, set rating to zero and show a message.
            try:
                rating = headerdiv.find("span", itemprop="ratingValue").text
            except AttributeError:
                rating = 0
            episode["rating"] = float(rating)

            # Append episode dictionary to episodes list.
            self.episodes.append(episode)
            # Print current episode.
            print(f"- \"{episode_title}\"", end=" ")
            print(f"(S{season_number} - E{episode_number})", end=" ")
            if rating:
                print()
            else:
                print("[no rating yet]")

            # Sleep for a moment to reduce server load.
            sleep(1)

            # Try to get URL of next episode.
            # If there is no URL, this is the last episode of the series.
            try:
                urlpart = headerdiv.find("a", class_="bp_item np_next")["href"]
            except TypeError:
                url = ""
            else:
                url = urljoin(IMDB_URL, urlpart)

    def store(self):
        """Store scraped information in a JSON file."""
        with open(self.filename, "w") as json_file:
            json.dump((self.series_title, self.episodes), json_file)
            print(f"\nScraped data was saved in the file {self.filename}.")


def main():
    """Call methods to scrape information and store it."""
    imdbs = IMDbScraper(FILENAME)
    imdbs.scrape()
    imdbs.store()

if __name__ == "__main__":
    main()
