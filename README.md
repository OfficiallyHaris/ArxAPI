# ArxAPI
This project is a lightweight Python tool that automates the parsing arXiv academic papers to extract key information and metadata using arXiv API and Python PDF extracting libraries (pdfminer.six). Current development is focused on working with arXiv's API. Future versions may expand to other academic sources where PDF extraction is viable.  

Overview: 

Decided on Flask to implement a simple, rudimentary (prototyping) RESTful API.

Explored and integrated the arXiv API, using their official examples.
    – Paper title, authors, published date, and summary were easily retrieved thanks to the API’s built-in methods.   

pdfminer.six evaluated for PDF text extraction:
  - Pros: Strong text extraction capabilities, including support for advanced layout parsing; no licensing concerns (unlike PyMuPDF).
  - Cons: Limited or no support for image extraction; lacks built-in table extraction functionality.
  - Next steps: Likely to require custom implementation or use in conjunction with another library for advanced parsing.

Built early-stage regex rules to extract:
  - Dataset names.
  - Dataset sizes (partial success).
    
(All of the above was within a week with limited time and focus available)


Current limitations: 
- Regex implementation is too simple; not yet generalisable or reliable.
- No support for bulk processing — only extracts from a single paper at a time.

Development phase for version 1.0:

Address current limitations and restructure logic where needed.

Generalise and clean up regex rules for dataset detection.

Design a more robust metadata extraction process.

Extract additional fields:
  - Dataset type.
  - Number of classes.
  - Train/test/validation splits.

Future Versions: 
Implement more complex extraction features:
  - Table and image parsing.
  - Methodology summarisation.
  - Inference for missing or implicit metadata (e.g. dataset names).
    
Note: Simple, stand-alone regex is only planned for the early stage. Later on, I’ll move toward experimenting with more robust (and hopefully less confusing) tools and methods. Some possible directions include:
  - Use layout-aware functions within pdfminer.six or other document data extraction libraries, to identify likely sections.
  - Keyword-based or rule-based pattern matching and prefiltering.  
  - Potential use of NLP or language models for inferred extraction.
  

  
