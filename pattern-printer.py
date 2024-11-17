import sys
from math import gcd
from functools import reduce
import subprocess
import importlib
import os

def import_module(module_name):
    # Import module
    print(f"-------------------------------------------------------------")
    print(f"Reading pattern information from module:...")
#    print(f"-------------------------------------------------------------")

    try:
        # Dynamically import the specified module
        module = importlib.import_module(module_name)
        print(f"---✅ found pattern module {module}.")
    except ModuleNotFoundError:
        print(f"""
        Error: Cannot find the pattern file '{module_name}'.
        Please check:
        1. The file exists in this folder
        2. The filename is spelled correctly
        3. The file ends with .py
        """)
        sys.exit(1)

    try:
        pattern_name = module.pattern_name
        print(f"---✅ Found pattern name: '{pattern_name}.'")
    except AttributeError:
        pattern_name = module_name
        print(f"Pattern name not found in module {module_name}. Defaulting to name: {module_name}")

    # Access the pattern from the imported module
    try:
        pattern = module.pattern
        print("---✅ Imported pattern from module.")
    except AttributeError:
        print(f"Error: Your pattern file '{module_name}' is missing does not contain list 'pattern'. The pattern list is required to instruct me how the panels should be assembled. Exiting...")
        sys.exit(1)

    # Access the stitch dictionary from the imported module
    stitch_dictionary = {}  # Default to an empty dictionary
    try:
        stitch_dictionary = module.stitch_dictionary
        print("---✅ Imported stitch dictionary from module.")
    except AttributeError:
        print(f"Error: Module '{module_name}' does not contain list 'Stitch Dictionary'. No stitch dictionary documents will be output.")
    print(f"-------------------------------------------------------------")
    print(f"Checking all pattern panels present...")
#    print(f"-------------------------------------------------------------")
    for panel_name in pattern:
        if not hasattr(module, panel_name):
            print(f"Error: could not find {panel_name}. Please check all panels are present and correct in the pattern module.")
            sys.exit(1)
        else:
            print(f"   -✅ {panel_name} found.")

    print(f"---✅ All panels imported.")
    print(f"-------------------------------------------------------------")
    print("Evaluating row lengths:")
#    print(f"-------------------------------------------------------------")
    pattern_lengths = {name: len(getattr(module, name)) for name in pattern}
    for panel_name, length in pattern_lengths.items():
        print(f"      - {panel_name}: {length} rows")

    return module, pattern_name, pattern, stitch_dictionary


# Function to get all list names from the imported module
def get_list_names_from_module(module):
    return [name for name, obj in module.__dict__.items() if isinstance(obj, list)]

# Least common multiple function for lists
def lcm(a, b):
    return a * b // gcd(a, b)

def lcm_of_lists(*lists):
    list_lengths = [len(lst) for lst in lists]
    return reduce(lcm, list_lengths)

# Function to write a stitch dictionary document
def print_stitch_dictionary(stitch_dict,file_name):
    with open(file_name, 'w') as f:
        # Write the header row (Pattern panel names)
        f.write("| Abbreviation | Instructions |\n")
        f.write("|---|--------------|\n")  # Divider row
        
        # Write each row
        for abbr,instr in stitch_dict.items():
            #f.write(f"| **{abbr}** | {instr} |\n")
             f.write(f"| **{escape_markdown_specials(abbr)}** | {escape_markdown_specials(instr)} |\n")
#             f.write(" |——————————|————————————————————————————————————|\n")


def escape_markdown_specials(text):
    # Replace `|`, `\`, and `/` with escaped versions
    return text.replace('|', r'\|').replace('/', r'\/')

def setup_pattern_output_files(pattern_name):
    # Create a folder for outputs
    print(f"-------------------------------------------------------------")
    print(f"Setting up output files:")
#    print(f"-------------------------------------------------------------")

    output_dir = pattern_name
    print(f"---ℹ️ The output will be saved in the following directory: {output_dir}")
    os.makedirs(output_dir, exist_ok=True)
    #TODO:sanitise whitespace from pattern name when creating output dir name.
    print(f"---✅ Output directory set up.")

    # Return all file paths we'll need
    return {
        'output_dir': output_dir,
        'markdown_table': os.path.join(output_dir, f"{pattern_name}_table.md"),
        'html_table': os.path.join(output_dir, f"{pattern_name}_table_html.html"),
        'pdf_table': os.path.join(output_dir, f"{pattern_name}_table_pdf.pdf"),
        'markdown_plain': os.path.join(output_dir, f"{pattern_name}_plain.md"),
        'html_plain': os.path.join(output_dir, f"{pattern_name}_plain_html.html"),
        'pdf_plain': os.path.join(output_dir, f"{pattern_name}_plain_pdf.pdf"),
        'epub': os.path.join(output_dir, f"{pattern_name}_ebook.epub"),
        'stitch_dictionary_markdown' : os.path.join(output_dir, f"{pattern_name}_stitch_dictionary.md"),
        'stitch_dictionary_pdf' : os.path.join(output_dir, f"{pattern_name}_stitch_dictionary_pdf.pdf"),
        'stitch_dictionary_html' : os.path.join(output_dir, f"{pattern_name}_stitch_dictionary_html.html"),
        'stitch_dictionary_epub' : os.path.join(output_dir, f"{pattern_name}_stitch_dictionary_ebook.epub")
    }

def calculate_total_rows():
    # Calculate the total rows to cycle through (LCM of list lengths)
#    print("-------------------------------------------------------------")
    print("Calculating total rows required to cycle through all panels...")
#    print("-------------------------------------------------------------")
    lists_to_cycle = [getattr(module, name) for name in pattern]
    total_rows = lcm_of_lists(*lists_to_cycle)
    if total_rows > 200:
        print(f"The number of rows in the pattern do not divide evenly, which can lead to large outputs. The current configuration of panels will not repeat for {total_rows} rows.")
        while True:
            try:
                user_input = input(f"If you don't want to print all {total_rows} rows, enter a different number of total rows to print here (or just press enter to print all {total_rows}): ").strip()
                rows_to_print = int(user_input) if user_input else total_rows
                print(f"---✅ Selected {rows_to_print} rows to print.")
                if rows_to_print <= 0:
                    raise ValueError("Row count must be positive.")
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again. ")
    else:
            rows_to_print = total_rows
    return(rows_to_print)

# Function to cycle through panel patterns based on the provided pattern
def write_pattern_tabular(module, pattern, file_name, rows_to_print, pattern_name):
    # Open the file to write the markdown table
    print("-------------------------------------------------------------")
    print(f"Creating tabular pattern - iterating through pattern...")
#    print(f"-------------------------------------------------------------")
    lists_to_cycle = [getattr(module, name) for name in pattern]
    with open(file_name, 'w') as f:
    #    # write yaml properties
    #    f.write("---\ntable-use-row-colors: true\n---\n")
        # Write the header row (Pattern panel names)
        f.write(f"# {pattern_name} \n \n")
        f.write(" | **ROW #** | **" + " **| **".join(pattern) + "**| \n")
        f.write(" |--|-" + " | ".join(["-------------------------------------------------------------"] * len(pattern)) + "| \n")  # Divider row
        # Write each row
        for i in range(rows_to_print):
            row = [escape_markdown_specials(lst[i % len(lst)]) for lst in lists_to_cycle]
            f.write(f" | **{i + 1}** | " + " | ".join(row) + " | \n")
            #row = [lst[i % len(lst)] for lst in lists_to_cycle]  # Cycle through each list
            #f.write(f" | **{i + 1}** | " + " | ".join(row) + " | \n")
            f.write(" |——|—" + " | ".join(["——————"] * len(pattern)) + "| \n")  # Divider row


def write_pattern_plaintext(module, pattern, file_name, rows_to_print, pattern_name):
    # Fetch the lists from the module according to the pattern
    # Open the file to write the markdown table
    print(f"-------------------------------------------------------------")
    print(f"Creating plaintext pattern - iterating through pattern...")
#    print(f"-------------------------------------------------------------")
    lists_to_cycle = [getattr(module, name) for name in pattern]
    with open(file_name, 'w') as g:
        g.write(f"# {pattern_name} \n \n")
        # Write each row
        for i in range(rows_to_print):
            g.write(f"# Row {i + 1}\n\n")  # Output row number

            # Cycle through each list and write in the specified format
            for j, lst in enumerate(lists_to_cycle):
                variable_name = pattern[j]  # Get the panel variable name from the pattern
                content = escape_markdown_specials(lst[i % len(lst)])  # Get the content for the row

                # Write the content in the markdown list format
                g.write(f"- **{variable_name}**: {content}\n")

            # Add a newline after each row for clarity
            g.write("\n")


########
# MAIN #
########

if len(sys.argv) != 2:
    print("Usage: python3 pattern-printer.py module_name, where 'module_name' is the name of a pattern file containing pattern name, pattern structure, and the panels to be printed")
    sys.exit(1)

# Get module name containing pattern instructions from command-line arguments
module_name = sys.argv[1]

module, pattern_name, pattern, stitch_dictionary = import_module (module_name)

# Calculate the total rows to cycle through (based on LCM of list lengths)
rows_to_print = calculate_total_rows()
print(f"---ℹ️ The output will be a repeatable pattern of {rows_to_print} rows.")
files = setup_pattern_output_files(pattern_name)

# Create plaintext patterns (markdown)
write_pattern_tabular(module, pattern, files['markdown_table'], rows_to_print, pattern_name)
print (f"---✅ Generated tabular pattern: {files['markdown_table']}")
write_pattern_plaintext(module, pattern, files['markdown_plain'], rows_to_print, pattern_name)
print (f"---✅ Generated plaintext pattern: {files['markdown_plain']}")

#For Now, Spaghetti to convert to a bunch of formats:
#TODO when I have time, switch fro this bunch of OS commands to use python library: https://github.com/boisgera/pandoc, but that seems to work quite differently so let's get this working for now.
print(f"-------------------------------------------------------------")
print(f"Converting markdown to various output formats:")
#print(f"-------------------------------------------------------------")

# PDF TABLE
try:
    subprocess.run(
        ['pandoc', files['markdown_table'], '-o', files['pdf_table'], '-V', 'papersize=A3', '-V', 'geometry:margin=0.5in', '-V', 'geometry:portrait'],
        check=True
    )
    print(f"---✅ Tabular PDF created:  {files['pdf_table']}.")
except subprocess.CalledProcessError as e:
    print(f"⚠️ Tabular PDF: Error during Pandoc conversion to PDF table: {e}")

# HTML TABLE
try:
    subprocess.run(
        ['pandoc', files['markdown_table'], '-o', files['html_table'], '--metadata', f'title=\"{pattern_name} - Table Pattern\"'],
        check=True
    )
    print(f"---✅ Tabular HTML created:  {files['html_table']}")
except subprocess.CalledProcessError as e:
    print(f"⚠️ Tabular HTML: Error during Pandoc conversion to HTML Table: {e}")

# Plain PDF pages
try:
    subprocess.run(
        ['pandoc', files['markdown_plain'], '-o', files['pdf_plain'], '-V', 'papersize=A4', '-V', 'geometry:margin=0.5in', '-V', 'geometry:portrait'],
        check=True
    )
    print(f"---✅ PDF A4 created:  {files['pdf_plain']}.")
except subprocess.CalledProcessError as e:
    print(f"⚠️ PDF A4: Error during Pandoc conversion to PDF paginated format: {e}")

# PLAIN HTML
try:
    subprocess.run(
        ['pandoc', files['markdown_plain'], '-o', files['html_plain'], '--metadata', f'title="{pattern_name} - Text Pattern"'],
        check=True
    )
    print(f"---✅ HTML created:  {files['html_plain']}.")
except subprocess.CalledProcessError as e:
    print(f"⚠️ HTML: Error during Pandoc conversion to HTML: {e}")

# EPUB
try:
    subprocess.run(
        ['pandoc', files['markdown_plain'], '-o', files['epub'], '--metadata', f'title="{pattern_name} - Pattern"'],
        check=True
    )
    print(f"---✅ Ebook created:  {files['epub']}.")
except subprocess.CalledProcessError as e:
    print(f"⚠️ EPUB: Error during Pandoc conversion to EPUB: {e}")

# Print the stitch dictionary to various outputs, if it exists.

if not stitch_dictionary:
        print("ℹ️  No stitch dictionary will be generated (stitch dictionary not present in the input file, or empty).")
else:
    print(f"-------------------------------------------------------------")
    print("Creating stitch dictionary...")
#    print(f"-------------------------------------------------------------")
    try:
        print_stitch_dictionary(stitch_dictionary, files['stitch_dictionary_markdown'])
        print(f"---✅ Stitch dictionary table created: {files['stitch_dictionary_markdown']}")
    except Exception as e:
        print(f"⚠️ Error creating stitch dictionary: {e}")

#Stitch Dic PDF Table

    try:
        subprocess.run(
            ['pandoc', files['stitch_dictionary_markdown'], '-o', files['stitch_dictionary_pdf'], '-V', 'papersize=A4', '-V', 'geometry:margin=1in', '-V', 'geometry:portrait'],
            check=True
        )
        print(f"---✅ Stitch Dictionary PDF created:  {files['stitch_dictionary_pdf']}")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Stitch Dictionary PDF: Error during Pandoc conversion: {e}")

    # Stitch Dic HTML Table
    try:
        subprocess.run(
            ['pandoc', files['stitch_dictionary_markdown'], '-o', files['stitch_dictionary_html'], '--metadata', f'title="{pattern_name} - Dictionary"'],
            check=True
        )
        print(f"---✅ Stitch Dictionary HTML created:  {files['stitch_dictionary_html']}")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Stitch Dictionary HTML: Error during Pandoc conversion: {e}")

    # Stich Dic Epub

    try:
        subprocess.run(
            ['pandoc', files['stitch_dictionary_markdown'], '-o', files['stitch_dictionary_epub']],
            check=True
        )
        print(f"---✅ Stitch Dictionary PDF created:  {files['stitch_dictionary_epub']}")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Stitch Dictionary PDF: Error during Pandoc conversion: {e}")
