import praw 
import pandas as pd
from praw.models import MoreComments

from sqlalchemy import create_engine
import pymysql

import os 
from google.cloud import language_v1

credential_path = "/Users/tommyshi/Documents/Academics/Fall 2021/1.125 Architecting and Engineering Software Systems/Final_Proj/1.125_fproj/prod-seeker-332518-f2e20d287e46.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

reddit = praw.Reddit(client_id='TxY72RVlJM3XkOtouvTAaw',
    client_secret='_sRx1WW5Ub4_nqXH3NFoi8JgFVenCg', 
    user_agent='prods',
    username='lolcatster',
    password='lolcats123')

# scrape relevant subreddits
subreddits = ['hometheater', '4kTV', 'HTBuyingGuides']
#, '4kTV', 'BuyItForLife']
comments = pd.DataFrame()
for sr in subreddits:
    for post in reddit.subreddit(sr).top("all", limit = 100):
        post.comments.replace_more(limit=0)
        for top_level_comment in post.comments:
            if top_level_comment.score > 1:
                comments = comments.append({'post_title': post.title,
                                            'post_ratio': post.upvote_ratio, 
                                            'comment_body':top_level_comment.body, 
                                            'comment_score': top_level_comment.score,
                                            'post_comments': post.num_comments,
                                            'post_date': post.created,
                                            'comment_date':top_level_comment.created_utc,
                                            'post_id': post.id,
                                            'comment_id': top_level_comment.id}, 
                                            ignore_index=True)

## Use Google NLP entity analysis 
def sample_analyze_entity_sentiment(key, text_content):
    """
    Analyzing Entity Sentiment in a String

    Args:
      text_content The text content to analyze
    """
    client = language_v1.LanguageServiceClient()
    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}
    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_entity_sentiment(request = {'document': document, 'encoding_type': encoding_type})
    # Loop through entitites returned from the API
    df = pd.DataFrame()
    
    for entity in response.entities:
        if language_v1.Entity.Type(entity.type_).name != 'CONSUMER_GOOD':
            continue
        sentiment = entity.sentiment
        for mention in entity.mentions:
            if language_v1.EntityMention.Type(mention.type_).name != 'PROPER':
                continue
#        if language_v1.Entity.Type(entity.type_).name == 'CONSUMER_GOOD' and \
#        sentiment.score > 0 and entity.salience > 0.75:
            print(u"Representative name for the entity: {}".format(entity.name))
        
            df = df.append({
                            'post_id': key.post_id,
                            'comment_id': key.comment_id,
                            'entity_name': entity.name,
                            'entity_type': language_v1.Entity.Type(entity.type_).name,
                            'entity_salience': entity.salience,
                            'entity_sentiment_score': sentiment.score,
                            'entity_sentiment_magnitude': sentiment.magnitude,
                            'entity_mention': language_v1.EntityMention.Type(mention.type_).name
                        },
                        ignore_index=True)
    return df.drop_duplicates() 

entities = pd.DataFrame()
entmaster = pd.DataFrame()


for index, comment in comments.iterrows():
    entmaster = entmaster.append(sample_analyze_entity_sentiment(comment, comment['comment_body']))





## Categorize ## 
def classify(text, verbose=True):
    """Classify the input text into categories. """

    language_client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = language_client.classify_text(request={"document": document})
    categories = response.categories

    result = {}

    for category in categories:
        # Turn the categories into a dictionary of the form:
        # {category.name: category.confidence}, so that they can
        # be treated as a sparse vector.
        result[category.name] = category.confidence

    if verbose:
        print(text)
        for category in categories:
            print(u"=" * 20)
            print(u"{:<16}: {}".format("category", category.name))
            print(u"{:<16}: {}".format("confidence", category.confidence))

    return result

comment_cat = pd.DataFrame()
for index, c in comments.iterrows():
    if len(c['comment_body'].split()) < 20:
        continue
    comment_cat = comment_cat.append({
        'id': c['comment_id'],
        'category': classify(c['comment_body'])}
        , ignore_index=True)

comment_cat = comment_cat.assign(category=comment_cat.category.astype(str).str.split(',')).explode('category')
comment_cat['category'] = comment_cat['category'].str.strip('{}')



## write to mysql db ## 
# Credentials
hostname="localhost"
dbname="proddis"
uname="root"
pwd="1234"

engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
				.format(host=hostname, db=dbname, user=uname, pw=pwd))

comments.to_sql('comments', engine, index=False)
entmaster.to_sql('entities', engine, index=False)
comment_cat.to_sql('comment_categories', engine, index=False)

