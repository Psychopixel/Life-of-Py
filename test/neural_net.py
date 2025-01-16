import numpy as np
import random

class NeuralNet:
    """
    A simple feedforward neural network with one hidden layer.
    """

    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        """
        :param input_size: Number of input neurons
        :param hidden_size: Number of neurons in hidden layer
        :param output_size: Number of output neurons
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # Initialize weights (e.g., Xavier or small random)
        # We'll store them as NumPy arrays
        self.W1 = np.random.randn(self.hidden_size, self.input_size) * 0.1
        self.b1 = np.zeros((self.hidden_size, 1))
        self.W2 = np.random.randn(self.output_size, self.hidden_size) * 0.1
        self.b2 = np.zeros((self.output_size, 1))

    def forward(self, inputs: np.ndarray) -> np.ndarray:
        """
        Compute the forward pass.
        :param inputs: (input_size,) or (input_size, 1) shape
        :return: Output activations (output_size,) shape
        """
        # Reshape inputs to (input_size, 1) if needed
        if inputs.ndim == 1:
            inputs = inputs.reshape(-1, 1)  # column vector

        # Hidden layer: z1 = W1*inputs + b1, then ReLU
        z1 = np.dot(self.W1, inputs) + self.b1
        a1 = self.relu(z1)

        # Output layer: z2 = W2*a1 + b2
        z2 = np.dot(self.W2, a1) + self.b2
        # We could do a softmax or leave it raw. 
        # For discrete actions, we might just pick argmax from these raw scores.
        return z2.flatten()  # shape (output_size,)

    def relu(self, x: np.ndarray) -> np.ndarray:
        return np.maximum(0, x)

    def mutate(self, mutation_rate: float, mutation_stddev: float):
        """
        Apply random noise to weights/biases with a probability of mutation.
        :param mutation_rate: chance of each weight being mutated
        :param mutation_stddev: std deviation of Gaussian noise
        """
        # We'll mutate W1, b1, W2, b2 in place
        self._mutate_array(self.W1, mutation_rate, mutation_stddev)
        self._mutate_array(self.b1, mutation_rate, mutation_stddev)
        self._mutate_array(self.W2, mutation_rate, mutation_stddev)
        self._mutate_array(self.b2, mutation_rate, mutation_stddev)

    def _mutate_array(self, arr: np.ndarray, rate: float, stddev: float):
        """
        For each element in arr, with probability rate, add Gaussian noise ~ N(0, stddev).
        """
        rows, cols = arr.shape
        for r in range(rows):
            for c in range(cols):
                if random.random() < rate:
                    arr[r, c] += random.gauss(0, stddev)
