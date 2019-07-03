"""Download dataset, create pandas profile and combine years."""
from os import getcwd
from pathlib import Path

import pandas as pd
from pandas_profiling import ProfileReport
from serenata_toolbox.chamber_of_deputies.reimbursements import Reimbursements as ChamberDataset


def donload_data(year):
    return ChamberDataset(year, 'data/')


for run_download in map(donload_data, range(2014, 2020)):
    run_download()
DATA_PATH = '%s/data' % getcwd()
Path('%s/reports/' % getcwd()).mkdir(exist_ok=True)

csv_files = list(Path(DATA_PATH).glob('*reimbursements*.csv'))
combined_data = map(lambda filepath: pd.read_csv(filepath, low_memory=False, encoding='utf_8',
                                                 error_bad_lines=False, delimiter=','), csv_files)
combined_data = pd.concat(combined_data)
list(map(lambda filepath: filepath.unlink(), Path(DATA_PATH).glob('*')))
combined_data.to_csv('%s/reimbursements.csv' % DATA_PATH)

ProfileReport(combined_data).to_file('%s/reports/reimbursements.html' % (getcwd()))
