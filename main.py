import os
import re
import csv
import PyPDF2

# Function to extract the highest total amount from the given text
def extract_highest_total_amount(text):
    # Regular expression pattern to find the total amounts
    pattern = r'(?:total)[\s\S]*?(\$\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
    # Find all matches in the text
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    # Convert matched amounts to float and remove '$' and ',' characters
    amounts = [float(match.replace("$", "").replace(",", "")) for match in matches]
    # Return the highest amount in the formatted string, or None if no matches found
    return "${:,.2f}".format(max(amounts)) if amounts else None

# Function to process PDF files in the given folder and write the results to a CSV file
def process_pdfs(folder_path, csv_output_file):
    # Open the CSV file for writing
    with open(csv_output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write the header row
        csv_writer.writerow(['File', 'Highest Total Amount'])

        # Iterate through all files in the folder
        for file in os.listdir(folder_path):
            # Check if the file has a .pdf extension
            if file.endswith(".pdf"):
                # Get the full path of the PDF file
                pdf_path = os.path.join(folder_path, file)
                # Open the PDF file
                with open(pdf_path, 'rb') as pdf_file:
                    # Read the PDF file using PdfReader
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    # Initialize a variable to store the extracted text
                    text = ""
                    # Iterate through all pages in the PDF file
                    for page_num in range(len(pdf_reader.pages)):
                        # Extract text from the current page
                        page = pdf_reader.pages[page_num]
                        text += page.extract_text()

                # Extract the highest total amount from the text
                highest_total_amount = extract_highest_total_amount(text)
                # If the highest total amount is found, write it to the CSV file
                if highest_total_amount:
                    csv_writer.writerow([file, highest_total_amount])
                # Otherwise, print a message indicating that the amount was not found
                else:
                    print(f"Highest total amount not found in {file}")

if __name__ == '__main__':
    # Specify the folder path containing the PDF files
    folder_path = "C:/Users/Dana/PycharmProjects/GetInvoiceAmountwithPyPDF2"
    # Specify the name of the output CSV file
    csv_output_file = 'output.csv'
    # Call the process_pdfs function with the folder path and output CSV file
    process_pdfs(folder_path, csv_output_file)
