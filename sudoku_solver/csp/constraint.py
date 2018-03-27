class Constraint:
    def __init__(self, v1, v2, f):
        self.v1 = v1
        self.v2 = v2
        self.f = f

    def is_satisfied(self):
        if self.v1.is_assigned() and self.v2.is_assigned():
            return self.f(self.v1.value(), self.v2.value())
        return False

    def can_be_satisfied(self):
        if not self.v1.is_assigned() or not self.v2.is_assigned():
            for value_1 in self.v1.domain:
                for value_2 in self.v2.domain:
                    if self.f(value_1, value_2):
                        return True
            return False
        else:
            return self.is_satisfied()
