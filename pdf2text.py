from pdfminer.high_level import extract_text


def read_pdf(file_path):
    # Extract the text from the PDF, maintaining the original layout
    text = extract_text(file_path)
    return text


# Use the function
file_path = 'C:/Users/nanda/Downloads/HP/HP.pdf'  # replace with your file path
pdf_text = read_pdf(file_path)
# print(pdf_text[:1000])


with open('books/HP_text_formatted.txt', 'w') as file:
    # Write the string to the file
    file.write(pdf_text)