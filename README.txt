# 1.125_fproj - Proddis Product Discoverer

The primary components of this project are: 
1) Python script to scrape reddit and running Google NLP API on the reddit data for entity identification and sentiment
scoring. 
2) MySQL db to which the analyzed data is written to, and then aggregated within SQL 
3) Python flask app that integrates the underlying HTML template dynamically with the data from the MySQL db. 

Requirements:
1. Google NLP API requires a Google Cloud project which provides authentication credentials through which the API runs. 
2. Reddit developer account is required to use PRAW library for scraping reddit. 
3. Python libraries: pandas, sqlalchemy, google.cloud, bing_images
4. MySQL db to be set up

Running the project:
1. reddit_scrape.py must be run first, which will populate MySQL db
2. Run the create_agg_data.sql script to aggregate the data and perform entity-level calculations and grouping 
3. Run the image_search.py script to generate image URLs for the entity names, which will create another db table. May be easier
to upload the 'ent_images.csv' file directly due to string formatting challenges of writing directly to db from Python.  
4. Run the app.py script, which will load the front-end based on the index.html template file and pull in data from the db 