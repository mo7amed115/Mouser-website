# Mouser-website
# Mouser Data Extraction Script

This Python script allows you to extract data from the Mouser API based on a list of manufacturer part numbers. The extracted data is saved to a CSV file for further analysis.

## Prerequisites

To run this script, you need to have the following dependencies installed:

- Python 3
- pandas
- subprocess
- json
- ast
- csv
- datetime

You can install the required Python libraries using pip:

```bash
pip install pandas subprocess json ast csv datetime

## Usage
1. Prepare the input file:
  - Create a CSV file containing the list of keywords in a column named "Input Manufacturer PartNumber".
  - Save the file as "new_missing.csv" in the "update" folder.
2. Run the script:
- Open a terminal or command prompt.
- Navigate to the project directory.
- Run the following command:

