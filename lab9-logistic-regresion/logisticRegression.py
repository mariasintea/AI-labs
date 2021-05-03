import csv
from math import exp, log2
from random import sample


# reads data from file
def read_data():
    data = []
    data_names = []
    with open("iris.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                data_names = row
            else:
                data.append(row)
            line_count += 1
    input_data = [[float(data[i][data_names.index("sepal.length")]), float(data[i][data_names.index("sepal.width")]), float(data[i][data_names.index("petal.length")]), float(data[i][data_names.index("petal.width")])] for i in range(len(data))]
    output_data = [data[i][data_names.index("variety")] for i in range(len(data))]
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


# min-max normalisation for input data
def normalisation(data):
    normalised_features = []
    for i in range(len(data[0])):
        feature = [elem[i] for elem in data]
        normalised_feature = [(f - min(feature)) / (max(feature) - min(feature)) for f in feature]
        normalised_features.append(normalised_feature)

    normalised_data = []
    for i in range(len(data)):
        normalised_feature = []
        for j in range(len(data[0])):
            normalised_feature.append(normalised_features[j][i])
        normalised_data.append(normalised_feature)

    return normalised_data


# gets classification classes from output data
def get_classes(outputs):
    classes = []
    for output in outputs:
        if classes.count(output) == 0:
            classes.append(output)
    return classes


# maps x into [0, 1]
def sigmoid(x):
    return 1 / (1 + exp(-x))


def calculate_loss_binary_classification(real_probabilities, computed_probabilities):
    loss = 0.0
    for i in range(len(real_probabilities)):
        loss += -(real_probabilities[i] * log2(computed_probabilities[i]) + (1 - real_probabilities[i]) * log2(1 - computed_probabilities[i]))
    return loss / len(real_probabilities)


# linear regression using batch gradient descent
def gradient_descent(x, y):
    epochs = 3000
    learning_rate = 0.0001
    n = len(x)
    w = [0.0] * (len(x[0]) + 1)
    for _ in range(epochs):
        coeff = [0.0] * (len(x[0]) + 1)
        for i in range(n):
            y_computed = w[0]
            for j in range(1, len(x[0]) + 1):
                y_computed += w[j] * x[i][j - 1]
            y_computed = sigmoid(y_computed)
            current_error = y_computed - y[i]
            coeff[0] = current_error
            for j in range(1, len(x[0]) + 1):
                coeff[j] += current_error * x[i][j - 1]
        for i in range(len(x[0]) + 1):
            w[i] = w[i] - learning_rate * coeff[i]

        '''computed = []
        for elem in x:
            computed.append(predict(elem, w))
        error = calculate_loss_binary_classification(y, computed)
        print(error)'''
    return w


# prediction for test input data
def predict(x, w):
    computed_output = w[0]
    for i in range(len(x)):
        computed_output += x[i] * w[i + 1]
    computed_output = sigmoid(computed_output)
    return computed_output


# calculates error for computed results
def calculate_error(real_labels, computed_labels):
    error = 0.0
    for i in range(len(real_labels)):
        error += (real_labels[i] != computed_labels[i])
    return error / len(real_labels)


# one vs all classification
def logistic_regression(normalised_train_inputs, train_outputs, normalised_test_inputs, test_outputs, classes):
    weights = []
    for current_class in classes:
        train_outputs_current_class = [1 if current_class == elem else 0 for elem in train_outputs]
        w = gradient_descent(normalised_train_inputs, train_outputs_current_class)
        weights.append(w)

    labels = []
    for i in range(0, len(normalised_test_inputs)):
        computed_max = 0
        index_max = 0
        for k in range(0, len(classes)):
            computed = predict(normalised_test_inputs[i], weights[k])
            if computed > computed_max:
                computed_max = computed
                index_max = k
        labels.append(classes[index_max])

    return labels


def main():
    input_data, output_data = read_data()
    train_inputs, train_outputs, test_inputs, test_outputs = split_data(input_data, output_data)
    normalised_train_inputs = normalisation(train_inputs)
    normalised_test_inputs = normalisation(test_inputs)

    classes = get_classes(output_data)
    computed_labels = logistic_regression(normalised_train_inputs, train_outputs, normalised_test_inputs, test_outputs, classes)
    print("real classification:", test_outputs)
    print("comp classification:", computed_labels)
    error = calculate_error(test_outputs, computed_labels)
    print("classification error:", error)


if __name__ == '__main__':
    main()
