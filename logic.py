"""
Purpose: The purpose of this file is to implement the logic bot for playing the game of Minesweeper. This bot will be used to generate the board and to make decisions based on the current state of the board.
"""

from board import generate_board
import random

# From recitation 8
class LogicBot:
    def __init__(self, game_environment):
        self.game = game_environment
        self.H, self.W = game.shape

        # Initialize sets [cite: 15]
        self.cells_remaining = set((r, c) for r in range(self.H) for c in range(self.W))
        self.inferred_safe = set()
        self.inferred_mine = set()

        # Store revealed clues: { (r, c) : clue_number } [cite: 16]
        self.clue_numbers = {}
        self.game_over = False

    def play_game(self):
        # Loop until game ends [cite: 17]
        while not self.game_over:

            # 1. Choose a cell to open [cite: 18]
            if self.inferred_safe:
                cell_to_open = self.inferred_safe.pop()
            else:
                # If no safe cells, pick a random cell from "remaining" [cite: 18]
                # (Make sure not to pick one we already think is a mine)
                available_cells = self.cells_remaining - self.inferred_mine
                if not available_cells:
                    break # No more cells to open
                cell_to_open = random.choice(list(available_cells))

            # 2. Open the cell [cite: 19]
            (r, c) = cell_to_open
            clue = self.game.open(r, c) # Assume game.open() returns -1 for a mine

            self.cells_remaining.discard((r, c))

            if clue == -1: # Hit a mine [cite: 19]
                self.game_over = True
                # (record results)
                break
            else:
                # 3. Update clues [cite: 20]
                self.clue_numbers[(r, c)] = clue

                # 4. Run the inference loop [cite: 24]
                self.run_inference_loop()

        # (Return game results)
        pass

    def run_inference_loop(self):
        # Keep looping until no new inferences are made [cite: 24]
        while True:
            new_inferences_made = False

            # For each cell with a revealed clue [cite: 21]
            for (r, c), clue_value in self.clue_numbers.items():

                # (You need a helper function get_neighbors(r, c))
                all_neighbors = self.get_neighbors(r, c)

                # Count neighbors
                unrevealed_neighbors = []
                num_inferred_mines_around = 0
                num_inferred_safe_around = 0
                num_revealed_safe_around = 0

                for nr, nc in all_neighbors:
                    if (nr, nc) in self.inferred_mine:
                        num_inferred_mines_around += 1
                    elif (nr, nc) in self.inferred_safe:
                        num_inferred_safe_around += 1
                    elif (nr, nc) in self.clue_numbers:
                        # This cell is already open, so it's safe
                        num_revealed_safe_around += 1
                    elif (nr, nc) in self.cells_remaining:
                        # This is an unknown, un-inferred neighbor
                        unrevealed_neighbors.append((nr, nc))

                num_unrevealed = len(unrevealed_neighbors)
                if num_unrevealed == 0:
                    continue

                # Core Logic 1: Mark Mines
                # If (clue_value) - (# known mines) == (# unrevealed neighbors)
                # Then all unrevealed neighbors MUST be mines.
                if (clue_value - num_inferred_mines_around) == num_unrevealed:
                    for (nr, nc) in unrevealed_neighbors:
                        if (nr, nc) not in self.inferred_mine:
                            self.inferred_mine.add((nr, nc))
                            self.cells_remaining.discard((nr, nc)) # Remove from "remaining" [cite: 22]
                            new_inferences_made = True


                # Core Logic 2: Mark Safe
                # (total # neighbors) - (clue_value) == total # of safe neighbors
                # (known safe neighbors) = (inferred safe) + (revealed safe)

                total_neighbors_count = len(all_neighbors)
                total_safe_neighbors_count = total_neighbors_count - clue_value
                known_safe_neighbors_count = num_inferred_safe_around + num_revealed_safe_around

                # If (total safe neighbors needed) - (known safe neighbors) == (# unrevealed neighbors)
                # Then all unrevealed neighbors MUST be safe.
                if (total_safe_neighbors_count - known_safe_neighbors_count) == num_unrevealed:
                    for (nr, nc) in unrevealed_neighbors:
                        if (nr, nc) not in self.inferred_safe:
                            self.inferred_safe.add((nr, nc))
                            # (Do NOT remove from cells_remaining.
                            #  They will be picked by the main loop.)
                            new_inferences_made = True

            # If this whole loop made no new inferences, we are done.
            if not new_inferences_made:
                break

    def get_neighbors(self, r, c):
        # (Helper function: returns valid (r, c) coords for all 8 neighbors)
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.H and 0 <= nc < self.W:
                    neighbors.append((nr, nc))
        return neighbors