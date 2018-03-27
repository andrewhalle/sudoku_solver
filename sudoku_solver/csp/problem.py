from copy import deepcopy

class Problem:
    def __init__(self):
        self.variables = []
        self.constraints = []

    def is_satisfied(self):
        for c in self.constraints:
            if not c.is_satisfied():
                return False
        return True

    def can_be_satisfied(self):
        for c in self.constraints:
            if not c.can_be_satisfied():
                return False
        return True

    def neighbors(self):
        retval = []
        first_unassigned_variable = None
        for i in range(len(self.variables)):
            v = self.variables[i]
            if not v.is_assigned():
                first_unassigned_variable = i
                break
        if first_unassigned_variable == None:
            return []
        for value in self.variables[first_unassigned_variable].domain:
            nbr = deepcopy(self)
            nbr.variables[i].assign(value)
            retval.append(nbr)
        return retval

    def dump_domains(self):
        for v in self.variables:
            print(v.domain)
        print()

    def backtracking_search(self):
        start = deepcopy(self)
        curr = start
        stack = [start]
        while not curr.is_satisfied():
            curr = stack.pop(0)
            #curr.dump_domains()
            if not curr.can_be_satisfied():
                continue
            stack += curr.neighbors()
        if not curr.is_satisfied():
            raise ValueError("could not satisfy all constraints")
        self.variables = curr.variables
        self.constraints = curr.constraints

