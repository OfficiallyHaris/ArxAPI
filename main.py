#barebones of using arxiv API (and urllib); i will give arxiv api a pseudonym called ArxAPI
#ArxAPI uses atom 1.0;XML-based format (atom doc - https://www.ietf.org/rfc/rfc4287.txt)
#case example below; url variable queries (requests) retreives first ten results; query is all:electron (electron is search term)
# arXiv recommends feedparser for easy handling calling the api via HTTP and parsing - i might stick and further my flask library usage 

## calling the API
## http://export.arxiv.org/api/{method_name}?{parameters}


## practice task: retrieve N articles of chosen topic
## 1. only return the titles and summary 
## 1.1 return in a more digestable fashion
## 1.2 retrieve and store actual papers
## 1.3 start PDF extraction   

from flask import Flask, request, render_template_string, jsonify, send_file
import requests
import json
import feedparser

import pdf_extraction


app = Flask(__name__)
HTML_TEMPLATE = """
<!doctype html>
<title>ArXiv Paper Search</title>
<h2>Search for Papers</h2>
<form method="post">
  <label>Search Query:</label>
  <input type="text" name="query" placeholder="Enter paper topic"><br><br>

  <label>Start Index:</label>
  <input type="number" name="start" value="0"><br><br>

  <label>Number of Results:</label>
  <input type="number" name="max_results" value="10"><br><br>

  <input type="submit" value="Search">
</form>

{% if results %}
  <h3>Results:</h3>
  <ul>
  {% for paper in results %}
    <li>
      <strong>{{ paper.title }}</strong><br>
      Authors: {{ paper.authors }}<br>
      Published: {{ paper.published }}<br>
      <a href="{{ paper.pdf_url }}">PDF Link</a>
      <p>{{ paper.summary }}</p>

    <form action="/save_to_json/{{loop.index0}}" method="get">
      <button type="submit">Save This Paper as JSON</button>
    </form>
    </li>
    <hr>
  {% endfor %}
  </ul>
{% endif %}
"""


@app.route('/', methods=['GET', 'POST'])
def index():
    global saved_results
    results = []
    if request.method == 'POST':
      #POST/submitted form requests
      search_query = request.form.get('query', '')
      start = int(request.form.get('start', 0))
      max_results = int(request.form.get('max_results', 10))
      results = fetch_papers(search_query, start, max_results)  
  
      saved_results = results

    return render_template_string(HTML_TEMPLATE, results=results)


@app.route('/save_to_json/<int:paper_id>', methods=['GET'])
def save_to_json(paper_id):
    paper = saved_results[paper_id]
    #pdf_url = paper['pdf_url']
    pdf_response = requests.get(paper['pdf_url'])
    
    with open('Papers/'+paper['title']+'.pdf', 'wb') as f:
       f.write(pdf_response.content)
    
    parse_to_json(paper['title']+'.pdf', paper)

    
    return f"Paper{paper_id} saved as paper_{paper['title']}.json!"


@app.route('/api/papers', methods= ['GET'])
def api_papers():
    #request.args.get() refers to the query parameters in the URL e.g /papers?query=autoencoder&start=5&max_results
        #(for case in example below) #request.args.get(): retrieve query - (e.g) ?query=autoencoder save autoencoder to search_query variable
    search_query = requests.args.get('query', default='', type=str)
    start = requests.args.get('start', default='0', type=int)
    max_results = requests.args.get('max_results', default='10', type=int)

    results = fetch_papers(search_query, start, max_results)
    return jsonify({'results': results, 'count':len(results)})


def fetch_papers(search_query, start, max_results):
    base_url = 'http://export.arxiv.org/api/query?'
    query = f'search_query=all:{search_query}&start={start}&max_results={max_results}'
    
    header = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(base_url + query, headers=header)
    
    feed = feedparser.parse(response.content)

    results = []
    for entry in feed.entries:
        paper = {
            'title': entry.title,
            'authors': ", ".join([author.name for author in entry.authors]),
            'summary': entry.summary,
            'published': entry.published,
            'pdf_url': next(
                (link.href for link in entry.links if hasattr(link, 'title') and link.title == 'pdf'), None
            )
        }
        results.append(paper)
        
    
    return results

def parse_to_json(filePath, paper):
  
  dataset_name, dataset_keyword_attributes = pdf_extraction.parse_datasetName_and_attributes(filePath)
  # print(dataset_name)
  # print(dataset_keyword_attributes)
  data = {
    **paper, 
     "dataset name": dataset_name,
     "dataset keywords/attributes": dataset_keyword_attributes}

  # merge_datasetData = {**paper, data}

  with open(f'Papers/paper_{filePath}.json', 'w', encoding='utf-8') as f:
    json.dump(data,f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    app.run(debug=True)

