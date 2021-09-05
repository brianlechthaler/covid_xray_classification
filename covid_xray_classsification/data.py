from pandas import read_csv as __readcsv__
from covid_xray_classsification.cmd import Runner as __runner__
from pandas import DataFrame as __df__


class Downloader:
    """Wrapper of kaggle-api client intended to be used to download a dataset.

    Args:
        dataset(str): Specify a dataset to download from kaggle with user/dataset formatting. (default 'andyczhao/covidx-cxr2')"""
    def __init__(self,
                 dataset='andyczhao/covidx-cxr2'):
        # Move values specified at class instantiation to self, making sure to remove param vars to reduce memory usage.
        self.dataset = dataset
        del dataset

    def download(self,
                 save_to='dataset',
                 unzip=True):
        """
        Download dataset to specified location, creating the specified location should it not exist at time of function invocation.

        Args:
             save_to(str): Path to save dataset to. (default 'dataset')
             unzip(bool): Whether or not to unzip the dataset after downloading it. (default True)
        """
        # ---- Part 1/2: Setup ----
        # Create our directory in case it does not exist yet.
        create_directory = __runner__(command=['mkdir',
                                               '-p', save_to]) # Specify the path of the directory we wish to create.

        # Form command to download dataset
        dataset_download_command = [
            'kaggle', 'datasets', 'download',   # Specify the base command.
            '-d', self.dataset, # Specify dataset we wish to download.
            '-p', save_to]

        # Check if we need to unzip the dataset after download.
        if unzip is True:
            # Specify the --unzip flag for kaggle to unzip dataset after download.
            dataset_download_command.append('--unzip')

        # Download dataset to specified path.
        download_dataset = __runner__(command=dataset_download_command)  # Specify the directory to which we wish to download our dataset of choice.

        # ---- Part 2/2: Runtime ----
        # Run the command to create a directory in case we need to.
        create_directory.run()

        # Run the command to download our dataset, optionally unzipping it.
        download_dataset.run()


class Reshape:
    """Turn a folder full of images and a DataFrame containing filenames and their corresponding classification into directories named after their content's classification.

    Args:
        table(pandas.DataFrame): Pandas DataFrame containing filenames and their corresponding classification. (default pandas.DataFrame())
        input_folder(str): Folder containing unsorted images. (default 'dataset')
        column_filename(str): Column containing file names. (default 'filename')
        column_classification(str): Column containing a filename's corresponding classification. (default 'classification')"""
    def __init__(self,
                 table=__df__(),
                 input_folder='dataset',
                 column_filename='filename',
                 column_classification='classification'):
        # Move values specified at class instantiation to self, making sure to remove param vars to reduce memory usage.
        self.table = table
        del table
        self.input_folder = input_folder
        del input_folder
        self.column_filename = column_filename
        del column_filename
        self.column_classification = column_classification
        del column_classification
