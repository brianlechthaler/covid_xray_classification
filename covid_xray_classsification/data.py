from subprocess import run as __run__
from pandas import read_csv as __readcsv__


class Downloader:
    """Wrapper of kaggle-api client intended to be used to download a dataset.

    Args:
        dataset(str): Specify a dataset to download from kaggle with user/dataset formatting. (default 'andyczhao/covidx-cxr2')"""
    def __init__(self,
                 dataset='andyczhao/covidx-cxr2'):
        self.dataset_id = dataset
