from subprocess import run as __run__
from pandas import DataFrame as __df__
from os.path import join as __join__


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
        __run__(['mkdir', '-p', save_to], check=True)  # Specify the path of the directory we wish to create.

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
        __run__(dataset_download_command, check=True)  # Specify the directory to which we wish to download our dataset of choice.


class Reshaper:
    """Turn a folder full of images and a DataFrame containing filenames and their corresponding classification into directories named after their content's classification.

    Args:
        table(pandas.DataFrame): Pandas DataFrame containing filenames and their corresponding classification. (default pandas.DataFrame())
        input_folder(str): Folder containing unsorted images. (default 'dataset')
        output_folder(str): Folder to contain the reshaped dataset. (default 'reshaped_dataset')
        column_filename(str): Column containing file names. (default 'filename')
        column_classification(str): Column containing a filename's corresponding classification. (default 'classification')"""
    def __init__(self,
                 table=__df__(),
                 input_folder='dataset',
                 output_folder='reshaped_dataset',
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
        self.output_folder = output_folder
        del output_folder

        # Create a variable to keep track of created directories.
        self.created_directories = []

    def reshape(self):
        """Reshape dataset according to params specified at instantiation. Takes no arguments, returns nothing."""
        # Loop over each row in our DataFrame.
        for index, column in self.table.iterrows():
            # Check if the columns we need exist in this row.
            if column[self.column_filename] and column[self.column_classification]:
                # Check if we need to create a directory that we're about to move something to.
                # Formulate command to make the directory we need.
                __run__(['mkdir',
                         '-p', __join__(self.output_folder,
                                        column[self.column_classification])],
                         check=True)  # Append the created directory's name to a list to prevent running mkdir when not necessary.

                # Formulate command to move the file where it needs to go.
                __run__(['mv',
                         __join__(self.input_folder,
                                  column[self.column_filename]),
                         __join__(self.output_folder,
                                  column[self.column_classification],
                                  column[self.column_filename]),],
                        check=True)
            else:
                # Raise an exception if critical column values are missing.
                raise Exception("Row does not contain necessary columns.")
