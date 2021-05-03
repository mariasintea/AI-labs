from math import sqrt, log2


# reads data for multi-target regression
def read_regression():
    try:
        f = open("regression.txt", "r")
    except IOError:
        print("File reading error!")
        return []
    no_targets = int(f.readline().strip().split()[0])
    no_samples = int(f.readline().strip().split()[0])
    real_outputs = []
    for _ in range(no_samples):
        line = f.readline().strip().split(",")
        real_outputs_line = []
        for elem in line:
            real_outputs_line.append(float(elem))
        real_outputs.append(real_outputs_line)

    computed_outputs = []
    for _ in range(no_samples):
        line = f.readline().strip().split(",")
        computed_outputs_line = []
        for elem in line:
            computed_outputs_line.append(float(elem))
        computed_outputs.append(computed_outputs_line)

    f.close()
    return no_targets, real_outputs, computed_outputs


# reads data for multi-class classification
def read_classification():
    try:
        f = open("classification.txt", "r")
    except IOError:
        print("File reading error!")
        return []
    no_labels = int(f.readline().strip().split()[0])
    labels = []
    line = f.readline().strip().split(",")
    for elem in line:
        labels.append(elem)
    no_samples = int(f.readline().strip().split()[0])

    real_labels = []
    line = f.readline().strip().split(",")
    for elem in line:
        real_labels.append(elem)

    computed_labels = []
    line = f.readline().strip().split(",")
    for elem in line:
        computed_labels.append(elem)

    f.close()
    return no_labels, labels, real_labels, computed_labels


# reads data for binary classification with probabilities
def read_probabilities():
    try:
        f = open("binary.txt", "r")
    except IOError:
        print("File reading error!")
        return []
    no_samples = int(f.readline().strip().split()[0])
    real_probabilities = []
    for _ in range(no_samples):
        line = f.readline().strip().split(",")
        real_probabilities_line = []
        for elem in line:
            real_probabilities_line.append(float(elem))
        real_probabilities.append(real_probabilities_line)
    computed_probabilities = []
    for _ in range(no_samples):
        line = f.readline().strip().split(",")
        computed_probabilities_line = []
        for elem in line:
            computed_probabilities_line.append(float(elem))
        computed_probabilities.append(computed_probabilities_line)

    f.close()
    return real_probabilities, computed_probabilities


# maps the labels into an array: 1 - label exists in sample line, 0 - otherwise
def mapping(labels, samples):
    matrix = []
    for sample in samples:
        line = [0] * len(labels)
        for label in sample:
            line[labels[label]] = 1
        matrix.append(line)
    return matrix


# reads data for multi-class classification with probabilities
def read_multi_class():
    try:
        f = open("multi-class.txt", "r")
    except IOError:
        print("File reading error!")
        return []
    no_class = int(f.readline().strip().split()[0])
    labels = {}
    line = f.readline().strip().split(",")
    for i, elem in enumerate(line):
        labels[elem] = i

    no_samples = int(f.readline().strip().split()[0])
    real_labels = []
    for _ in range(no_samples):
        line = f.readline().strip().split(",")
        real_labels_line = []
        for elem in line:
            real_labels_line.append(elem)
        real_labels.append(real_labels_line)
    real_probabilities = mapping(labels, real_labels)

    computed_probabilities = []
    for _ in range(no_samples):
        line = f.readline().strip().split(",")
        computed_probabilities_line = []
        for elem in line:
            computed_probabilities_line.append(float(elem))
        computed_probabilities.append(computed_probabilities_line)

    f.close()
    return no_class, real_probabilities, computed_probabilities


# reads data for multi-label classification with probabilities
def read_multi_label():
    try:
        f = open("multi-label.txt", "r")
    except IOError:
        print("File reading error!")
        return []
    no_class = int(f.readline().strip().split()[0])
    labels = {}
    line = f.readline().strip().split(",")
    for i, elem in enumerate(line):
        labels[elem] = i

    no_samples = int(f.readline().strip().split()[0])
    real_labels = []
    for _ in range(no_samples):
        line = f.readline().strip().split(",")
        real_labels_line = []
        for elem in line:
            real_labels_line.append(elem)
        real_labels.append(real_labels_line)
    real_probabilities = mapping(labels, real_labels)

    computed_probabilities = []
    for _ in range(no_samples):
        line = f.readline().strip().split(",")
        computed_probabilities_line = []
        for elem in line:
            computed_probabilities_line.append(float(elem))
        computed_probabilities.append(computed_probabilities_line)

    f.close()
    return no_class, real_probabilities, computed_probabilities


# Root Mean Square Error
def calculate_rmse(real_outputs, computed_outputs, k=0):
    square_sum = 0.0
    no_samples = len(real_outputs)
    for i in range(no_samples):
        square_sum += (real_outputs[i][k] - computed_outputs[i][k]) ** 2
    error = sqrt(square_sum / no_samples)
    return error


# calculates overall error
def calculate_error(real_outputs, computed_outputs, no_targets):
    sum = 0.0
    for i in range(no_targets):
        sum += calculate_rmse(real_outputs, computed_outputs, i)
    return sum/no_targets


# calculates accuracy, precision and recall for one label
def calculate_one_label_quality(real_labels, computed_labels, current_label):
    no_correct = 0
    for i in range(0, len(real_labels)):
        if real_labels[i] == computed_labels[i]:
            no_correct += 1
    accuracy = no_correct / len(real_labels)

    true_positive = false_positive = true_negative = false_negative = 0
    for i in range(0, len(real_labels)):
        if real_labels[i] == current_label and computed_labels[i] == current_label:
            true_positive += 1
        elif real_labels[i] != current_label and computed_labels[i] == current_label:
            false_positive += 1
        elif real_labels[i] != current_label and computed_labels[i] != current_label:
            true_negative += 1
        elif real_labels[i] == current_label and computed_labels[i] != current_label:
            false_negative += 1

    precision = true_positive / (true_positive + false_positive)
    recall = true_positive / (true_positive + false_negative)

    return accuracy, precision, recall


# calculates overall accuracy, precision and recall
def calculate_quality(real_labels, computed_labels, labels):
    accuracies = []
    precisions = []
    recalls = []
    for label in labels:
        acc, prec, recall = calculate_one_label_quality(real_labels, computed_labels, label)
        accuracies.append(acc)
        precisions.append(prec)
        recalls.append(recall)
    mean_accuracy = sum(accuracies)/len(accuracies)
    mean_precision = sum(precisions)/len(precisions)
    mean_recall = sum(recalls)/len(recalls)
    return mean_accuracy, mean_precision, mean_recall


# calculates loss function value for binary classification
def calculate_loss_binary_classification(real_probabilities, computed_probabilities):
    loss = 0.0
    for i in range(len(real_probabilities)):
        loss += -(real_probabilities[i][0] * log2(computed_probabilities[i][0]) + real_probabilities[i][1] * log2(computed_probabilities[i][1]))
    return loss / len(real_probabilities)


# calculates loss function value for multi-classes classification
def calculate_loss_multi_class_classification(real_probabilities, computed_probabilities, no_class):
    loss = 0.0
    for i in range(len(real_probabilities)):
        for j in range(no_class):
            loss += - real_probabilities[i][j] * log2(computed_probabilities[i][j])
    return loss / len(real_probabilities)


# calculates loss function value for multi-label classification
def calculate_loss_multi_label_classification(real_probabilities, computed_probabilities, no_class):
    loss = 0.0
    for i in range(no_class):
        class_loss = 0.0
        for j in range(len(real_probabilities)):
            class_loss += - (real_probabilities[j][i] * log2(computed_probabilities[j][i]) + (1 - real_probabilities[j][i]) * log2(1 - computed_probabilities[j][i]))
        loss += class_loss
    return loss / len(real_probabilities)


def main():
    no_targets, real_outputs, computed_outputs = read_regression()
    no_labels, labels, real_labels, computed_labels = read_classification()
    error = calculate_error(real_outputs, computed_outputs, no_targets)
    print("Error prediction: ", error)
    accuracy, precision, recall = calculate_quality(real_labels, computed_labels, labels)
    print("Accuracy: {}, Precision: {}, Recall: {}".format(accuracy, precision, recall))
    print("Loss function for regression: ", error)
    real_probabilities, computed_probabilities = read_probabilities()
    print("Loss function for binary classification: ", calculate_loss_binary_classification(real_probabilities, computed_probabilities))
    no_classes, real_probabilities, computed_probabilities = read_multi_class()
    print("Loss function for multi-class classification: ", calculate_loss_multi_class_classification(real_probabilities, computed_probabilities, no_classes))
    no_classes, real_probabilities, computed_probabilities = read_multi_label()
    print("Loss function for multi-label classification: ", calculate_loss_multi_label_classification(real_probabilities, computed_probabilities, no_classes))


if __name__ == '__main__':
    main()
