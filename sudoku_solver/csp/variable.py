class Variable:
    def __init__(self, domain=set()):
        if not isinstance(domain, set):
            raise ValueError("Domain must be a set!")
        self.domain = domain

    def add_to_domain(self, value):
        self.domain.add(value)

    def remove_from_domain(self, value):
        self.domain.remove(value)

    def assign(self, value):
        if value not in self.domain:
            raise ValueError("that value isn't in the domain for this variable")
        self.domain = { value }

    def is_assigned(self):
        return len(self.domain) == 1

    def value(self):
        if not self.is_assigned():
            raise ValueError()
        return list(self.domain)[0]

