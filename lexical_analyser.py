import re
from collections import defaultdict

# Token types and their regex patterns
token_patterns = [
    ('KEYWORD', r'\b(if|else|while|for|return|int|float)\b'),
    ('IDENTIFIER', r'[a-zA-Z_]\w*'),
    ('CONSTANT', r'\d+(\.\d+)?'),
    ('LITERAL', r'"[^"]*"'),
    ('OPERATOR', r'[+\-*/%]'),
    ('ASSIGN', r'='),
    ('PUNCTUATOR', r'[;,\(\)\{\}]')
]

def tokenize(code):
    tokens = []
    position = 0

    while position < len(code):
        if code[position].isspace():
            position += 1
            continue

        match_found = False
        for token_type, pattern in token_patterns:
            regex = re.compile(pattern)
            match = regex.match(code, position)
            if match:
                value = match.group(0)
                tokens.append((token_type, value))
                position = match.end()
                match_found = True
                break

        if not match_found:
            print(f"Invalid character at position {position}: {code[position]}")
            break

    return tokens

# Example usage
input_code = input("Enter code: ")
result = tokenize(input_code)

# Group tokens by type
grouped_tokens = defaultdict(list)
for token_type, value in result:
    grouped_tokens[token_type].append(value)

# Display grouped tokens
print("\n=== Token Summary ===")
for token_type, values in grouped_tokens.items():
    unique_values = list(dict.fromkeys(values))  # Remove duplicates while preserving order
    print(f"{token_type}: {', '.join(unique_values)}")