import requests
import bs4
import csv

req_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

redfin_results = []
page_num = 1
continue_paging = True

while continue_paging:
    base_url = "https://www.redfin.com/zipcode/77019/filter/sort=lo-price/page-{}"
    listings_response = requests.get(base_url.format(page_num), headers=req_headers)
    soup = bs4.BeautifulSoup(listings_response.text, "lxml")


    redfin_listings = soup.select(".HomeCardContainer")

    print("Current Page")
    print(page_num)

    # only go through 6 pages for now
    if (page_num == 6):
        continue_paging = False

    for listing in redfin_listings:
        listing_price = listing.select(".homecardV2Price")
        address = listing.select(".homeAddressV2")
        home_stats = listing.select(".HomeStatsV2")
        num_beds = ''
        num_baths = ''
        sqft = ''

        if(len(listing_price) > 0):
            listing_price = listing_price[0].getText()
        
        if (len(address) > 0):
            address = address[0].getText()
        
        if(len(home_stats) > 0):
            home_stats = home_stats[0].select(".stats")
            num_beds = home_stats[0].getText()
            num_baths = home_stats[1].getText()
            sqft = home_stats[2].getText()
        
        listing_obj = {}
        listing_obj['price'] = listing_price
        listing_obj['address'] = address
        listing_obj["beds"] = num_beds
        listing_obj["baths"] = num_baths
        listing_obj["sqft"] = sqft

        if (type(listing_obj["price"]) == str and type(listing_obj["address"]) == str):
            redfin_results.append(listing_obj)
            
    page_num += 1 

print("Data process complete. Writing output file")
with open('redfin_listings.csv', 'w', encoding='utf8', newline='') as output_file:
    fc = csv.DictWriter(output_file, fieldnames=['price', 'address', 'beds', 'baths', 'sqft'])
    fc.writeheader()
    fc.writerows(redfin_results)
print("Output file complete")