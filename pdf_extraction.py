from pdfminer.high_level import extract_pages
from pdfminer.layout import LTPage, LTTextContainer, LTChar, LTTextBox, LTTextLine
import re

# pdf_document = 'Comparison of Autoencoders for tokenization of ASL datasets.pdf'

def get_paragraphs(page):
    return[
        paragraph
        for paragraph in page
        if isinstance(paragraph, LTTextContainer) and paragraph.get_text().strip()
    ]

def get_textline(paragraph):
    return[
        line.get_text()
        for line in paragraph
        if isinstance(line, LTTextLine) and line.get_text().strip()    
    ]

def get_font_sizes(paragraph:LTTextContainer): #Retrieves a list of font sizes for characters in the paragraph.
    # for line in paragraph:
    #     print(type(line))
    return[
        char.size
        for line in paragraph #iterate through the (objects within) text containers (lines in the paragraph; elements in the text container)
        if isinstance(line, LTTextLine)
        for char in line # iterates through the objects itself 
        if isinstance(char,LTChar)
    ]
#font_sizes = get_font_sizes(page_layout) # nested iteration order : elements in page (text containers); elements within the object 
#page; text containers;elements within container; the elements within container again 
def list_sized_paragraphs(page):
    return[
        (max(get_font_sizes(paragraph)), paragraph.get_text()) #gets the maximum of the largest tuple(like a list within the list; which list within the list is the biggest; not the max element; the max list)
        for paragraph in page # Iterates over each element on the page.
        if isinstance(paragraph, LTTextContainer) and paragraph.get_text().strip()
    ]

#(?: ... ) This is a non-capturing group, meaning it groups the pattern inside but doesn't store it as a captured group.
#\s+ Matches one or more whitespace characters (spaces, tabs, or line breaks).
#...\s+)* The * here applies to the whole non-capturing group, meaning:Zero or more occurrences of:

def extract_dataset_name(textLines):
    exclude_keywords_for_datasetNameMatching = ["Validation","Test", "Testing", "Train", "Training"]
    #data_type = ["Images","Text"]
    dataset_nameMatches = re.findall(r'(?:[A-Z][a-zA-Z0-9\-]*\s+)*[A-Z][a-zA-Z0-9\-]*\s+Dataset', textLines)
    dataset_nameMatches = [m for m in dataset_nameMatches if not any(word.lower() in m.lower() for word in exclude_keywords_for_datasetNameMatching)]
    return dataset_nameMatches

def extract_dataset_attirbutes(textLines):
    # keywords = ["validation", "test", "testing", "training", "train" ]
    # data_type = ["images", "text"]
    attributes = re.findall(r'(\d{1,3}(?:,\d{3})*\s+(?:images|samples|instances|observations|examples)(?:\s+for\s+(?:training|validation|testing|test|train))?)', textLines)
    return attributes

def parse_datasetName_and_attributes(PDFfilepath):
    found_dataset_name = []
    data_set_attributes = []
    for page_layout in extract_pages(PDFfilepath):
        paragraphs = get_paragraphs(page_layout)
        for p in paragraphs:
            if extract_dataset_name(p.get_text()):
                found_dataset_name.append(extract_dataset_name(p.get_text()))
            if extract_dataset_attirbutes(p.get_text()):
                data_set_attributes.append(extract_dataset_attirbutes(p.get_text()))
    
    
    # print("----")
    # for elements in found_dataset_name:
    #     print(elements)
    # for elements in data_set_attributes:
    #     print(elements)
    # print("----")

    #Pythonic (below) way does not work with numpy; when implicitly checking for empty list; not important for now, highly unlikely to use numpy, at least at this stage
    if not found_dataset_name:
        found_dataset_name.append(["Not Found"])
    
    if not data_set_attributes:
        data_set_attributes.append(["Not Found"])
        

    returnParsedData = [found_dataset_name,data_set_attributes]
    return returnParsedData


# filepath = 'Adversarial Autoencoders in Operator Learning.pdf'
# parse_datasetName_and_attributes(filepath)
#parse_datasetName_and_attributes_to_json(pdf_document)

