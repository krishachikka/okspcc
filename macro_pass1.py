# Macro Processor - Pass 1

# Input Program
source_program = [
    "MACRO", 
    "KRIS &arg1, &arg2", 
    "A1, &arg1", 
    "A2, &arg2",
    "MEND", 
    "KRIS data1, data2", 
    "data1 DC f'5'", 
    "data2 DC f'3'"
]

# Data Structures for Pass 1
MNT = []    # Macro Name Table
MDT = []    # Macro Definition Table
ALA = []    # Argument List Array

# Pointers for MNT and MDT
MNTC = 0     # Macro Name Table Counter
MDTC = 0     # Macro Definition Table Counter
processing_macro = False  # Flag to check if we are inside a macro definition

# Step 1: Initialize MDTC and MNTC
def process_macro(source_program):
    global MNTC, MDTC, processing_macro
    macro_name = None
    parameters = []

    # Step 2: Read each statement of the source program
    for line in source_program:
        line = line.strip()

        # Step 3: Check for MACRO keyword (start of macro definition)
        if line == "MACRO":
            processing_macro = True
            continue  # Skip this line, as we are defining a macro
            
        # Step 4: Macro definition line (e.g., KRIS &arg1, &arg2)
        if processing_macro and line.startswith("KRIS"):
            parts = line.split(" ", 1)
            macro_name = parts[0]
            params = parts[1].strip().split(",")  # Get parameters
            params = [p.strip().lstrip('&') for p in params]  # Remove '&' from arguments
            ALA.append({i: param for i, param in enumerate(params)})  # Create Argument List Array with indices starting from #0
            MDT.append((MDTC, line))  # Add the macro definition line to MDT
            MDTC += 1
            continue
        
        # Step 5: Store macro body in MDT (just store the macro body lines)
        if processing_macro:
            if line == "MEND":
                # MEND marks the end of the macro definition
                MNT.append((MNTC, macro_name, MDTC))  # Store in MNT
                MDT.append((MDTC, line))  # Add MEND to MDT
                MDTC += 1  # Move MDT counter to next index
                processing_macro = False  # Reset processing flag after MEND
                continue
            else:
                # Replace the argument names with their respective indices in the MDT
                for i in range(len(ALA[-1])):
                    line = line.replace(f"&{ALA[-1][i]}", f"#{i}")  # Replace with #index notation
                MDT.append((MDTC, line))  # Add modified line to MDT
                MDTC += 1

# Process the input program and populate MNT, MDT, ALA
process_macro(source_program)

# Output the result
print(f"{'Index':<10}{'Macro Name':<15}{'Address':<10}")
print("-" * 35)
for entry in MNT:
    print(f"{entry[0]:<10}{entry[1]:<15}{entry[2]:<10}")

print() 

print(f"{'Index':<10}{'Definition'}")
print("-" * 35)
for entry in MDT:
    print(f"{entry[0]:<10}{entry[1]}")

print()

print(f"{'Arguments'}")
print("-" * 35)
for entry in ALA:
    print(f"{entry}")