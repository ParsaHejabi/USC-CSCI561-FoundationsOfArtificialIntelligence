import sys
import numpy as np
from matplotlib import pyplot as plt
import random
import csv

TEST_LABELS_ADDRESS = 'H:\\My Drive\\UniversityOfSouthernCalifornia\\Term1\\CSCI561' \
                      '-FoundationsofArtificialIntelligence\\Homeworks\\HW3\\resource\\asnlib\\public\\test_label' \
                      '.csv'


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


def load_data(train_images_address, train_labels_address, test_images_address, local=False):
    train_images = load_images(train_images_address)
    train_labels = load_labels(train_labels_address)
    test_images = load_images(test_images_address)
    if local:
        test_labels = load_labels(TEST_LABELS_ADDRESS)
        return train_images, train_labels, test_images, test_labels
    else:
        return train_images, train_labels, test_images


def test_train_test_split():
    random_number = random.randint(0, train_images.shape[1])
    first_image = np.array(train_images[random_number], dtype='float32')
    pixels = first_image.reshape((28, 28))
    plt.imshow(pixels, cmap='gray')
    plt.show()
    print(train_labels[random_number])

    random_number = random.randint(0, test_images.shape[1])
    first_image = np.array(test_images[random_number], dtype='float32')
    pixels = first_image.reshape((28, 28))
    plt.imshow(pixels, cmap='gray')
    plt.show()
    print(test_labels[random_number])


def xavier_initialization():
    params = {'W1': np.random.randn(784, 128) / np.sqrt(784), 'B1': np.zeros((1, 128)),
              'W2': np.random.randn(128, 64) / np.sqrt(64), 'B2': np.zeros((1, 64)),
              'W3': np.random.randn(64, 10) / np.sqrt(64), 'B3': np.zeros((1, 10))}
    return params


def sigmoid(Z):
    return 1 / (1 + np.exp(-Z))


def sigmoid_back_prop(Z):
    sig = sigmoid(Z)
    return sig * (1 - sig)


def softmax(x):
    return np.exp(x - x.max()) / np.sum(np.exp(x - x.max()), axis=1, keepdims=True)


def forward_prop(A_1, W, B):
    Z = A_1.dot(W) + B
    A = sigmoid(Z)
    return A, Z


def forward_prop_softmax(A_1, W, B):
    Z = A_1.dot(W) + B
    A = softmax(Z)
    return A, Z


def cross_entropy_loss(y, y_hat):
    return -np.mean(y * np.log(y_hat + 1e-8))


if __name__ == '__main__':
    cmd_args = sys.argv

    local = True
    if local:
        train_images, train_labels, test_images, test_labels = load_data(cmd_args[1], cmd_args[2], cmd_args[3],
                                                                         local=local)
    else:
        train_images, train_labels, test_images = load_data(cmd_args[1], cmd_args[2], cmd_args[3],
                                                            local=local)

    # train_size = 0.85
    #
    # full_train = np.append(train_images, train_labels, axis=1)
    # full_test = np.append(test_images, test_labels, axis=1)
    #
    # full_dataset = np.append(full_train, full_test, axis=0)
    # np.random.shuffle(full_dataset)
    #
    # train_full = full_dataset[: round((train_images.shape[0] + test_images.shape[0]) * train_size)]
    # test_full = full_dataset[round((train_images.shape[0] + test_images.shape[0]) * train_size):]
    #
    # train_images = train_full[:, : train_images.shape[1]]
    # train_labels = train_full[:, train_images.shape[1]:]
    #
    # test_images = test_full[:, : test_images.shape[1]]
    # test_labels = test_full[:, test_images.shape[1]:]
    #
    # assert train_images.shape[0] == round(train_size * 70000)
    # assert train_images.shape[1] == 784
    # assert train_labels.shape[0] == round(train_size * 70000)
    # assert train_labels.shape[1] == 10
    #
    # assert test_images.shape[0] == 70000 - round(train_size * 70000)
    # assert test_images.shape[1] == 784
    # assert test_labels.shape[0] == 70000 - round(train_size * 70000)
    # assert test_labels.shape[1] == 10

    # test_train_test_split()

    parameters = xavier_initialization()

    epochs = 50
    learning_rate = 0.01
    for i in range(epochs):
        A1, Z1 = forward_prop(train_images, parameters['W1'], parameters['B1'])
        A2, Z2 = forward_prop(A1, parameters['W2'], parameters['B2'])
        A3, Z3 = forward_prop_softmax(A2, parameters['W3'], parameters['B3'])

        # print(A1.shape)
        # print(A2.shape)
        # print(A3.shape)

        loss = cross_entropy_loss(train_labels, A3)
        # -----------------------------------------------

        dZ3 = (A3 - train_labels)
        dW3 = np.matmul(dZ3.T, A2) / train_images.shape[0]
        dW3 = dW3.T
        dB3 = np.sum(dZ3, axis=0, keepdims=True) / train_images.shape[0]

        # print(dZ3.shape)
        # print(dW3.shape)
        # print(dB3.shape)

        dZ2 = np.matmul(dW3, dZ3.T).T * sigmoid_back_prop(Z2)
        dW2 = np.matmul(dZ2.T, A1) / train_images.shape[0]
        dW2 = dW2.T
        dB2 = np.sum(dZ2, axis=0, keepdims=True) / train_images.shape[0]

        # print(dZ2.shape)
        # print(dW2.shape)
        # print(dB2.shape)

        dZ1 = np.matmul(dW2, dZ2.T).T * sigmoid_back_prop(Z1)
        dW1 = np.matmul(dZ1.T, train_images) / train_images.shape[0]
        dW1 = dW1.T
        dB1 = np.sum(dZ1, axis=0, keepdims=True) / train_images.shape[0]

        # print(dZ1.shape)
        # print(dW1.shape)
        # print(dB1.shape)

        parameters['W1'] = parameters['W1'] - learning_rate * dW1
        parameters['B1'] = parameters['B1'] - learning_rate * dB1
        parameters['W2'] = parameters['W2'] - learning_rate * dW2
        parameters['B2'] = parameters['B2'] - learning_rate * dB2
        parameters['W3'] = parameters['W3'] - learning_rate * dW3
        parameters['B3'] = parameters['B3'] - learning_rate * dB3
        #
        # print(f'DW3: {dW3}')
        # print(f'DW2: {dW2}')
        # print(f'DW1: {dW1}')

        if i % 50 == 0:
            print(f'Current loss at epoch {i}th: {loss}')

    A1, Z1 = forward_prop(test_images, parameters['W1'], parameters['B1'])
    A2, Z2 = forward_prop(A1, parameters['W2'], parameters['B2'])
    A3, Z3 = forward_prop_softmax(A2, parameters['W3'], parameters['B3'])

    predictions = np.argmax(A3, axis=1)
    print(f'Accuracy: {np.mean(predictions == np.argmax(test_labels, axis=1))}')

    mismatch = np.array([])
    with open('test_predictions_2.csv', 'w') as test_prediction_file:
        writer = csv.writer(test_prediction_file)
        writer.writerow(predictions)

    # for i in range(predictions.shape[0]):
    #     if predictions[i] != test_images[i]:
    #         mismatch = np.append(mismatch, (i, predictions[i], test_images[i]))
