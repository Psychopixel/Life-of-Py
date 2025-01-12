import numpy as np
from src.neural_net import NeuralNet

def test_forward_pass():
    nn = NeuralNet(input_size=3, hidden_size=5, output_size=2)
    input_vec = np.array([0.5, -0.2, 0.7])
    output = nn.forward(input_vec)
    # output shape should be (2,)
    assert output.shape == (2,)

def test_relu():
    nn = NeuralNet(1, 1, 1)
    x = np.array([[-1.0], [0.0], [1.0]])
    # manually test nn.relu
    out = nn.relu(x)
    assert (out == np.array([[0.0], [0.0], [1.0]])).all()

def test_mutate():
    nn = NeuralNet(input_size=2, hidden_size=2, output_size=2)

    # capture old weights
    old_W1 = nn.W1.copy()
    nn.mutate(mutation_rate=1.0, mutation_stddev=0.1)
    # with mutation_rate=1.0, every param changes
    # compare to see if at least one changed
    diff = np.abs(old_W1 - nn.W1)
    assert np.any(diff > 0.0), "Weights should have changed with mutation_rate=1.0"
