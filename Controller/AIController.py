from BlueBrain import NeuralNetwork as nn


input_layer_size = 2
secret_layer_size = 4
secret_layer_count = 32
generation_count = 20

test_nn = nn.NeuralNetwork(input_layer_size, secret_layer_size, secret_layer_count,
                           generation_count)
test2_nn = nn.NeuralNetwork(input_layer_size, secret_layer_size, secret_layer_count,
                            generation_count)
test_nn.set_up()

test_nn.fit(input_x=[
    [1635, 375],
    [975, 525],
],
    output_y=[[0, 2, 2, 1],[0, 2, 2, 1]], iteration=1, genetic_iteration=1)


test_nn.save_model_by_path("./Models/SitOnCircle_sefa_64_91.dat")

# Hangi dosyada çaışıyorsak o dosyanın yolu üzerinden işlem yapmamız gerekiyor
with open("../Models/SitOnCircle_sefa_64_91.dat", 'rb') as f:
    test_nn = test_nn.load_model_by_file(f)


predict = test_nn.predict(
    [
        [1635, 375],
        [975, 525],
    ])

print(predict)
