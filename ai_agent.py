import random


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __hash__(self):
        return hash(self.count)

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count and self.count !=0:
            return self.cells
        return False

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return False

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        #1
        self.moves_made.add(cell)
        if cell not in self.safes:
            #2
            self.mark_safe(cell)

        new_sentence = self.neighbors(cell, count)
        self.knowledge.append(new_sentence)

        for sentence in self.knowledge:

            # If the sentence's cells are known mines, mark all as mine
            if sentence.known_mines():
                for additional_cell in sentence.known_mines().copy():
                    self.mark_mine(additional_cell)

            # If the sentence's cells are known safes, mark all as safe
            if sentence.known_safes():
                for additional_cell in sentence.known_safes().copy():
                    self.mark_safe(additional_cell)

        for i in self.knowledge.copy():
            for j in self.knowledge.copy():
                superset = i.cells
                count2 = i.count
                subset = j.cells
                count1 = j.count

                # Ignore when comparing the same set
                if subset == superset:
                    continue

                if subset.issubset(superset):
                    another_sentence = Sentence(
                        superset.difference(subset), count2 - count1)
                    self.knowledge.append(another_sentence)

        # Clean duplicate sentences by adding hash function in Sentence class
        self.knowledge = list(set(self.knowledge))

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe_cell in self.safes:
            if safe_cell not in self.moves_made:
                return safe_cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        moves = []
        for i in range(self.height):
            for j in range(self.width):
                cell=(i,j)
                if cell not in self.moves_made and cell not in self.mines:
                    moves.append(cell)

        if len(moves) != 0:
            return random.choice(moves)
        return None


    def neighbors(self, cell, count):

        # Returns a sentence including undetermined neighboring cells of the given cell and the respective count
        neighboring_cells = set()

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the given cell itself
                if (i, j) == cell:
                    continue

                # Add undetermined cells only within the board
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i, j) in self.mines:
                        count -= 1
                        continue
                    if (i, j) not in self.safes or (i, j) not in self.moves_made:
                        neighboring_cells.add((i, j))
        return Sentence(neighboring_cells, count)
