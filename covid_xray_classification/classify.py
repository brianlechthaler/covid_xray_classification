from tensorflow.keras.preprocessing.image import load_img as __load_img__
from keras.preprocessing.image import img_to_array as __img2ary__
from tensorflow import expand_dims as __expdim__
from tensorflow.keras import Model as __model__


class Classifier:
    """Classify an image at a given path resized down to the specified target_size.

    Args:
        model(tensorflow.keras.Model): A keras model to classify the image with. (default tensorflow.keras.Model)
        image(str): Path to the image we wish to classify. (default '')
        target_size(tuple): 2-dimensional tuple describing the dimensions we wish to resize the specified image to. (default (256,256))"""
    def __init__(self,
                 model=__model__,
                 image='',
                 target_size=(256,256)):

        # Classify the specified image using the specified model, return prediction.
        self.predictions = model.predict(
            # Expand the array's dimensions.
            __expdim__(
                # Convert the image to an array.
                __img2ary__(
                    # Load image from specified path.
                    __load_img__(
                        image,
                        # Use target size from keyword parameter.
                        target_size=target_size))))

        self.score = self.predictions[0]