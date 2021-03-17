import requests
import bs4
import csv

req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

listings_response = requests.get("https://www.zillow.com/homes/for_sale/77019_rb/", headers=req_headers)
soup = bs4.BeautifulSoup(listings_response.text, "lxml")

zillow_results = []
zillow_listings = soup.select(".list-card")


for listing in zillow_listings:
    listing_price = listing.select(".list-card-price")
    listing_address = listing.select(".list-card-addr")
    list_card_details = listing.select(".list-card-details")
    num_beds = ""
    num_baths = ""
    sq_ft = ""

    if (len(listing_price) > 0):
        listing_price = listing_price[0].getText()
    
    if (len(listing_address) > 0):
        listing_address = listing_address[0].getText()

    if (len(list_card_details) > 0):
        list_card_details = list_card_details[0].find_all("li")
        num_beds = list_card_details[0].getText()
        num_baths = list_card_details[1].getText()
        sq_ft = list_card_details[2].getText()

    
    listing_obj = {}
    listing_obj['price'] = listing_price
    listing_obj['address'] = listing_address
    listing_obj["beds"] = num_beds
    listing_obj["baths"] = num_baths
    listing_obj["sqft"] = sq_ft

    zillow_results.append(listing_obj)

    with open('zillow_listings.csv', 'w', encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=['price', 'address', 'beds', 'baths', 'sqft'])
        fc.writeheader()
        fc.writerows(zillow_results)