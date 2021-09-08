from covid_xray_classification.models.xception import Small
from covid_xray_classification.data import Downloader, Reshaper
from pandas import read_csv
from os.path import join
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing import image_dataset_from_directory


Downloader().download()

Reshaper().reshape()

columns = ['patientid',
           'filename',
           'classification',
           'datasource']
input_folder_prefix = 'dataset'
batch_size = 32
image_size = (128,128)
rng_seed = 127001
validation_split = 0.1
epochs = 1
model_name = 'COVID_Chest_X-Ray_BinaryClassification_512x512'


net = Small(image_size=image_size)
model = net.model


callbacks = [EarlyStopping("val_accuracy",
                           patience=5)]


model.compile(optimizer=Adam(1e-3),
              loss="binary_crossentropy",
              metrics=["accuracy"])


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

train_ds = train_dataset.prefetch(buffer_size=32)
val_ds = validation_dataset.prefetch(buffer_size=32)


model.fit(
    train_ds,
    epochs=epochs,
    callbacks=callbacks,
    validation_data=val_ds)

model.save(join('dataset',model_name))



