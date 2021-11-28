import sys
import numpy as np
from matplotlib import pyplot as plt
import random
import csv


def load_images(address):
    with open(address) as images_file:
        return (np.array(list(csv.reader(images_file)), dtype=np.int32) / 255).astype('float32')


def load_labels(address):
    with open(address) as labels_address:
        labels = np.array(list(csv.reader(labels_address)), dtype=np.int32)
        result = np.zeros((labels.shape[0], 10))
        for index in range(labels.shape[0]):
            result[index][int(labels[index][0])] = 1

    return result


def load_data(train_images_address, train_labels_address, test_images_address):
    train_images = load_images(train_images_address)
    train_labels = load_labels(train_labels_address)
    test_images = load_images(test_images_address)
    return train_images, train_labels, test_images


def test_train_test_split():
    random_number = random.randint(0, train_images.shape[1])
    first_image = np.array(train_images[random_number], dtype='float32')
    pixels = first_image.reshape((28, 28))
    plt.imshow(pixels, cmap='gray')
    plt.show()
    # print(train_labels[random_number])

    random_number = random.randint(0, test_images.shape[1])
    first_image = np.array(test_images[random_number], dtype='float32')
    pixels = first_image.reshape((28, 28))
    plt.imshow(pixels, cmap='gray')
    plt.show()
    # print(test_labels[random_number])


def sigmoid(x):
    return 1 / (1 + np.e ** -x)


def sigmoid_derivative(a):
    return a * (1 - a)


def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)


def cross_entropy_loss(y, y_hat):
    return -np.mean(np.multiply(y, np.log(y_hat + 1e-8)))


def create_weight_matrices():
    parameters = {'W1': np.random.randn(h1_layer_size, input_layer_size) * 1 / np.sqrt(input_layer_size),
                  'W2': np.random.randn(h2_layer_size, h1_layer_size) * 1 / np.sqrt(h1_layer_size),
                  'W3': np.random.randn(output_layer_size, h2_layer_size) * 1 / np.sqrt(h2_layer_size)}
    return parameters


def train(train_image, train_label):
    Z1, A1, Z2, A2, Z3, A3 = forward_prop(train_image)

    dA3 = train_label - A3
    dZ3 = dA3 * sigmoid_derivative(A3)
    dW3 = np.dot(dZ3, A2.T)
    parameters['W3'] += learning_rate * dW3

    dA2 = np.dot(parameters['W3'].T, dA3)
    dZ2 = dA2 * sigmoid_derivative(A2)
    dW2 = np.dot(dZ2, A1.T)
    parameters['W2'] += learning_rate * dW2

    dZ1 = np.dot(parameters['W2'].T, dA2) * sigmoid_derivative(A1)
    dW1 = np.dot(dZ1, train_image.T)
    parameters['W1'] += learning_rate * dW1


def forward_prop(image):
    Z1 = np.dot(parameters['W1'], image)
    A1 = sigmoid(Z1)

    Z2 = np.dot(parameters['W2'], A1)
    A2 = sigmoid(Z2)

    Z3 = np.dot(parameters['W3'], A2)
    A3 = sigmoid(Z3)
    return Z1, A1, Z2, A2, Z3, A3


if __name__ == '__main__':
    cmd_args = sys.argv

    train_images, train_labels, test_images = load_data(cmd_args[1], cmd_args[2], cmd_args[3])

    input_layer_size = 784
    h1_layer_size = 256
    h2_layer_size = 64
    output_layer_size = 10
    learning_rate = 0.1
    epochs = 10

    parameters = create_weight_matrices()

    for epoch in range(epochs):
        for i in range(len(train_images)):
            train(np.array(train_images[i], ndmin=2).T, np.array(train_labels[i], ndmin=2).T)

    predictions = np.array([], dtype=np.int32)

    for i in range(len(test_images)):
        Z1, A1, Z2, A2, Z3, A3 = forward_prop(test_images[i])
        res_max = np.squeeze(A3.argmax(axis=0))
        predictions = np.append(predictions, int(res_max))

    predictions.tofile('test_predictions.csv', sep='\n')
