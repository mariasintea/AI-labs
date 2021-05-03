import csv
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC


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
    np.random.seed(5)
    indexes = [i for i in range(len(input_data))]
    train_indexes = np.random.choice(indexes, int(0.8 * len(input_data)), replace=False)
    validation_indexes = [i for i in indexes if i not in train_indexes]

    train_inputs = [input_data[i] for i in train_indexes]
    train_outputs = [output_data[i] for i in train_indexes]

    validation_inputs = [input_data[i] for i in validation_indexes]
    validation_outputs = [output_data[i] for i in validation_indexes]

    return train_inputs, train_outputs, validation_inputs, validation_outputs


# standard normalisation for input data
def normalisation(train_inputs, test_inputs):
    scaler = StandardScaler()
    scaler.fit(train_inputs)
    normalised_train_inputs = scaler.transform(train_inputs)
    normalised_test_inputs = scaler.transform(test_inputs)
    return normalised_train_inputs, normalised_test_inputs


def main():
    input_data, output_data = read_data()
    train_inputs, train_outputs, test_inputs, test_outputs = split_data(input_data, output_data)
    normalised_train_inputs, normalised_test_inputs = normalisation(train_inputs, test_inputs)

    classifier = OneVsRestClassifier(LinearSVC(random_state=0))
    classifier.fit(normalised_train_inputs, train_outputs)

    computed_outputs = classifier.predict(normalised_test_inputs)
    error = 1 - accuracy_score(computed_outputs, test_outputs)
    print('classification error: ', error)


if __name__ == '__main__':
    main()
