from tensorflow.keras import layers as __layers__
from tensorflow.keras import Input as __input__
from keras import Sequential as __sequential__
from keras import Model as __model__


class Small:
    """Generate a small Xception network.

    Args:
        input_shape(tuple): Input dimensions. (default (256,256))
        num_classes(int): Positive integer describing the number of classes. (default 2)
        """
    def __init__(self,
                 input_shape=(256, 256),
                 num_classes=2):
        inputs = __input__(shape=input_shape)
        # Image augmentation block
        layers = __sequential__(inputs)

        # Entry block
        layers = __layers__.Rescaling(1.0 / 255)(layers)
        layers = __layers__.Conv2D(32, 3, strides=2, padding="same")(layers)
        layers = __layers__.BatchNormalization()(layers)
        layers = __layers__.Activation("relu")(layers)

        layers = __layers__.Conv2D(64, 3, padding="same")(layers)
        layers = __layers__.BatchNormalization()(layers)
        layers = __layers__.Activation("relu")(layers)

        previous_block_activation = layers  # Set aside residual

        for size in [128, 256, 512, 728]:
            layers = __layers__.Activation("relu")(layers)
            layers = __layers__.SeparableConv2D(size, 3, padding="same")(layers)
            layers = __layers__.BatchNormalization()(layers)

            layers = __layers__.Activation("relu")(layers)
            layers = __layers__.SeparableConv2D(size, 3, padding="same")(layers)
            layers = __layers__.BatchNormalization()(layers)

            layers = __layers__.MaxPooling2D(3, strides=2, padding="same")(layers)

            # Project residual
            residual = __layers__.Conv2D(size, 1, strides=2, padding="same")(
                previous_block_activation
            )
            layers = __layers__.add([layers, residual])  # Add back residual
            previous_block_activation = layers  # Set aside next residual

        layers = __layers__.SeparableConv2D(1024, 3, padding="same")(layers)
        layers = __layers__.BatchNormalization()(layers)
        layers = __layers__.Activation("relu")(layers)

        layers = __layers__.GlobalAveragePooling2D()(layers)
        if num_classes == 2:
            activation = "sigmoid"
            units = 1
        else:
            activation = "softmax"
            units = num_classes

        layers = __layers__.Dropout(0.5)(layers)
        outputs = __layers__.Dense(units, activation=activation)(layers)
        self.model =  __model__(inputs, outputs)
