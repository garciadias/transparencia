"""Create the base lektor content files for all parties."""
from os import getcwd
from pathlib import Path

import pandas as pd

from data_explore.src.content_base import content_base

parties_color = pd.read_csv('%s/data_explore/data/parties_color.csv' % getcwd(), index_col=0)
parties_content_path = '%s/parlamentar/content/parties/' % getcwd()

for party, (color, title) in parties_color.iterrows():
    party_path = '%s%s' % (parties_content_path, party)
    Path(party_path).mkdir(exist_ok=True)
    with open('%s/contents.lr' % party_path, 'w') as contents_file:
        contents_file.write(content_base % (party, party, color, title, '\n #actual content'))
