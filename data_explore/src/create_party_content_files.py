"""Create the base lektor content files for all parties."""
from os import getcwd
from pathlib import Path

import pandas as pd

from data_explore.src.content_base import content_base


def write_content_file(party, color, title, companies, values, content):
    with open('%s/contents.lr' % party_path, 'w') as contents_file:
        contents_file.write(content_base % (party, party, color, title, companies, values, content))


def create_data_by_party_parties():
    CONGRESSPEOPLE = pd.read_csv('%s/data_explore/data/reimbursements.csv' % getcwd(), low_memory=False,
                                 encoding='utf_8', error_bad_lines=False, index_col=0)
    CONGRESSPEOPLE.cnpj_cpf = CONGRESSPEOPLE.cnpj_cpf.astype('category')
    CONGRESSPEOPLE.document_value = CONGRESSPEOPLE.document_value.fillna(0.0)
    COMPANIES_BY_PARTY = CONGRESSPEOPLE.groupby(['party', 'supplier'])[['document_value']].sum() / 1e6
    COMPANIES_BY_PARTY.to_csv('%s/data_explore/data/companies_by_party.csv' % getcwd())
    return None


def get_top_n_companies_by_party(party, n_values=10):
    return COMPANIES_BY_PARTY.loc[party].sort_values('document_value', ascending=False).head(10)


if __name__ == '__main__':
    PARTIES_COLOR = pd.read_csv('%s/data_explore/data/parties_color.csv' % getcwd(), index_col=0)
    PARTIES_CONTENT_PATH = '%s/parlamentar/content/parties/' % getcwd()
    if not Path('%s/data_explore/data/companies_by_party.csv' % getcwd()).exists():
        create_data_by_party_parties()
    else:
        COMPANIES_BY_PARTY = pd.read_csv('%s/data_explore/data/companies_by_party.csv' % getcwd(), index_col=0)

    VALID_PARTIES = COMPANIES_BY_PARTY.index.unique()[COMPANIES_BY_PARTY.index.unique().isin(PARTIES_COLOR.index)]
    content = 'test'
    for party, (color, title) in PARTIES_COLOR.loc[VALID_PARTIES].iterrows():
        party_path = '%s%s' % (PARTIES_CONTENT_PATH, party)
        Path(party_path).mkdir(exist_ok=True)
        top_companies = get_top_n_companies_by_party(party)
        suppliers, document_values = top_companies['supplier'], top_companies['document_value']
        suppliers = '\", \"'.join(suppliers.values)
        document_values = ', '.join(document_values.values.round(2).astype('str'))
        write_content_file(party, color, title, suppliers, document_values, content)
