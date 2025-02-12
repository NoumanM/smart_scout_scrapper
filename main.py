import os.path
import csv
import requests
import json
from time import sleep


from constants import token

total_pages = 0

url = "https://smartscoutapi-east.azurewebsites.net/api/sellers/search"

categories = {
    "3": "Home & Kitchen",
    "17": "Health & Household",
    "21": "Appliances",
    "2": "Arts, Crafts & Sewing",
    "13": "Automotive",
    "6": "Baby Products",
    "4": "Beauty & Personal Care",
    "31": "Books",
    "27": "CDs & Vinyl",
    "62": "Camera & Photo",
    "19": "Cell Phones & Accessories",
    "9": "Clothing, Shoes & Jewelry",
    "20": "Collectibles & Fine Art",
    "15": "Electronics",
    "26": "Entertainment",
    "25": "Gift Cards",
    "10": "Grocery & Gourmet Food",
    "38": "Movies & TV",
    "11": "Industrial & Scientific",
    "37": "Kitchen & Dining",
    "14": "Musical Instruments",
}

def decode_category(data):
    for row in data:
        category_id = row.get('primaryCategoryId')
        row['primaryCategoryId'] = categories.get(str(category_id), None)
    return data


def search_data(page_number):
    global total_pages
    start_row = (page_number - 1) * 1000
    end_row = page_number * 1000
    payload = json.dumps({
        "loadDefaultData": False,
        "filter": {
            "percentFba": {
                "min": "0",
                "max": "0"
            },
            "primaryCategoryId": {
                "values": [
                    "3",
                    "17"
                ],
                "filterType": "set"
            },
            "country": {
                "filterType": "text",
                "type": "startsWith",
                "filter": "US"
            }
        },
        "pageFilter": {
            "startRow": start_row,
            "endRow": end_row,
            "includeTotalRowCount": True,
            "sortModel": [],
            "fields": [
                "name",
                "amazonSellerId",
                "primaryCategoryId",
                "primarySubCategory",
                "estimateSales",
                "avgPrice",
                "percentFba",
                "numberWinningBrands",
                "numberAsins",
                "numberTopAsins",
                "street",
                "city",
                "state",
                "country",
                "zipCode",
                "businessName",
                "numBrands1000",
                "numberReviewsLifetime",
                "numberReviews30Days",
                "moMGrowth",
                "threeMonthGrowth",
                "sixMonthGrowth",
                "yearGrowth",
                "moMGrowthCount",
                "sixMonthGrowthCount",
                "isSuspended",
                "lastSuspendedDate",
                "startedSellingDate",
                "amazonSellerId",
                "note"
            ]
        }
    })
    headers = {
        'Accept': 'text/plain',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Authorization': f'Bearer {token}',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json-patch+json',
        'Origin': 'https://app.smartscout.com',
        'Referer': 'https://app.smartscout.com/',
        'Request-Id': '|d40380d04acb4b0a9fd9fda8753dd334.e9076f71eb10467f',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'X-SmartScout-Marketplace': 'US',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'traceparent': '00-d40380d04acb4b0a9fd9fda8753dd334-e9076f71eb10467f-01',
        'Cookie': 'ARRAffinity=3cd56cc2b0db1eb96628d469bd51aadad1fbc26e09c3764d456c7d963180807d; ARRAffinitySameSite=3cd56cc2b0db1eb96628d469bd51aadad1fbc26e09c3764d456c7d963180807d'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    json_response = json.loads(response.text)
    resp_data = json_response.get('payload', None)
    resp_data = decode_category(resp_data)
    total_pages = json_response.get('pageInfo')
    exists = False
    if resp_data:
        if os.path.exists('../output.csv'):
            exists = True
        with open('../output.csv', 'a+', newline='', encoding='utf-16') as file:
            writer = csv.writer(file)
            if not exists:
                writer.writerow(resp_data[0].keys())
            for row in resp_data:
                writer.writerow(row.values())


def process_data(selected_categories, fba_percent_min, fba_percent_max, country_filter):
    global total_pages
    search_data(1)
    if total_pages:
        total_pages = total_pages // 1000 + 1
        for page in range(2, total_pages + 1):
            search_data(page)
