from datetime import datetime
import time
import pandas as pd
import subprocess
import json
import ast
import csv
import datetime

# First section
#data = pd.read_excel("Mouser_Input.xlsx")
#data = pd.read_csv("missing.csv")
data = pd.read_csv("./update/new_missing.csv")

data = data["Input Manufacturer PartNumber"].tolist()
# =======================================================
print("The number of elements =", len(data))
s = int(input("Start from: "))
e = int(input("To: "))
new_data = data[s:e]
print("The number of new elements =", len(new_data))
# =======================================================
# timestamp = datetime.now().strftime("%H%M")
name = f"output_{s}_{e}"
output_file = f"{name}.csv"  # Specify the output file name

# Create an empty list to store the results
results = []
missed = []
data = []

api = input('Enter your API : ')
# Iterate over the keywords
for keyword in new_data:
    try:
        curl_command = [
            'curl',
            '-X', 'POST',
            f'https://api.mouser.com/api/vtext/search/keyword?apiKey={api}',
            '-H', 'accept: application/json',
            '-H', 'Content-Type: application/json',
            '-d', f'{{ "SearchByKeywordRequest": {{ "keyword": "{keyword}", "records": 0, "startingRecord": 0, "searchOptions": "string", "searchWithYourSignUpLanguage": "string" }} }}'
        ]

        # Execute the curl command and capture the output
        output = subprocess.check_output(curl_command)

        # Decode the output as a string
        output_str = output.decode('utf-8')

        # Convert the output string to JSON
        output_json = json.loads(output_str)

        # Append the result to the list
        results.append(output_json)
        print(f"the number of products = {len(results)}")
        time.sleep(1)

    except:
        pass

# Save the results to a JSON file
with open(f'{name}.json', 'w') as file:
    json.dump(results, file)

print(f"Created {name}.json file")

# Second section
with open(f'{name}.json', 'r') as file:
    json_data = json.load(file)

# Get the length of the JSON data
for f in json_data:
    try:
        output = f['SearchResults']['Parts']
        data.append(output)
    except:
        missed.append("Missing")
        pass

print(f"The True Data   ==> {len(data)}")
print(f"The Failed Data ==> {len(missed)}")

df = pd.DataFrame(data)
name2 = f"update_{name}"
# Create the filename with the timestamp
filename = f"{name2}.csv"
# Save the DataFrame to a CSV file
df.to_csv(filename, index=False)

print(f"Created {name2}.json file")

# Third section
data = pd.read_csv(f"{name2}.csv")
filtered_data = data['0']
filterd_dict = []
for i in range(len(filtered_data)):
    try:
        data_dict = ast.literal_eval(filtered_data[i])
        filterd_dict.append(data_dict)
    except:
        print("Error on ==>", i)
print(len(filterd_dict))


def extract_product_data(data):
    current_datetime = datetime.datetime.now()
    # Extracting the data from the dictionary and filling missing values with "Not available"
    manufacturer = data.get('Manufacturer', 'Not available')
    manufacturer_part_number = data.get('ManufacturerPartNumber', 'Not available')
    source = data.get('Source', 'mouser.com')
    category = data.get('Category', 'Not available')
    competitor = 'Mouser'
    competitor_part_number = data.get('MouserPartNumber', 'Not available')
    if competitor_part_number == 'N/A':
        competitor_part_number = 'Not available'
    availability = data.get('Availability', 'Non-Stocked, Call for Quote')
    factory_lead_time = data.get('LeadTime', 'Not available')
    description = data.get('Description', 'Not available')
    currency = 'USD'
    URL = data.get('ProductDetailUrl', 'Not available')
    # Extracting PriceBreaks data
    price_breaks = data.get('PriceBreaks', [])
    if len(price_breaks) == 0:
        status = 'No price'
    else:
        status = "Priced"

    cache_time = current_datetime.strftime("%m/%d/%Y %I:%M:%S %p")
    life_cycle = data.get('LifecycleStatus', "Not available")
    if life_cycle is None:
        life_cycle = "Not available"

    # Assigning quantities and prices to variables
    quantities = []
    prices = []
    for i in range(10):
        quantity = price_breaks[i]['Quantity'] if i < len(price_breaks) else 'Not available'
        price = price_breaks[i]['Price'] if i < len(price_breaks) else 'Not available'
        quantities.append(quantity)
        prices.append(price)

    # Creating a dictionary with the extracted data
    extracted_data = {
        "Manufacturer": manufacturer,
        "Manufacturer Part Number": manufacturer_part_number,
        "Source": source,
        "Category": category,
        "Competitor": competitor,
        "Competitor Part Number": competitor_part_number,
        "Availability": availability,
        "Factory Lead Time": factory_lead_time,
        "Quantity1": quantities[0],
        "Quantity2": quantities[1],
        "Quantity3": quantities[2],
        "Quantity4": quantities[3],
        "Quantity5": quantities[4],
        "Quantity6": quantities[5],
        "Quantity7": quantities[6],
        "Quantity8": quantities[7],
        "Quantity9": quantities[8],
        "Quantity10": quantities[9],
        "Price1": prices[0],
        "Price2": prices[1],
        "Price3": prices[2],
        "Price4": prices[3],
        "Price5": prices[4],
        "Price6": prices[5],
        "Price7": prices[6],
        "Price8": prices[7],
        "Price9": prices[8],
        "Price10": prices[9],
        "Currency": currency,
        "URL": URL,
        "Status": status,
        "Cache Time": cache_time,
        "Life Cycle": life_cycle,
        "Description": description
    }

    return extracted_data


# Specify the output CSV file name
output_file = f'product_data_{s}_{e}.csv'

# Extract and save the product data to a CSV file
with open(output_file, 'w', newline='') as csvfile:
    fieldnames = [
        "Manufacturer", "Manufacturer Part Number", "Source", "Category", "Competitor",
        "Competitor Part Number", "Manufacturer", "Manufacturer Part Number", "Availability",
        "Factory Lead Time", "Quantity1", "Price1", "Quantity2", "Price2", "Quantity3", "Price3", "Quantity4", "Price4",
        "Quantity5", "Price5", "Quantity6", "Price6", "Quantity7", "Price7", "Quantity8", "Price8",
        "Quantity9", "Price9", "Quantity10", "Price10", "Currency", "URL", "Status", "Cache Time", "Life Cycle",
        "Description"
    ]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Extract and write the product data for each dictionary
    for data_dict in filterd_dict:
        product_data = extract_product_data(data_dict)
        writer.writerow(product_data)

print("Product data saved to", output_file)
