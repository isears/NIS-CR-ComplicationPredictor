"""
Define a simple 3-layer feedforward neural network classifier
"""

import torch
import torch.nn as nn


class SimpleFFNN(nn.Module):
    def __init__(self, n_features, hidden_dim=32) -> None:
        super().__init__()

        self.ffnn = nn.Sequential(
            nn.Linear(n_features, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, x):
        y_hat = self.ffnn(x) # x: torch.float32
        return torch.sigmoid(y_hat)
