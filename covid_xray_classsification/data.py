from pandas import read_csv as __readcsv__
from covid_xray_classsification.cmd import Runner as __runner__


class Downloader:
    """Wrapper of kaggle-api client intended to be used to download a dataset.

    Args:
        dataset(str): Specify a dataset to download from kaggle with user/dataset formatting. (default 'andyczhao/covidx-cxr2')"""
    def __init__(self,
                 dataset='andyczhao/covidx-cxr2'):
        self.dataset_id = dataset
    def download(self, saveTo='dataset'):
        """
        Download dataset to specified location, creating the specified location should it not exist at time of function invocation.

        Args:
             saveTo(str): Path to save dataset to.
        """
        # Create our directory in case it does not exist yet.
        __runner__(command=['mkdir',
                            '-p', saveTo]) # Specify the path of the directory we wish to create.
        # Download dataset to specified path.
        __runner__(command=['kaggle', 'datasets', 'download',
                            '-d', self.dataset,  # Specify dataset we wish to download.
                            '-p', saveTo])  # Specify the directory to which we wish to download our dataset of choice.
