from covid_xray_classification.cmd import Runner as __runner__
from pandas import DataFrame as __df__
from os import pathsep as __pthsep__


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
                if column[self.column_classification] not in self.created_directories:
                    # Formulate command to make the directory we need.
                    mkdir = __runner__(['mkdir',
                                        '-p', f"{self.output_folder}{__pthsep__}{column[self.column_classification]}"])
                    # Run the command to make the directory we need.
                    mkdir.run()
                    # Append the created directory's name to a list to prevent running mkdir when not necessary.
                    self.created_directories.append(column[self.column_classification])

                # Formulate command to move the file where it needs to go.
                mv = __runner__(['mv',
                                 f"{self.input_folder}{__pthsep__}{column[self.column_classification]}{__pthsep__}{column[self.column_filename]}",
                                 f"{self.output_folder}{__pthsep__}{column[self.column_classification]}{__pthsep__}{column[self.column_filename]}"])
                # Run the command to move the file where it needs to go.
                mv.run()
            else:
                # Raise an exception if critical column values are missing.
                raise Exception("Row does not contain necessary columns.")
