import requests
from datetime import datetime
import os

base_url = 'https://myaussie-api.aussiebroadband.com.au/billing/transactions?group=true'

api_token = "<API_TOKEN>"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
    'Authorization': 'Bearer ' + api_token
}

# Define the current and previous year
this_year = "2024"
last_year = "2023"

# Define the date range for filtering receipts
start_date = datetime.strptime(f"{last_year}-07-01", "%Y-%m-%d")
end_date = datetime.strptime(f"{this_year}-06-30", "%Y-%m-%d")

# Define the directory to save the receipts
download_directory = r"C:\Users\" # CHANGE THIS TO YOUR DESIRED LOCATION

# Ensure the download directory exists
os.makedirs(download_directory, exist_ok=True)

# Function to check if a date is within the specified range
def is_within_date_range(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return start_date <= date <= end_date

# Fetch the data from the API
response = requests.get(base_url, headers=headers)

if response.status_code == 200:
    json_data = response.json()

    # Filter the JSON data for receipts within the date range
    filtered_receipts = []
    for month, transactions in json_data.items():
        for transaction in transactions:
            if transaction['type'] == 'receipt' and is_within_date_range(transaction['time']):
                filtered_receipts.append(transaction)
    
    # Print the filtered receipts
    #print(filtered_receipts)

    # Function to download a receipt and save it with the appropriate filename
    def download_receipt(transaction):
        receipt_id = transaction['id']
        receipt_date = datetime.strptime(transaction['time'], "%Y-%m-%d")
        receipt_month = receipt_date.strftime("%B %Y")
        receipt_url = f"https://myaussie-api.aussiebroadband.com.au/billing/receipts/{receipt_id}"
        
        receipt_response = requests.get(receipt_url, headers=headers)
        
        if receipt_response.status_code == 200:
            filename = f"Aussie Broadband receipt {receipt_month} {receipt_id}.pdf"
            file_path = os.path.join(download_directory, filename)
            with open(file_path, 'wb') as file:
                file.write(receipt_response.content)
            print(f"Downloaded receipt: {file_path}")
        else:
            print(f"Failed to download receipt {receipt_id}")

    # Download each filtered receipt
    for receipt in filtered_receipts:
        download_receipt(receipt)
else:
    print(f"Failed to retrieve data: {response.status_code}")
