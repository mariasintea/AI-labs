import csv
import random
import numpy as np
from normalisation import normalisation
from sklearn.metrics import mean_squared_error
from sklearn import linear_model


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
    np.random.seed(5)
    indexes = [i for i in range(len(input_data))]
    train_indexes = np.random.choice(indexes, int(0.8 * len(input_data)), replace=False)
    validation_indexes = [i for i in indexes if i not in train_indexes]

    train_inputs = [input_data[i] for i in train_indexes]
    train_outputs = [output_data[i] for i in train_indexes]

    validation_inputs = [input_data[i] for i in validation_indexes]
    validation_outputs = [output_data[i] for i in validation_indexes]

    return train_inputs, train_outputs, validation_inputs, validation_outputs


def main():
    input_data, output_data = read_data()
    train_inputs, train_outputs, test_inputs, test_outputs = split_data(input_data, output_data)

    normalised_train_input_data, normalised_train_output_data = normalisation(train_inputs, train_outputs)
    normalised_test_input_data, normalised_test_output_data = normalisation(test_inputs, test_outputs)

    regressor = linear_model.SGDRegressor(learning_rate='constant', alpha=0.01, shuffle=True)
    epochs = 1000
    for _ in range(epochs):
        random.shuffle(normalised_train_input_data)
        regressor.partial_fit(normalised_train_input_data, normalised_train_output_data)
    w0, w1, w2 = regressor.intercept_[0], regressor.coef_[0], regressor.coef_[1]
    print('the learnt model: f(GDP, Freedom) = ', w0, ' + ', w1, ' * GDP', ' + ', w2, ' * Freedom')

    computed_outputs = regressor.predict(normalised_test_input_data)
    error = mean_squared_error(computed_outputs, normalised_test_output_data)
    print('error: ', error)


if __name__ == '__main__':
    main()
