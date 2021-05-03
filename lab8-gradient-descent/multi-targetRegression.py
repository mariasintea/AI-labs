from random import sample
import sklearn.datasets
from normalisation import z_normalisation


# gets linnerud dataset from sklearn datasets
def read_data():
    data = sklearn.datasets.load_linnerud()
    x = data['data']
    y = data['target']
    return x, y


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


# normalisation for given features
def normalisation(data):
    normalised_features = []
    for i in range(len(data[0])):
        feature = [elem[i] for elem in data]
        normalised_feature = z_normalisation(feature)
        normalised_features.append(normalised_feature)

    normalised_data = []
    for i in range(len(data)):
        normalised_feature = []
        for j in range(len(data[0])):
            normalised_feature.append(normalised_features[j][i])
        normalised_data.append(normalised_feature)

    return normalised_data


# linear regression using batch gradient descent
def gradient_descent(x, y):
    epochs = 3000
    learning_rate = 0.001
    m = len(x[0])
    n = len(x)
    w = [[0.0] * (len(x[0]) + 1) for _ in range(len(y[0]))]
    for _ in range(epochs):
        for out_nr in range(len(y[0])):
            coeff = [0.0] * (len(x[0]) + 1)
            for i in range(n):
                y_computed = w[out_nr][0]
                for j in range(1, len(x[0]) + 1):
                    y_computed += w[out_nr][j] * x[i][j - 1]
                current_error = y_computed - y[i][out_nr]
                coeff[0] = current_error
                for j in range(1, len(x[0]) + 1):
                    coeff[j] += current_error * x[i][j - 1]
            for i in range(len(x[0]) + 1):
                w[out_nr][i] = w[out_nr][i] - learning_rate * coeff[i] / n

        computed_outputs = predict(x, w)
        print(calculate_error(computed_outputs, y))

    return w


# prediction for test input data
def predict(x, w):
    computed_outputs = [[0.0] * len(w) for _ in range(len(x))]
    for i in range(len(w)):
        for j in range(len(x)):
            computed_outputs[j][i] = w[i][0]
            for k in range(len(x[0])):
                computed_outputs[j][i] += x[j][k] * w[i][k + 1]
    return computed_outputs


# Mean Square Error
def calculate_mse(real_outputs, computed_outputs, k=0):
    square_sum = 0.0
    no_samples = len(real_outputs)
    for i in range(no_samples):
        square_sum += (real_outputs[i][k] - computed_outputs[i][k]) ** 2
    error = square_sum / no_samples
    return error


# calculates overall error
def calculate_error(real_outputs, computed_outputs):
    sum = 0.0
    no_targets = len(real_outputs[0])
    for i in range(no_targets):
        sum += calculate_mse(real_outputs, computed_outputs, i)
    return sum/no_targets


def main():
    input_data, output_data = read_data()
    train_inputs, train_outputs, test_inputs, test_outputs = split_data(input_data, output_data)
    normalised_train_inputs = normalisation(train_inputs)
    normalised_train_outputs = normalisation(train_outputs)
    normalised_test_inputs = normalisation(test_inputs)
    normalised_test_outputs = normalisation(test_outputs)

    w = gradient_descent(normalised_train_inputs, normalised_train_outputs)
    for i in range(len(w)):
        line = "feature " + str(i+1) + ": f(x1"
        for j in range(2, len(w[0])):
            line += ", x" + str(j)
        line += ") = " + str(w[i][0])
        for j in range(1, len(w[0])):
            line += " + x" + str(j) + " * " + str(w[i][j])
        print(line)
    computed_outputs = predict(normalised_test_inputs, w)
    print("error:", calculate_error(normalised_test_outputs, computed_outputs))


if __name__ == '__main__':
    main()
