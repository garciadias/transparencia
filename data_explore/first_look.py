from os import getcwd

import matplotlib.pyplot as plt
import pandas as pd
from pandas_profiling import ProfileReport
import seaborn as sns

CONGRESSPEOPLE = pd.read_csv('%s/data_explore/data/reimbursements.csv' % getcwd(), low_memory=False,
                             encoding='utf_8', error_bad_lines=False, index_col=0)
# ProfileReport(CONGRESSPEOPLE).to_file('%s/reports/reimbursements.html' % (getcwd()))

TOTAL_BY_YEAR = [CONGRESSPEOPLE[CONGRESSPEOPLE.year == year].groupby('congressperson_name')['document_value'].sum()
                 for year in range(2014, 2020)]
TOTAL_BY_YEAR = pd.concat(TOTAL_BY_YEAR, axis=1, sort=True)
TOTAL_BY_YEAR = pd.DataFrame(TOTAL_BY_YEAR.values, columns=range(2014, 2020), index=TOTAL_BY_YEAR.index)

CONGRESSPEOPLE_BY_PARTY = CONGRESSPEOPLE[['congressperson_name', 'party']].drop_duplicates()
CONGRESSPEOPLE_BY_PARTY.set_index('congressperson_name', inplace=True)
TOTAL_BY_YEAR['party'] = CONGRESSPEOPLE_BY_PARTY['party']

MEAN_BY_PARTY = TOTAL_BY_YEAR.groupby('party').mean()[list(range(2014, 2019))].sort_values(2018).mean(axis=1)
STD_BY_PARTY = TOTAL_BY_YEAR.groupby('party').mean()[list(range(2014, 2019))].sort_values(2018).std(axis=1)

PARTY_CODES = [i for i, value in enumerate(MEAN_BY_PARTY.index)]
f = sns.catplot(data=TOTAL_BY_YEAR.groupby('party').mean().sort_values(2018).T, kind="point", size=8)
f.set_xticklabels(rotation=90)
plt.figure(figsize=(16, 9))
plt.errorbar(range(len(MEAN_BY_PARTY)), MEAN_BY_PARTY / 1e3, STD_BY_PARTY / 1e3, marker='', ls='')
plt.scatter(range(len(MEAN_BY_PARTY)), MEAN_BY_PARTY / 1e3, c=PARTY_CODES, cmap=plt.cm.tab20)
plt.xticks(labels=MEAN_BY_PARTY.index.astype(str), ticks=range(len(MEAN_BY_PARTY)), rotation=90)
plt.show()

CONGRESSPEOPLE.cnpj_cpf = CONGRESSPEOPLE.cnpj_cpf.astype('category')
CONGRESSPEOPLE.document_value = CONGRESSPEOPLE.document_value.fillna(0.0)
COMPANIES_BY_PARTY = CONGRESSPEOPLE.groupby(['party', 'supplier'])[['document_value']].sum()
COMPANIES_BY_PARTY.loc['PSL'].sort_values(ascending=False, by='document_value')[:10].plot.bar()
