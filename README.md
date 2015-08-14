# Wikipedia crawler
Script to identify the most controversial wikipedia pages based on their revision history.

# TO DO:
- Write crawler.py
  - Random walker from main page.
- Extract info from page.
  - Categories - Are some categories more prone to edit wars?
  - Extract first 1000 revisions.
  - Extract page title.
- Store data in file.
  - Dictionary: { URL : { CATEGORIES, REVISION HISTORY, TITLE, FIRST PARAGRAPH (x) } } 
  - Write to Pickle.
    - Wrote to JSON instead. 
- Process data.
  - Insert cut-off point at 1-1-2014. (?)
  - Turn revision history into datetime objects. 
- Analyze data.
  - Which pages has the most revisions in the shortest amount of time?
    - Is this dependent on category?
  - Build classifier? Predict categories from revision history / first paragraph?
