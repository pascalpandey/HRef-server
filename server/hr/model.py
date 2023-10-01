import numpy as np
import tensorflow as tf

n_components = 1201

class score_predictor(tf.keras.Model):
    def __init__(self, n_components):
        super().__init__()
        # self.input_layer= tf.keras.layers.Input(shape=(n_components,))
        # self.model_layers = tf.keras.Sequential([
        #     tf.keras.layer.Input(shape=(n_components,)),
        #     tf.keras.layers.Dense(64, activation="relu", kernel_regularizer = tf.keras.regularizers.l2(3e-4)),
        #     tf.keras.layers.Dense(32, activation="relu", kernel_regularizer = tf.keras.regularizers.l2(3e-4)),
        #     tf.keras.layers.Dense(32, activation="relu", kernel_regularizer = tf.keras.regularizers.l2(3e-4)),
        #     tf.keras.layers.Dense(32, activation="relu", kernel_regularizer = tf.keras.regularizers.l2(3e-4)),
        #     tf.keras.layers.Dense(1, activation="relu")
        # ])
        self.dense64 = tf.keras.layers.Dense(64, activation="relu", kernel_regularizer = tf.keras.regularizers.l2(3e-4))
        self.dense32 = tf.keras.layers.Dense(32, activation="relu", kernel_regularizer = tf.keras.regularizers.l2(3e-4))
        self.output_layer = tf.keras.layers.Dense(1, activation="relu")
        
    def call(self, inputs, training=False):
        x = self.dense64(inputs)
        for i in range(3):
            x = self.dense32(x)
        x = self.output_layer(x)
        return x
        
        