class Optimizer:
    def __init__(self):
        # Stores variables with their constant values for propagation
        self.variables = {}

        # Keeps track of variables that are actually used (for dead code elimination)
        self.used_variables = set()

        # Stores already seen expressions for common subexpression elimination
        self.expression_map = {}

    def evaluate_expression(self, expr):
        """
        Evaluates simple arithmetic expressions with constants or known variables.
        If the expression is fully evaluable (e.g., '5 * 3'), it returns the result.
        If partial (e.g., '5 * x' where x is known), it substitutes and evaluates.
        """
        parts = expr.split()
        if len(parts) == 3:
            op1, operator, op2 = parts
            # Case 1: both operands are digits
            if op1.isdigit() and op2.isdigit():
                return str(eval(f"{op1} {operator} {op2}"))
            # Case 2: one operand is a digit and the other is a known constant variable
            if op1.isdigit() and op2 in self.variables:
                return str(eval(f"{op1} {operator} {self.variables[op2]}"))
            if op2.isdigit() and op1 in self.variables:
                return str(eval(f"{self.variables[op1]} {operator} {op2}"))
        # Return unchanged if the expression can't be folded
        return expr

    def constant_propagation(self, var, value):
        """
        Stores the variable if it is assigned a constant value.
        This allows replacing variable references later.
        """
        if value.isdigit():
            self.variables[var] = value

    def common_subexpression_elimination(self, code):
        """
        Eliminates repeated expressions by mapping them to a previously computed variable.
        If the same expression is seen again, reuse the previous variable.
        """
        new_code = []
        for line in code:
            if '=' in line:
                var, expr = map(str.strip, line.split('='))
                if expr in self.expression_map:
                    # Expression already seen, use the mapped variable instead
                    new_code.append(f"{var} = {self.expression_map[expr]}")
                else:
                    # First time seeing this expression, store its mapping
                    self.expression_map[expr] = var
                    new_code.append(line)
            else:
                new_code.append(line)
        return new_code

    def dead_code_elimination(self, code):
        """
        Removes assignments to variables that are never used later in the code.
        Keeps lines only if the variable is in the used set.
        """
        return [line for line in code if '=' not in line or line.split('=')[0].strip() in self.used_variables]

    def loop_optimization(self, code):
        """
        Placeholder for loop optimization.
        Currently removes lines with basic loop constructs ('for', 'while').
        """
        return [line for line in code if 'for' not in line and 'while' not in line]

    def optimize(self, code):
        """
        The main optimization workflow.
        Applies:
        1. Constant Folding
        2. Constant Propagation
        3. Common Subexpression Elimination
        4. Dead Code Elimination
        5. Basic Loop Optimization
        """
        optimized = []

        # Step 1 & 2: Constant Folding and Propagation
        for line in code:
            line = line.strip()
            if not line:
                continue  # Skip blank lines

            if '=' in line:
                var, expr = map(str.strip, line.split('='))
                expr = self.evaluate_expression(expr)  # Try folding constants
                self.constant_propagation(var, expr)   # Propagate constant values
                self.used_variables.add(var)           # Track variable as used
                optimized.append(f"{var} = {expr}")
            else:
                # Non-assignment lines (e.g., loop lines) are added directly
                optimized.append(line)

        # Step 3: Eliminate redundant expressions
        optimized = self.common_subexpression_elimination(optimized)

        # Step 4: Remove code that doesn't affect output
        optimized = self.dead_code_elimination(optimized)

        # Step 5: Placeholder loop optimization
        optimized = self.loop_optimization(optimized)

        return optimized


# Sample input code with some optimization opportunities
input_code = [
    "a = 5 * 3",     # Can be folded to a = 15
    "b = a + 4",     # Depends on a (constant propagation possible)
    "c = b - 3",     # Depends on b
    "d = c * 2",     # Depends on c
    "e = a + 4",     # Same as b's expression, can be optimized (common subexpression)
]

# Create an optimizer instance
optimizer = Optimizer()

# Run the optimizer
optimized_code = optimizer.optimize(input_code)

# Print the optimized result
print("\nOptimized Code:")
for line in optimized_code:
    print(line)