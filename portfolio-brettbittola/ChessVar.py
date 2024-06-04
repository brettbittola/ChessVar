# Author:  Brett Bittola
# GitHub username: brettbittola
# Date: 12/10/2023
# Description: A game of chess with a board and unique moves for each piece.

class ChessVar:
    """Creates a new game of chess"""

    def __init__(self):
        """Initializes a new game of chess, setting the game state to unfinished and setting the team turn to white"""
        self._game_state = 'UNFINISHED'
        self._team_turn = 'white'
        self._white_piece_list = ['pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'rook', 'rook',
                                  'knight', 'knight', 'bishop', 'bishop', 'king', 'queen']
        self._black_piece_list = ['pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'rook', 'rook',
                                  'knight', 'knight', 'bishop', 'bishop', 'king', 'queen']
        self._board = Board()
        self._column_nums = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8}

    def get_game_state(self):
        """Returns if the game is still being played or, if not, who won"""
        return self._game_state

    def set_game_state(self, new_state):
        """Updates if the game is still being played or, if not, who won"""
        self._game_state = new_state

    def set_team_turn(self):
        """Switches the team that will be making the next move"""
        if self._team_turn == 'white':
            self._team_turn = 'black'
        else:
            self._team_turn = 'white'

    def get_team_turn(self):
        """Returns whose turn it is"""
        return self._team_turn

    def remove_piece(self, color, piece):
        """Remove a captured piece from piece list"""
        if color == 'white':
            self._white_piece_list.remove(piece)
        else:
            self._black_piece_list.remove(piece)

    def get_white_piece_list(self):
        """Returns a list of white chess pieces"""
        return self._white_piece_list

    def get_black_piece_list(self):
        """Returns a list of black chess pieces"""
        return self._black_piece_list

    def make_move(self, first_square_lower, second_square_lower):
        """Moves a piece to a new square, accessing the two square classes being used, checks to confirm a piece is in
        the original square, checks the type and color of that piece, checks that the move is valid for that piece type,
        and if there is a piece on the second square, confirms that the second piece is a different color than the first
        piece. If a piece is captured, that piece is removed from its teams piece list and checks to see if any other
        pieces of this type exist. If not, the game is over."""

        first_square = self._board.get_square(first_square_lower.upper())
        second_square = self._board.get_square(second_square_lower.upper())
        moving_piece = first_square.get_piece()

        if self.get_game_state() != 'UNFINISHED':
            return False

        if moving_piece.get_piece_color() != self.get_team_turn():
            return False

        if moving_piece is None:
            return False

        if isinstance(moving_piece, Rook):
            if self.check_rook_path(first_square, second_square) is False:
                return False
        elif isinstance(moving_piece, Bishop):
            if self.check_bishop_path(first_square, second_square) is False:
                return False
        elif isinstance(moving_piece, Queen):
            if self.check_queen_path(first_square, second_square) is False:
                return False

        if first_square.get_piece() is None:
            return False

        if moving_piece and moving_piece.valid_move(first_square, second_square):
            if second_square.get_piece() is not None:
                if self.capture_piece(second_square) is False:
                    return False

            second_square.set_piece(moving_piece)
            first_square.set_piece(None)
            self.set_team_turn()
            moving_piece.set_square(second_square)
            return True

        return moving_piece.valid_move(first_square, second_square)

    def capture_piece(self, second_square):
        """Removes a chess piece from the board"""
        if second_square.get_piece() is not None:
            captured_piece = second_square.get_piece()
            piece_color = captured_piece.get_piece_color()
            piece_type = captured_piece.get_piece()

            if piece_color == self._team_turn:
                return False

            if piece_color == 'white':
                self.remove_piece('white', piece_type)
                piece_list = self.get_white_piece_list()
                if piece_type not in piece_list:
                    self.set_game_state('BLACK_WON')
                    return True
            else:
                self.remove_piece('black', piece_type)
                piece_list = self.get_black_piece_list()
                if piece_type not in piece_list:
                    self.set_game_state('WHITE_WON')
                    return True
        return False

    def check_rook_path(self, first_square, second_square):
        """Checks if there are any pieces between the first and second square of a move for a rook"""
        first_square_row = int(first_square.get_row())
        second_square_row = int(second_square.get_row())
        first_square_column = self._column_nums[first_square.get_column()]
        first_square_column_letter = first_square.get_column()
        second_square_column = self._column_nums[second_square.get_column()]

        row_difference_actual = first_square_row - second_square_row
        column_difference_actual = second_square_column - first_square_column
        row_difference = abs(row_difference_actual)
        column_difference = abs(column_difference_actual)

        if row_difference == 0:
            for column in range(min(first_square_column, second_square_column) + 1, max(first_square_column,
                                                                                        second_square_column)):
                column_letter = next(key for key, value in self._column_nums.items() if value == column)
                square = self._board.get_square(f"{column_letter}{first_square_row}")
                if square.get_piece() is not None:
                    return False

        if column_difference == 0:
            for row in range(min(first_square_row, second_square_row) + 1, max(first_square_row, second_square_row)):
                square = self._board.get_square(f"{first_square_column_letter}{row}")
                if square.get_piece() is not None:
                    return False

        if row_difference != 0 and column_difference != 0:
            return False

        return True

    def check_bishop_path(self, first_square, second_square):
        """Checks if there are any pieces between the first and second square of a move for a bishop"""
        first_square_row = int(first_square.get_row())
        second_square_row = int(second_square.get_row())
        first_square_column = self._column_nums[first_square.get_column()]
        second_square_column = self._column_nums[second_square.get_column()]
        column_letters = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H'}

        row_difference_actual = second_square_row - first_square_row
        column_difference_actual = second_square_column - first_square_column

        if row_difference_actual > 0:
            row_direction = 1
        else:
            row_direction = -1
        if column_difference_actual > 0:
            column_direction = 1
        else:
            column_direction = -1

        current_row = first_square_row + row_direction
        current_column = first_square_column + column_direction

        while current_row != second_square_row and current_column != second_square_column:
            square = self._board.get_square(f"{column_letters[current_column]}{current_row}")
            if square.get_piece() is None:
                current_row += row_direction
                current_column += column_direction
            else:
                return False

        return True

    def check_queen_path(self, first_square, second_square):
        """Checks if there are any pieces between the first and second square of a move for a queen"""
        return self.check_rook_path(first_square, second_square) or self.check_bishop_path(first_square, second_square)


class Board:
    """Represents the chess board, using the square classes and piece classes"""

    def __init__(self):
        """Initializes 8 rows and 8 columns of Square classes to make a visual chess board, also initializes 16 Pieces
        of each color, in their correct location"""
        self._chess_board = [[Square('A', '1'), Square('A', '2'), Square('A', '3'), Square('A', '4'), Square('A', '5'),
                              Square('A', '6'), Square('A', '7'), Square('A', '8')],
                             [Square('B', '1'), Square('B', '2'), Square('B', '3'), Square('B', '4'), Square('B', '5'),
                              Square('B', '6'), Square('B', '7'), Square('B', '8')],
                             [Square('C', '1'), Square('C', '2'), Square('C', '3'), Square('C', '4'), Square('C', '5'),
                              Square('C', '6'), Square('C', '7'), Square('C', '8')],
                             [Square('D', '1'), Square('D', '2'), Square('D', '3'), Square('D', '4'), Square('D', '5'),
                              Square('D', '6'), Square('D', '7'), Square('D', '8')],
                             [Square('E', '1'), Square('E', '2'), Square('E', '3'), Square('E', '4'), Square('E', '5'),
                              Square('E', '6'), Square('E', '7'), Square('E', '8')],
                             [Square('F', '1'), Square('F', '2'), Square('F', '3'), Square('F', '4'), Square('F', '5'),
                              Square('F', '6'), Square('F', '7'), Square('F', '8')],
                             [Square('G', '1'), Square('G', '2'), Square('G', '3'), Square('G', '4'), Square('G', '5'),
                              Square('G', '6'), Square('G', '7'), Square('G', '8')],
                             [Square('H', '1'), Square('H', '2'), Square('H', '3'), Square('H', '4'), Square('H', '5'),
                              Square('H', '6'), Square('H', '7'), Square('H', '8')]]

        self._chess_pieces = [Rook('A1', 'white'), Knight('B1', 'white'), Bishop('C1', 'white'), Queen('D1', 'white'),
                              King('E1', 'white'), Bishop('F1', 'white'), Knight('G1', 'white'), Rook('H1', 'white'),
                              Pawn('A2', 'white'), Pawn('B2', 'white'), Pawn('C2', 'white'), Pawn('D2', 'white'),
                              Pawn('E2', 'white'), Pawn('F2', 'white'), Pawn('G2', 'white'), Pawn('H2', 'white'),
                              Rook('A8', 'black'), Knight('B8', 'black'), Bishop('C8', 'black'), Queen('D8', 'black'),
                              King('E8', 'black'), Bishop('F8', 'black'), Knight('G8', 'black'), Rook('H8', 'black'),
                              Pawn('A7', 'black'), Pawn('B7', 'black'), Pawn('C7', 'black'), Pawn('D7', 'black'),
                              Pawn('E7', 'black'), Pawn('F7', 'black'), Pawn('G7', 'black'), Pawn('H7', 'black')]
        for piece in self._chess_pieces:
            square = self.get_square(piece.get_square())
            square.set_piece(piece)

        self._column_nums = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8}

    def get_chess_board(self):
        """Returns a list of squares on the chess board"""
        return self._chess_board

    def get_chess_pieces(self):
        """Returns a list of chess pieces"""
        return self._chess_pieces

    def get_square(self, square_name):
        """Returns the square object from given square name"""
        for row in self._chess_board:
            for square in row:
                if square.get_column() + square.get_row() == square_name:
                    return square
        return None

    def print_board(self):
        """Returns a visual copy of the board"""
        for column in self._chess_board:
            line = []
            for item in column:
                if item.get_piece() is None:
                    line.append(item.get_column() + item.get_row())
                else:
                    line.append(repr(item.get_piece()))
            print(line)

    def get_column_nums(self):
        """Returns a dictionary of chess board columns with their numeric value"""
        return self._column_nums


class Square:
    """Represents a square on the board, and shows what Piece is currently on that square, if any"""

    def __init__(self, column, row):
        """Initializes a row, column and sets value to None for a square on the chess board"""
        self._row = row
        self._column = column
        self._piece = None

    def __repr__(self):
        """Returns an easy-to-read representation of this square"""
        if self._piece is None:
            return "_"
        else:
            return f"{self._column}{self._row}"

    def get_row(self):
        """Returns the row a square is in"""
        return self._row

    def get_column(self):
        """Returns the column a square is in"""
        return self._column

    def get_piece(self):
        """Returns what piece is on this square, or None if there isn't one"""
        return self._piece

    def set_piece(self, piece):
        """Changes the value of a square when a move is made"""
        self._piece = piece
        if piece is None:
            self._piece = None


class Piece:
    """Represents a chess piece"""

    def __init__(self, starting_square, color):
        """Initializes a chess piece class with color, piece type, and starting square for that piece. Also sets a
        string value for each piece to be used in the piece list."""
        self._square = starting_square
        self._color = color

    def get_square(self):
        """Returns location on the board of this piece"""
        return self._square

    def set_square(self, square):
        """Moves this piece's square on the board to a new square"""
        self._square = square

    def get_piece_color(self):
        """Returns the piece color"""
        return self._color


class Rook(Piece):
    """Represents a rook that can only move within a row or a column each turn. Inherits all other methods from Piece
    class"""

    def __init__(self, starting_square, color):
        """Initializes a rook chess piece"""
        self._piece = 'rook'
        self._color = color
        super().__init__(starting_square, color)
        self._square = starting_square
        self._column_nums = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8}

    def __repr__(self):
        """Returns a readable name when the object is printed"""
        if self._color == 'white':
            return 'R'
        else:
            return 'r'

    def get_piece(self):
        """Returns the value of a chess piece"""
        return self._piece

    def get_square(self):
        """Returns the square a piece is on"""
        return self._square

    def get_piece_color(self):
        """Returns the color of a chess piece"""
        return self._color

    def valid_move(self, first_square, second_square):
        """Defines the movement rules for a rook"""
        valid_move = False
        column_nums = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8}
        rows = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        first_square_row = int(first_square.get_row())
        second_square_row = int(second_square.get_row())

        row_difference = abs(second_square_row - first_square_row)
        column_difference = abs(column_nums[second_square.get_column()] - column_nums[first_square.get_column()])

        if row_difference == 0:
            if second_square.get_column() in columns:
                valid_move = True
        elif column_difference == 0:
            if second_square_row in rows:
                valid_move = True

        return valid_move


class Bishop(Piece):
    """Represents a bishop that can only move diagonally on a certain color square. Inherits all other methods from
    Piece class"""

    def __init__(self, starting_square, color):
        """Initializes a bishop chess piece"""
        self._piece = 'bishop'
        super().__init__(starting_square, color)
        self._square = starting_square
        self._color = color

    def __repr__(self):
        """Returns a readable name when the object is printed"""
        if self._color == 'white':
            return 'B'
        else:
            return 'b'

    def get_piece(self):
        """Returns the value of a chess piece"""
        return self._piece

    def get_square(self):
        """Returns the square a piece is on"""
        return self._square

    def get_piece_color(self):
        """Returns the color of a chess piece"""
        return self._color

    def valid_move(self, first_square, second_square):
        """Changes Piece class method to use bishop's valid moves"""
        valid_move = False
        column_nums = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8}

        first_square_row = int(first_square.get_row())
        second_square_row = int(second_square.get_row())

        row_difference = abs(first_square_row - second_square_row)
        column_difference = abs(column_nums[second_square.get_column()] - column_nums[first_square.get_column()])

        if column_difference == row_difference:
            valid_move = True

        return valid_move


class Knight(Piece):
    """Represents a knight who can move two spaces one way then one space perpendicular. Inherits all other methods from
     Piece class"""

    def __init__(self, starting_square, color):
        """Initializes a knight chess piece"""
        self._piece = 'knight'
        super().__init__(starting_square, color)
        self._square = starting_square
        self._color = color

    def __repr__(self):
        """Returns a readable name when the object is printed"""
        if self._color == 'white':
            return 'K'
        else:
            return 'k'

    def get_piece(self):
        """Returns the value of a chess piece"""
        return self._piece

    def get_square(self):
        """Returns the square a piece is on"""
        return self._square

    def get_piece_color(self):
        """Returns the color of a chess piece"""
        return self._color

    def valid_move(self, first_square, second_square):
        """Changes Piece class method to use king's valid moves"""
        valid_move = False
        column_nums = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8}

        first_square_row = int(first_square.get_row())
        second_square_row = int(second_square.get_row())

        row_difference = abs(first_square_row - second_square_row)
        column_difference = abs(column_nums[second_square.get_column()] - column_nums[first_square.get_column()])

        if column_difference == 1 and row_difference == 2:
            valid_move = True
        elif column_difference == 2 and row_difference == 1:
            valid_move = True

        return valid_move


class King(Piece):
    """Represents a king that can only move one space at a time. Inherits all other methods from Piece class"""

    def __init__(self, starting_square, color):
        """Initializes a king chess piece"""
        self._piece = 'king'
        super().__init__(starting_square, color)
        self._square = starting_square
        self._color = color

    def __repr__(self):
        """Returns a readable name when the object is printed"""
        if self._color == 'white':
            return 'M'  # since knight also starts with a k, we use M for king since it resembles a crown
        else:
            return 'm'

    def get_piece(self):
        """Returns the value of a chess piece"""
        return self._piece

    def get_square(self):
        """Returns the square a piece is on"""
        return self._square

    def get_piece_color(self):
        """Returns the color of a chess piece"""
        return self._color

    def valid_move(self, first_square, second_square):
        """Changes Piece class method to use king's valid moves"""
        valid_move = False
        column_nums = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8}

        first_square_row = int(first_square.get_row())
        second_square_row = int(second_square.get_row())

        row_difference = abs(first_square_row - second_square_row)
        column_difference = abs(column_nums[second_square.get_column()] - column_nums[first_square.get_column()])

        if (column_difference <= 1) and (row_difference <= 1):
            valid_move = True

        return valid_move


class Queen(Piece):
    """Represents a queen that can move in any direction any number of spaces. Inherits all other methods from Piece
    class"""

    def __init__(self, starting_square, color):
        """Initializes a queen chess piece"""
        self._piece = 'queen'
        super().__init__(starting_square, color)
        self._square = starting_square
        self._color = color

    def __repr__(self):
        """Returns a readable name when the object is printed"""
        if self._color == 'white':
            return 'Q'
        else:
            return 'q'

    def get_piece(self):
        """Returns the value of a chess piece"""
        return self._piece

    def get_square(self):
        """Returns the square a piece is on"""
        return self._square

    def get_piece_color(self):
        """Returns the color of a chess piece"""
        return self._color

    def valid_move(self, first_square, second_square):
        """Changes Piece class method to use queen's valid moves"""
        valid_move = False
        column_nums = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8}
        rows = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        first_square_row = int(first_square.get_row())
        second_square_row = int(second_square.get_row())

        row_difference = abs(first_square_row - second_square_row)
        column_difference = abs(column_nums[second_square.get_column()] - column_nums[first_square.get_column()])

        if column_difference == row_difference:
            valid_move = True
        elif (row_difference == 0) or (column_difference == 0):
            if second_square.get_row() in rows or second_square.get_column() in columns:
                valid_move = True

        return valid_move


class Pawn(Piece):
    """Represents a pawn that can move one space forward unless it is attacking, or it is it's first move. Inherits all
    other methods from Piece class"""

    def __init__(self, starting_square, color):
        """Initializes a pawn chess piece"""
        self._piece = 'pawn'
        super().__init__(starting_square, color)
        self._square = starting_square
        self._color = color
        self._first_move = 0

    def __repr__(self):
        """Returns a readable name when the object is printed"""
        if self._color == 'white':
            return 'P'
        else:
            return 'p'

    def get_piece(self):
        """Returns the value of a chess piece"""
        return self._piece

    def get_square(self):
        """Returns the square a piece is on"""
        return self._square

    def get_piece_color(self):
        """Returns the color of a chess piece"""
        return self._color

    def valid_move(self, first_square, second_square):
        """Determines if a pawn's move is valid"""
        valid_move = False
        column_nums = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8}

        first_square_row = int(first_square.get_row())
        second_square_row = int(second_square.get_row())

        row_difference = abs(first_square_row - second_square_row)
        column_difference = abs(column_nums[second_square.get_column()] - column_nums[first_square.get_column()])

        if self._first_move == 0:
            if column_difference == 0:
                if row_difference <= 2:
                    if second_square.get_piece() is None:
                        valid_move = True
                        self._first_move += 1

        elif column_difference == 0:
            if row_difference == 1:
                if second_square.get_piece() is None:
                    valid_move = True

        elif second_square.get_piece() is not None:
            if column_difference == 1 and row_difference == 1:
                valid_move = True

        return valid_move
