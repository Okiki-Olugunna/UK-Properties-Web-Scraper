# from urllib import response
import requests
from bs4 import BeautifulSoup

# import json
import csv


class RightMoveScaper:
    results = []

    # function to make a request to the RightMove search url
    def fetch(self, url):
        print(f"\nHTTP GET Request to URL: \n {url} \n")
        response = requests.get(url)
        print(f" | STATUS CODE: {response.status_code} | \n")

        return response

    # function to parse the desired data from RightMove
    def parse(self, html):
        # print(html)

        content = BeautifulSoup(html, "lxml")

        # all of the titles of the properties
        titles = [
            title.text.strip()
            for title in content.findAll("h2", {"class": "propertyCard-title"})
        ]
        # all of the addresses
        addresses = [
            address["content"]
            for address in content.findAll("meta", {"itemprop": "streetAddress"})
        ]
        # property description
        descriptions = [
            description.text
            for description in content.findAll(
                "span", {"data-test": "property-description"}
            )
        ]
        # prices
        prices = [
            price.text.strip()
            for price in content.findAll("div", {"class": "propertyCard-priceValue"})
        ]
        # date property was added / edited on the site
        dates = [
            date.text.strip()
            for date in content.findAll(
                "span", {"class": "propertyCard-branchSummary-addedOrReduced"}
            )
        ]
        dates_2 = [
            date.text.split(" ")[-1]
            for date in content.findAll(
                "span", {"class": "propertyCard-branchSummary-addedOrReduced"}
            )
        ]
        # sellers
        sellers = [
            seller.text.split("by")[-1].strip()
            for seller in content.findAll(
                "span", {"class": "propertyCard-branchSummary-branchName"}
            )
        ]
        # links to the images of the properties
        images = [
            image["src"] for image in content.findAll("img", {"itemprop": "image"})
        ]

        # appending the parsed data to the results array
        for index in range(0, len(titles)):
            self.results.append(
                {
                    "Title": titles[index],
                    "Address": addresses[index],
                    "Description": descriptions[index],
                    "Price": prices[index],
                    "Date": dates[index],
                    "Date2": dates_2[index],
                    "Seller": sellers[index],
                    "Image": images[index],
                }
            )

            # print(json.dumps(item, indent=2))

    # function to store the data in a csv spreadsheet file
    def to_csv(self):
        with open("RightMoveProperties.csv", "w") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)

            print(
                "Property data has been scraped and stored in the file 'RightMoveProperties.csv' "
            )

    def run(self):
        # index represents the page number - starts at 0, goes to 24, 48 etc..
        # covers up to 4 pages of results
        for page in range(0, 3):
            index = page * 24
            # the url of the page to scrape
            # this specific link is for South London properties for sale under £100k
            url = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E92051&minBedrooms=1&maxPrice=100000&sortType=1&index={index}&propertyTypes=&mustHave=&dontShow=&furnishTypes=&keywords="

            response = self.fetch(url)
            self.parse(response.text)
            # storing the data in a spreadsheet csv file
            self.to_csv()


if __name__ == "__main__":
    scraper = RightMoveScaper()
    scraper.run()
