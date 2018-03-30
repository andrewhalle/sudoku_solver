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
        for v in self.variables:
            if not v.domain:
                return False
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

    def arc_reduce(constraint):
        v1_domain = list(constraint.v1.domain)
        v2_domain = list(constraint.v2.domain)
        change = False
        for value1 in v1_domain:
            satisfiable = False
            for value2 in v2_domain:
                if constraint.f(value1, value2):
                    satisfiable = True
            if not satisfiable:
                constraint.v1.remove_from_domain(value1)
                change = True

        v1_domain = list(constraint.v1.domain)
        v2_domain = list(constraint.v2.domain)
        for value2 in v2_domain:
            satisfiable = False
            for value1 in v1_domain:
                if constraint.f(value1, value2):
                    satisfiable = True
            if not satisfiable:
                constraint.v2.remove_from_domain(value2)
                change = True

        return change

    def enforce_arc_consistency(self):
        queue = []
        for c in self.constraints:
            queue.append(c)
        while queue:
            curr = queue.pop(0)
            if Problem.arc_reduce(curr):
                if not curr.v1.domain or not curr.v2.domain:
                    return
                else:
                    for c1 in self.constraints:
                        if c1.v1 in [c.v1, c.v2] or c1.v2 in [c.v1, c.v2]:
                            queue.append(c1)

    def backtracking_search(self):
        start = deepcopy(self)
        curr = start
        stack = [start]
        while not curr.is_satisfied():
            curr = stack.pop(0)
            curr.enforce_arc_consistency()
            if not curr.can_be_satisfied():
                continue
            stack = curr.neighbors() + stack
        if not curr.is_satisfied():
            raise ValueError("could not satisfy all constraints")
        self.variables = curr.variables
        self.constraints = curr.constraints

