import sys
import numpy as np
from matplotlib import pyplot as plt
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


def xavier_initialization():
    parameters = {}
    limit = np.sqrt(6 / float(train_images.shape[1]))
    parameters['W1'] = np.random.uniform(-limit, limit, size=(128, train_images.shape[0]))
    parameters['B1'] = np.zeros((128, 1))
    limit = np.sqrt(6 / float(128))
    parameters['W2'] = np.random.uniform(-limit, limit, size=(64, 128))
    parameters['B2'] = np.zeros((64, 1))
    limit = np.sqrt(6 / float(64))
    parameters['W3'] = np.random.uniform(-limit, limit, size=(10, 64))
    parameters['B3'] = np.zeros((10, 1))
    return parameters

def relu(Z):
    return np.maximum(Z, 0), Z


def relu_back_prop(Z):
    dZ = np.array(Z, copy=True)
    dZ[Z <= 0] = 0

    return dZ


def softmax(x):
    return np.exp(x - x.max()) / np.sum(np.exp(x - x.max())), x


def softmax_back_prop(x):
    return (np.exp(x - x.max()) / np.sum(np.exp(x - x.max()))) * (
                1 - (np.exp(x - x.max()) / np.sum(np.exp(x - x.max()))))


def forward_prop(A_1, W, B):
    A, Z = relu(W.dot(A_1) + B)
    return A, Z


def forward_prop_softmax(A_1, W, B):
    A, Z = softmax(W.dot(A_1) + B)
    return A, Z


def cross_entropy_loss(y, y_hat):
    assert y.shape == y_hat.shape
    return np.squeeze((1. / y.shape[1]) * np.sum((- np.dot(y, np.log(y_hat).T))))


if __name__ == '__main__':
    cmd_args = sys.argv

    local = True
    if local:
        train_images, train_labels, test_images, test_labels = load_data(cmd_args[1], cmd_args[2], cmd_args[3],
                                                                         local=local)
    else:
        train_images, train_labels, test_images = load_data(cmd_args[1], cmd_args[2], cmd_args[3],
                                                            local=local)

    train_size = 0.85

    full_train = np.append(train_images, train_labels, axis=1)
    full_test = np.append(test_images, test_labels, axis=1)

    full_dataset = np.append(full_train, full_test, axis=0)
    np.random.shuffle(full_dataset)

    train_full = full_dataset[: round((train_images.shape[0] + test_images.shape[0]) * train_size)]
    test_full = full_dataset[round((train_images.shape[0] + test_images.shape[0]) * train_size):]

    train_images = train_full[:, : train_images.shape[1]]
    train_labels = train_full[:, train_images.shape[1]:]

    test_images = test_full[:, : test_images.shape[1]]
    test_labels = test_full[:, test_images.shape[1]:]

    assert train_images.shape[0] == round(train_size * 70000)
    assert train_images.shape[1] == 784
    assert train_labels.shape[0] == round(train_size * 70000)
    assert train_labels.shape[1] == 10

    assert test_images.shape[0] == 70000 - round(train_size * 70000)
    assert test_images.shape[1] == 784
    assert test_labels.shape[0] == 70000 - round(train_size * 70000)
    assert test_labels.shape[1] == 10

    train_images = train_images.T
    train_labels = train_labels.T
    test_images = test_images.T
    test_labels = test_labels.T

    # random_number = random.randint(0, train_images.shape[1])
    # first_image = np.array(train_images[random_number], dtype='float32')
    # pixels = first_image.reshape((28, 28))
    # plt.imshow(pixels, cmap='gray')
    # plt.show()
    # print(train_labels[random_number])
    #
    # random_number = random.randint(0, test_images.shape[1])
    # first_image = np.array(test_images[random_number], dtype='float32')
    # pixels = first_image.reshape((28, 28))
    # plt.imshow(pixels, cmap='gray')
    # plt.show()
    # print(test_labels[random_number])

    parameters = xavier_initialization()

    epochs = 3000
    learning_rate = 0.0075
    for i in range(epochs):
        A1, Z1 = forward_prop(train_images, parameters['W1'], parameters['B1'])
        A2, Z2 = forward_prop(A1, parameters['W2'], parameters['B2'])

        A3, Z3 = forward_prop_softmax(A2, parameters['W3'], parameters['B3'])

        loss = cross_entropy_loss(train_labels, A3)

        dZ3 = (A3 - train_labels)
        dW3 = np.dot(dZ3, A2.T)
        dB3 = np.sum(dZ3, axis=1).reshape(10, 1)

        dZ2 = np.dot(dW3.T, dZ3) * relu_back_prop(Z2)
        dW2 = np.dot(dZ2, A1.T)
        dB2 = np.sum(dZ2, axis=1).reshape(64, 1)

        dZ1 = np.dot(dW2.T, dZ2) * relu_back_prop(Z1)
        dW1 = np.dot(dZ1, train_images.T)
        dB1 = np.sum(dZ1, axis=1).reshape(128, 1)

        parameters['W1'] -= learning_rate * dW1
        parameters['B1'] -= learning_rate * dB1
        parameters['W2'] -= learning_rate * dW2
        parameters['B2'] -= learning_rate * dB2
        parameters['W3'] -= learning_rate * dW3
        parameters['B3'] -= learning_rate * dB3

        if i % 50 == 0:
            print(f'Current loss at epoch {i}th: {loss}')

    A1, Z1 = forward_prop(test_images, parameters['W1'], parameters['B1'])
    A2, Z2 = forward_prop(A1, parameters['W2'], parameters['B2'])

    A3, Z3 = forward_prop_softmax(A2, parameters['W3'], parameters['B3'])

    predictions = np.argmax(A3, axis=0)

    match = 0
    mismatch = np.array([])
    with open('test_predictions_2.csv', 'w') as test_prediction_file:
        writer = csv.writer(test_prediction_file)
        for i in range(predictions.shape[0]):
            writer.writerow(predictions[i])
            if predictions[i] == test_images[i]:
                match += 1
            else:
                mismatch = np.append(mismatch, (i, predictions[i], test_images[i]))

    print(f'Accuracy: {match / test_images.shape[0]}')