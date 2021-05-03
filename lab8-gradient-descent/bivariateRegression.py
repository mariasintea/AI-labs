import csv
from random import sample, shuffle
import numpy as np
import matplotlib.pyplot as plt
from normalisation import normalisation


# reads data from file
def read_data():
    data = []
    data_names = []
    with open("world-happiness-report-2017.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                data_names = row
            else:
                data.append(row)
            line_count += 1
    input_data = [[float(data[i][data_names.index("Economy..GDP.per.Capita.")]), float(data[i][data_names.index("Freedom")])] for i in range(len(data))]
    output_data = [float(data[i][data_names.index("Happiness.Score")]) for i in range(len(data))]
    return input_data, output_data


# split data into train data - 80% and validation data - 20%
def split_data(input_data, output_data):
    indexes = [i for i in range(len(input_data))]
    train_indexes = sample(indexes, int(0.8 * len(input_data)))
    validation_indexes = [i for i in indexes if i not in train_indexes]

    train_inputs = [input_data[i] for i in train_indexes]
    train_outputs = [output_data[i] for i in train_indexes]

    validation_inputs = [input_data[i] for i in validation_indexes]
    validation_outputs = [output_data[i] for i in validation_indexes]

    return train_inputs, train_outputs, validation_inputs, validation_outputs


# calculates error prediction based on Mean Squared Error
def calculate_mse(real_outputs, computed_outputs):
    square_sum = 0.0
    no_samples = len(real_outputs)
    for i in range(no_samples):
        square_sum += (real_outputs[i] - computed_outputs[i]) ** 2
    error = square_sum / no_samples
    return error


# linear regression using batch gradient descent
def gradient_descent(x, y):
    learning_rate = 0.001
    epochs = 3000
    w0 = 0.0
    w1 = 0.0
    w2 = 0.0
    n = len(x)

    for _ in range(epochs):
        coeff_w0 = 0.0
        coeff_w1 = 0.0
        coeff_w2 = 0.0
        for i in range(n):
            y_computed = w0 + w1 * x[i][0] + w2 * x[i][1]
            current_error = y_computed - y[i]
            coeff_w0 += current_error
            coeff_w1 += current_error * x[i][0]
            coeff_w2 += current_error * x[i][1]
        w0 = w0 - learning_rate * coeff_w0/n
        w1 = w1 - learning_rate * coeff_w1/n
        w2 = w2 - learning_rate * coeff_w2/n

        computed_outputs = [w0 + w1 * e[0] + w2 * e[1] for e in x]
        error = calculate_mse(computed_outputs, y)
        print(error)


    return w0, w1, w2


def plot_data(normalised_train_input_data, normalised_train_output_data, w0, w1, w2):
    trainInputs1 = [x[0] for x in normalised_train_input_data]
    trainInputs2 = [x[1] for x in normalised_train_input_data]
    xref = np.linspace(min(trainInputs1), max(trainInputs1), 1000)
    yref = np.linspace(min(trainInputs2), max(trainInputs2), 1000)
    x_surf, y_surf = np.meshgrid(xref, yref)
    zref = []
    for el2 in range(len(yref)):
        for el in range(len(xref)):
            zref.append([w0 + w1 * xref[el] + w2 * yref[el2]])
    z_vals = np.array(zref)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter3D(trainInputs1, trainInputs2, normalised_train_output_data, label='train data')
    ax.plot_surface(x_surf, y_surf, z_vals.reshape(x_surf.shape), color='None', alpha=0.3)
    plt.legend()
    plt.xlabel('gdp capita')
    plt.ylabel('freedom')
    plt.title('train data and model')
    plt.show()


def main():
    input_data, output_data = read_data()
    train_inputs, train_outputs, test_inputs, test_outputs = split_data(input_data, output_data)

    normalised_train_input_data, normalised_train_output_data = normalisation(train_inputs, train_outputs)
    normalised_test_input_data, normalised_test_output_data = normalisation(test_inputs, test_outputs)

    w0, w1, w2 = gradient_descent(normalised_train_input_data, normalised_train_output_data)
    print('the learnt model: f(GDP, Freedom) = ', w0, ' + ', w1, ' * GDP', ' + ', w2, ' * Freedom')

    computed_outputs = [w0 + w1 * x[0] + w2 * x[1] for x in normalised_test_input_data]
    error = calculate_mse(computed_outputs, normalised_test_output_data)
    print('error: ', error)

    #plot_data(normalised_train_input_data, normalised_train_output_data, w0, w1, w2)


if __name__ == '__main__':
    main()
