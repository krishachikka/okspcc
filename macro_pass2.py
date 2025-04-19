# Pass 1 Output (MNT, MDT, ALA) from previous code
MNT = [
    (0, 'KRIS', 3)  # Format: (index, macro_name, address in MDT)
]

MDT = [
    (0, "KRIS &arg1, &arg2"),  # Macro definition header
    (1, "A1, #0"),              # Macro body: replace #0 with argument 1
    (2, "A2, #1"),              # Macro body: replace #1 with argument 2
    (3, "MEND")                 # End of macro definition
]

ALA = [
    {0: 'arg1', 1: 'arg2'}  # Argument list for macro 'KRIS'
]

# Complete source program from Pass 1 (both macro definition and invocation)
source_program_pass2 = [
    "MACRO", 
    "KRIS &arg1, &arg2", 
    "A1, &arg1", 
    "A2, &arg2",
    "MEND", 
    "KRIS data1, data2",  # Macro invocation with arguments
    "data1 DC f'5'",       # Data declaration
    "data2 DC f'3'"        # Data declaration
]

# Helper function to perform macro expansion during Pass 2
def expand_macros(source_program):
    expanded_program = []

    # Step 1: Iterate through each line in the source program
    for line in source_program:
        line = line.strip()

        # Step 2: Check if the line is part of a macro definition (skip those lines in output)
        if line.startswith("MACRO") or line.startswith("MEND"):
            continue  # Skip macro definition lines in output

        # Step 3: Check if the line contains a macro invocation (e.g., "KRIS data1, data2")
        for mnt_entry in MNT:
            macro_name = mnt_entry[1]  # Extract macro name (e.g., 'KRIS')
            macro_start_index = mnt_entry[2]  # The address where the macro starts in MDT

            if line.startswith(macro_name):  # If macro invocation is found
                # Extract arguments passed during macro invocation (e.g., 'data1, data2')
                arguments = line[len(macro_name):].strip().split(",")
                arguments = [arg.strip() for arg in arguments]  # Clean up arguments

                # Step 4: Find the corresponding macro definition in MDT
                macro_expansion = []
                for i in range(macro_start_index, len(MDT)):
                    mdt_entry = MDT[i]

                    if mdt_entry[1] == "MEND":
                        break  # End of the macro definition
                    else:
                        # Substitute the parameters in the macro body
                        line_expansion = mdt_entry[1]
                        # Substitute all parameters (e.g., #0, #1) with the actual arguments
                        for index, argument in enumerate(arguments):
                            line_expansion = line_expansion.replace(f"#{index}", argument)  # Replace #0, #1, etc. with arguments
                        
                        macro_expansion.append(line_expansion)

                # Add the expanded macro lines to the expanded program
                expanded_program.extend(macro_expansion)
                break  # Proceed to the next line after handling a macro invocation

        else:  # If no macro invocation found, just add the line as-is (e.g., data declarations)
            expanded_program.append(line)

    return expanded_program

# Expand the source program using Pass 2 logic
expanded_program = expand_macros(source_program_pass2)

# Output the expanded program (Post-Pass 2)
print("Expanded Program after Pass 2:")
for line in expanded_program:
    print(line)