import os
import json

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd
import keras

from keras import layers
from keras import models
from keras.models import load_model
from tensorflow.keras import optimizers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from tensorflow.keras.utils import load_img, img_to_array, array_to_img
from IPython.display import Image, display
import matplotlib.pyplot as plt
import matplotlib.cm as cm


import cv2


def show_accuracies(histories):
    for history in histories:
        acc = history.history['accuracy']
        val_acc = history.history['val_accuracy']
        loss = history.history['loss']
        val_loss = history.history['val_loss']
        print("Accuracy: ", np.mean(acc), "Validation Accuracy: ", np.mean(val_acc), "\n",
              "Loss: ", np.mean(loss), "Validation Loss: ",np.mean(val_loss), "\n")

def show_stats(histories):
    for history in histories: 
        acc_max = max(history.history['accuracy'])
        acc_mean = np.mean(history.history['accuracy'])
        val_acc_max = max(history.history['val_accuracy'])
        val_acc_mean = np.mean(history.history['val_accuracy'])
        loss_min = min(history.history['loss'])
        loss_mean = np.mean(history.history['loss'])
        val_loss_min = min(history.history['val_loss'])
        val_loss_mean = np.mean(history.history['val_loss'])
        print("Max Accuracy: ", acc_max," Mean Accuracy: ",acc_mean," Max Val Accuracy: ",val_acc_max," Mean Val Accuracy",val_acc_mean)
        print("Min Loss: ",loss_min," Mean loss: ",loss_mean, "Min Val Loss: ",val_loss_min," Mean Val Loss: ",val_loss_mean)


def plot_graphs(history, smooth = False, metric = 'accuracy', validation_metric = 'val_accuracy'):
    
    def smooth_curve(points, factor=0.8):
        smoothed_points = []
        for point in points:
            if smoothed_points:
                previous = smoothed_points[-1]
                smoothed_points.append(previous * factor + point * (1 - factor))
            else:
                smoothed_points.append(point)
        return smoothed_points
   
    acc = smooth_curve(history[metric]) if smooth else history[metric]
    val_acc = smooth_curve(history[validation_metric]) if smooth else history[validation_metric]
    loss = smooth_curve(history['loss']) if smooth else history['loss']
    val_loss = smooth_curve(history['val_loss']) if smooth else history['val_loss']
    epochs = range(1, len(acc) + 1)

    plt.plot(epochs, acc, 'bo', label='Training acc')
    plt.plot(epochs, val_acc, 'b', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.legend()
    
    plt.figure()
    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.legend()
    plt.show()
    
def save_dict_as_json(data, file_name):
    with open(file_name + ".json", "w") as fp:
        json.dump(data,fp, indent = 4) 

def load_image(img_path, show=False):

    img = image.load_img(img_path, target_size=(224, 224))
    img_tensor = image.img_to_array(img)                    # (height, width, channels)
    img_tensor = np.expand_dims(img_tensor, axis=0)         # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
    img_tensor /= 255
    
    if show:
        plt.imshow(img_tensor[0])                           
        plt.axis('off')
        plt.show()

    return img_tensor

def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    # First, we create a model that maps the input image to the activations
    # of the last conv layer as well as the output predictions
    grad_model = tf.keras.models.Model(
        [model.inputs], [model.get_layer(last_conv_layer_name).output, model.output]
    )

    # Then, we compute the gradient of the top predicted class for our input image
    # with respect to the activations of the last conv layer
    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    # This is the gradient of the output neuron (top predicted or chosen)
    # with regard to the output feature map of the last conv layer
    grads = tape.gradient(class_channel, last_conv_layer_output)

    # This is a vector where each entry is the mean intensity of the gradient
    # over a specific feature map channel
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # We multiply each channel in the feature map array
    # by "how important this channel is" with regard to the top predicted class
    # then sum all the channels to obtain the heatmap class activation
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    # For visualization purpose, we will also normalize the heatmap between 0 & 1
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()


def save_and_display_gradcam(img_path, heatmap, cam_path="cam.jpg", alpha=0.4):
    # Load the original image
    img = load_img(img_path)
    img = img_to_array(img)

    # Rescale heatmap to a range 0-255
    heatmap = np.uint8(255 * heatmap)

    # Use jet colormap to colorize heatmap
    jet = cm.get_cmap("jet")

    # Use RGB values of the colormap
    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[heatmap]

    # Create an image with RGB colorized heatmap
    jet_heatmap = array_to_img(jet_heatmap)
    jet_heatmap = jet_heatmap.resize((img.shape[1], img.shape[0]))
    jet_heatmap = img_to_array(jet_heatmap)

    # Superimpose the heatmap on original image
    superimposed_img = jet_heatmap * alpha + img
    superimposed_img = array_to_img(superimposed_img)

    # Save the superimposed image
    superimposed_img.save(cam_path)

def save_and_show_heatmap(img_src_path, img_dst_path, model, last_conv_layer_name):
    # Prepare image
    img_array = load_image(img_src_path)

    # Remove last layer's softmax
    model.layers[-1].activation = None

    # Print what the top predicted class is
    preds = model.predict(img_array)
    print("Predicted:", preds)

    # Generate class activation heatmap
    heatmap = make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index = 1)
    
    # Show joined heatmap and image
    save_and_display_gradcam(img_src_path, heatmap, img_dst_path)
    
    # Display Grad CAM
    
    display(Image(img_src_path))
    plt.matshow(heatmap)
    plt.show()
    display(Image(img_dst_path))


def model_accuracy(filename):
    with open(filename + ".json", "r") as fp:
        r = json.load(fp)
        return(r["val_accuracy"][-1])