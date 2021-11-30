from bing_images import bing
import pandas as pd 

from sqlalchemy import create_engine
import pymysql


ents = pd.read_csv('unique_entities.csv')

ent_images = pd.DataFrame()
for e in ents['entity_name']:
    ent_images = ent_images.append({
        'entity': e,
        'img_url': bing.fetch_image_urls(e, limit = 1, file_type = 'jpg')
    }, ignore_index=True)

hostname="localhost"
dbname="proddis"
uname="root"
pwd="1234"

engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
				.format(host=hostname, db=dbname, user=uname, pw=pwd))

ent_images.to_csv('ent_images.csv')