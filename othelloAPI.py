class API:

    def __init__(self):
        self.__board = [
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", "B", "W", " ", " ", " "],
            [" ", " ", " ", "W", "B", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "]
        ]
        self.black_move = True

    def get_score(self) -> list[int]:
        white_score = 0
        black_score = 0
        for i in self.__board:
            white_score+= i.count("W")
            black_score+= i.count("B")

        return [white_score, black_score]

    def __valid_coord(self, x, y) -> bool:
        return 0 <= x <= 7 and 0 <= y <= 7

    def __get_possible_moves(self) -> list[list[int]]:

        possible_move_coordinates = []

        for i in range(8):
            for j in range(8):
                trav_list = self.__check_valid_move(i, j)
                if trav_list:
                    possible_move_coordinates.append([i, j])
        return possible_move_coordinates

    def __check_valid_move(self, row: int, col: int) -> list[list[int]]:
        if self.__board[row][col] != " ":
            return []
        player = "B" if self.black_move else "W"
        opponent = "B" if not self.black_move else "W"

        traverse_lists = []

        all_possible_directions = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]

        for x, y in all_possible_directions:
            nx = x + row
            ny = y + col
            if self.__valid_coord(nx, ny) and self.__board[nx][ny] == opponent:
                travers_possible = True
                while self.__board[nx][ny] != player:
                    nx += x
                    ny += y
                    if not self.__valid_coord(nx, ny):
                        travers_possible = False
                        break
                if travers_possible and self.__board[nx][ny] != " ":
                    traverse_lists.append([x, y])

        return traverse_lists

    def make_move(self, row: int, col: int) -> None:
        traversals = self.__check_valid_move(row, col)
        if not traversals:
            return

        player = "B" if self.black_move else "W"
        opponent = "B" if not self.black_move else "W"
        for x, y in traversals:
            nx = row + x
            ny = col + y
            while self.__board[nx][ny] != player:
                self.__board[nx][ny] = player
                nx += x
                ny += y
        if self.__get_possible_moves():
            self.black_move = not self.black_move
        self.__board[row][col] = player

    def get_board(self) -> list[list[str]]:
        coordinates = self.__get_possible_moves()
        for x, y in coordinates:
            self.__board[x][y] = "N"

        return self.__board


