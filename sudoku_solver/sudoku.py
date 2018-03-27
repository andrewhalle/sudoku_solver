from sudoku_solver.csp import Problem, Variable, Constraint

class Sudoku:
    def __init__(self, data=[]):
        if not isinstance(data, list) or not len(data) == 9 or not isinstance(data[0], list) or not len(data[0]) == 9:
            raise ValueError("sudoku data must be 2D list of integers")
        self.data = data

    def format(self):
        for i in range(9):
            print_str = ""
            for j in range(9):
                print_str += str(self.data[i][j])
            print(print_str)

    def __indexes_in_box(box_num):
        start_row = 3 * (box_num // 3)
        end_row = start_row + 3
        start_col = 3 * (box_num % 3)
        end_col = start_col + 3
        retval = []
        for i in range(start_row, end_row):
            for j in range(start_col, end_col):
                retval.append(9*i + j)
        return retval

    def solve(self):
        p = Problem()

        # add all variables
        for i in range(9):
            for j in range(9):
                if self.data[i][j] == 0:
                    p.variables.append(Variable(set(range(1, 10))))
                else:
                    p.variables.append(Variable({ self.data[i][j] }))
        
        # constraint function
        constraint_f = lambda x,y: x != y

        # add row constraints
        for row in range(9):
            for i in range(8):
                for j in range(i+1, 9):
                    p.constraints.append(Constraint(p.variables[9*row + i], p.variables[9*row + j], constraint_f))

        # add column constraints
        for col in range(9):
            for i in range(8):
                for j in range(i+1, 9):
                    p.constraints.append(Constraint(p.variables[9*i + col], p.variables[9*j + col], constraint_f))

        # add box constraints
        for box in range(9):
            indexes = Sudoku.__indexes_in_box(box)
            for i in range(8):
                for j in range(i+1, 9):
                    p.constraints.append(Constraint(p.variables[indexes[i]], p.variables[indexes[j]], constraint_f))

        p.backtracking_search()
        for index in range(len(p.variables)):
            row = index // 9
            col = index % 9
            self.data[row][col] = p.variables[index].value()

