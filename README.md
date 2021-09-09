# COVID-19 Chest X-Ray Classification
Detect COVID-19 from X-Ray images using Keras.

## Quickstart
```bash
git clone https://github.com/brianlechthaler/covid_xray_classification
cd covid_xray_classification
python -m pip install -r requirements.txt
python setup.py build ; python setup.py install
# Don't forget to have your kaggle.json api key in the right place!
python example.py
```

## Example
Available from `example.py`.
```python
# Import everything we need
from covid_xray_classification.models.xception import Small
from covid_xray_classification.data import Downloader, Reshaper
from pandas import read_csv
from os.path import join
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing import image_dataset_from_directory
from tensorflow.keras.metrics import BinaryAccuracy,Precision,Recall


# Download default dataset to default location
Downloader().download()

# Specify a few runtime variables
columns = ['patientid',
           'filename',
           'classification',
           'datasource']
input_folder_prefix = 'dataset'
reshaped_dataset_folder = 'reshaped'
batch_size = 32
image_size = (256,256)
rng_seed = 127001
validation_split = 0.1
epochs = 50
learning_rate = 1e-3
model_name = 'COVID_Chest_X-Ray_BinaryClassification_128x128'

# Make folders based on labels corresponding to the images the folders contain.
# Here we put both train and test images in the same place, as we will split up the images ourselves later on.
for file_prefix in ['train', 'test']:
    # Extract metadata from the file containing it.
    metadata_table = read_csv(join(input_folder_prefix,
                                   f"{file_prefix}.txt"),
                                   sep=' ')
    # Define custom columns for the data we're importing.
    metadata_table.columns = columns
    # Create a Reshaper to reshape our data according to the parameters we specify
    reshape_task = Reshaper(table=metadata_table,
             input_folder=join(input_folder_prefix,
                               file_prefix),
             output_folder=join(input_folder_prefix,
                                'reshaped'))
    # Reshape our data according to specified parameters.
    reshape_task.reshape()

# Create a small Xception model designed to work with the size of images in our dataset.
net = Small(image_size=image_size)
model = net.model

# Define callbacks.
# Here we use the EarlyStopping callback to stop training if the validation accuracy stops increasing.
# This both saves a significant amount of power and usually decreases the total number of epochs to a fraction of what most will end up specifying
# We also make sure that this callback will automatically pick the best epoch at the end of training.
callbacks = [EarlyStopping("val_precision",
                           patience=10,
                           mode='max',
                           restore_best_weights=True)]

# Specify the metrics we wish to evaluate at the end of each epoch.
metrics = ["accuracy",
           BinaryAccuracy(),
           Precision(name='precision'),
           Recall(name='recall')]

# Compile the model.
# Here we use Adam as our optimizer, and binary_crossentropy as our loss as we are only doing binary classification:
# in other words, if all we need is 0: negative, 1: positive
model.compile(optimizer=Adam(learning_rate),
              loss="binary_crossentropy",
              metrics=metrics)

# Create a training dataset from 90% of the images in the dataset.
train_dataset = image_dataset_from_directory(
    directory=join(input_folder_prefix,
                   'reshaped'),
    labels='inferred',
    label_mode='binary',
    batch_size=batch_size,
    image_size=image_size,
    validation_split=validation_split,
    subset='training',
    seed=rng_seed
)

# Create a validation dataset from 10% of the images in the dataset.
validation_dataset = image_dataset_from_directory(
    directory=join(input_folder_prefix,
                   'reshaped'),
    labels='inferred',
    label_mode='binary',
    batch_size=batch_size,
    image_size=image_size,
    validation_split= validation_split,
    subset='validation',
    seed=rng_seed
)

# Cache our datasets in memory to speed up training
train_ds = train_dataset.prefetch(buffer_size=32)
val_ds = validation_dataset.prefetch(buffer_size=32)

# Train our model.
model.fit(
    train_ds,
    epochs=epochs,
    callbacks=callbacks,
    validation_data=val_ds)

# Save our model for later use.
model.save(join('dataset',model_name))
```