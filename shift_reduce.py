import re

class ShiftReduceParser:
    def __init__(self, grammar, start_symbol):
        self.grammar = grammar
        self.start_symbol = start_symbol
        self.stack = ['$']
        self.input_string = []
        self.history = []

    def shift(self):
        """Shift operation: Move symbol from input buffer to stack"""
        if self.input_string:
            self.stack.append(self.input_string.pop(0))
            self.history.append(("Shift", list(self.stack), list(self.input_string)))

    def reduce(self):
        """Reduce operation: Apply grammar rules and print applied rule"""
        for lhs, rhs_list in self.grammar.items():
            for rhs in rhs_list:
                if self.stack[-len(rhs):] == rhs:
                    # **FIX: Replace Unicode → with ASCII ->**
                    print(f"{''.join(self.stack):<15}{''.join(self.input_string):<20}{'Reducing (' + lhs + ' -> ' + ' '.join(rhs) + ')'}")
                    self.stack[-len(rhs):] = [lhs]  # Replace RHS with LHS
                    self.history.append(("Reduce", list(self.stack), list(self.input_string)))
                    return True
        return False  # No reduction possible

    def backtrack(self):
        """Backtrack operation: Revert to previous state if dead-end"""
        while self.history:
            operation, prev_stack, prev_input = self.history.pop()
            if operation == "Reduce":
                self.stack = prev_stack
                self.input_string = prev_input
                return True
        return False

    def tokenize(self, input_string):
        """Tokenize input to avoid splitting 'id' into characters"""
        return re.findall(r'id|\+|\*|\(|\)|\$', input_string)

    def parse(self, input_string):
        """Perform shift-reduce parsing"""
        self.stack = ['$']
        self.input_string = self.tokenize(input_string) + ['$']
        print(f"{'Stack':<15}{'Input':<20}{'Operation'}")
        print("-" * 60)

        while True:
            if self.input_string:
                print(f"{''.join(self.stack):<15}{''.join(self.input_string):<20}{'Shifting'}")
                self.shift()

            reduced = True
            while reduced:
                reduced = self.reduce()

            if self.stack == ['$'] + [self.start_symbol] and self.input_string == ['$']:
                print(f"{''.join(self.stack):<15}{''.join(self.input_string):<20}{'Accept'}")
                return

            if not self.input_string and not self.reduce():
                print("------------ Backtracking ------------")
                if not self.backtrack():
                    print("Parsing failed!")
                    return


# Define grammar
grammar = {
    'E': [['E', '+', 'T'], ['T']],
    'T': [['T', '*', 'F'], ['F']],
    'F': [['(', 'E', ')'], ['id']]
}

# Create parser and parse input
parser = ShiftReduceParser(grammar, 'E')
parser.parse("id*id")