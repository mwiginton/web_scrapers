import requests
import bs4
import csv


req_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}
realtor_results = []

base_url = "https://www.realtor.com/realestateandhomes-search/77019"
listings_response = requests.get(base_url, headers=req_headers)
soup = bs4.BeautifulSoup(listings_response.text, "lxml")

realtor_listings = soup.select(".component_property-card")
print(len(realtor_listings))

for listing in realtor_listings:   
    listing_price = listing.select('span[data-label="pc-price"]')
    num_beds = listing.select('li[data-label="pc-meta-beds"]')
    num_baths = listing.select('li[data-label="pc-meta-baths"]')
    sqft = listing.select('li[data-label="pc-meta-sqft"]')
    address = listing.select('div[data-label="pc-address"]')
    
    if (len(listing_price) > 0):
        listing_price = listing_price[0].getText()
    
    if (len(num_beds) > 0):
        num_beds = num_beds[0].getText()

    if (len(num_baths) > 0):
        num_baths = num_baths[0].getText()
    
    if (len(sqft) > 0):
        sqft = sqft[0].getText()
    
    if (len(address) > 0):
        address = address[0].getText()

    listing_obj = {}
    listing_obj['price'] = listing_price
    listing_obj['address'] = address
    listing_obj["beds"] = num_beds
    listing_obj["baths"] = num_baths
    listing_obj["sqft"] = sqft

    if (type(listing_obj["price"]) == str and type(listing_obj["address"]) == str):
        realtor_results.append(listing_obj)

with open('realtor.com_listings.csv', 'w', encoding='utf8', newline='') as output_file:
    fc = csv.DictWriter(output_file, fieldnames=['price', 'address', 'beds', 'baths', 'sqft'])
    fc.writeheader()
    fc.writerows(realtor_results)