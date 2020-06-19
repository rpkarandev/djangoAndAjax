# Using Ajax with Django
Here are few simple exercises showing implementation of ajax along with Django.  
- Exercise 1: Test continuous talk between server and client
- Exercise 2: Peform post request with file attached 
- Exercise 3: Peform post request with file attached - the file is sent as chunks of 100 kb


## My story 
The story started with myself building a website to upload multiple files as chunks using Django. Unfortunately, existing respos did not help me much. Wasted few days! I started building step by step. Hope the repo will be useful to someone looking for a solution.


## System configuration
- Apache 2.2
- modWSGI
- Python 3.5
- Django 2.0

### Caution
Repeated file upload request may overwhelm and load your db. Leads to dblock error especially if you are using sqlite. Adjust the time between the requests accordingly.
