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

## **Usage**
1. Prepare the input file:
  - Create a CSV file containing the list of keywords in a column named "Input Manufacturer PartNumber".
  - Save the file as "new_missing.csv" in the "update" folder.

2. Run the script:
  - Open a terminal or command prompt.
  - Navigate to the project directory.
  - Run the following command:(python main.py)

3. Provide necessary inputs:
  - Enter the start and end indices to specify the range of keywords to process.
  - Enter your Mouser API key when prompted.

4. Wait for the script to complete:
  - The script will send API requests for each keyword and save the results as JSON files.
  - It will then extract relevant data from the JSON files and save it as a CSV file.

5. Check the output:

  - The final output will be saved as a CSV file named "product_data_[start]_[end].csv" in the project directory.

# Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.





 

