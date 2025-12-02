"""
Task 1: Predict where are the mines based on the game states (Model needs to learn logic)

Input: Game States of Board (random states)
Output: Where is a the Mine
Model: Convolutional layer with ResNet
Loss: Binary Cross Entropy (Black Box: Model only predicts adjacent mines, however the loss is calculated on whether the mine is correctly predicted globally)
Training: Adam Optimizer
"""
def mine_prediction_model():
    pass

"""
Task 2: Reinforcement Learning Bot to play Minesweeper

Input: Current Game State (and you keep feeding that in after every move)
Output: Next Cell to Open (try to train the model to predict the mines and avoid them)
Model: Q-Learning ??? maybe Deep Q-Network
Loss: Black Box: Q-Learning Loss
Training: Adam Optimizer
"""
def minesweeper_rl_bot():
    pass
