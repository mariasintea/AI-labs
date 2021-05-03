from math import sqrt


# statistical normalisation (centered around mean and standardisation)
def z_normalisation(features):
    mean = sum(features) / len(features)
    standard_deviation = sqrt((1 / len(features) * sum([(feat - mean) ** 2 for feat in features])))
    normalised_features = [(feat - mean) / standard_deviation for feat in features]
    return normalised_features


# normalisation for given features
def normalisation(input_data, output_data):
    feature1 = [elem[0] for elem in input_data]
    normalised_feature1 = z_normalisation(feature1)
    feature2 = [elem[1] for elem in input_data]
    normalised_feature2 = z_normalisation(feature2)
    normalised_inputs = [[x, y] for x, y in zip(normalised_feature1, normalised_feature2)]
    normalised_outputs = z_normalisation(output_data)
    return normalised_inputs, normalised_outputs