import requests
import bs4
import csv

req_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

trulia_results = []
page_num = 1
continue_paging = True

base_url = "https://www.trulia.com/for_sale/77019_zip/price;a_sort/"
listings_response = requests.get(base_url.format(page_num), headers=req_headers)
soup = bs4.BeautifulSoup(listings_response.text, "lxml")

trulia_listings = soup.select('div[class*="InteractivePropertyCardContainer-"]')

for listing in trulia_listings:
        # data-testid="property-beds"
        listing_price = listing.find_all("div", attrs={"data-testid":"property-price"})
        address = listing.find_all("div", attrs={"data-testid":"property-street"})
        sqft = listing.find_all("div", attrs={"data-testid":"property-floorSpace"})
        num_beds = listing.find_all("div", attrs={"data-testid":"property-beds"})
        num_baths = listing.find_all("div", attrs={"data-testid":"property-baths"})

        if (len(listing_price) > 0):
            listing_price = listing_price[0].getText()
        
        if (len(address) > 0):
           address = address[0].getText()

        if (len(sqft) > 0):
           sqft = sqft[0].getText()
        
        if (len(num_beds) > 0):
           num_beds = num_beds[0].getText()

        if (len(num_baths) > 0):
           num_baths = num_baths[0].getText()   

        listing_obj = {}
        listing_obj['price'] = listing_price
        listing_obj['address'] = address
        listing_obj["beds"] = num_beds
        listing_obj["baths"] = num_baths
        listing_obj["sqft"] = sqft

        print(listing_obj)

        if (type(listing_obj["price"]) == str and type(listing_obj["address"]) == str):
            trulia_results.append(listing_obj) 
