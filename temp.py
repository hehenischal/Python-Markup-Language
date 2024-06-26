import re

def parse_cppml_to_html(input_file, output_file):
    with open(input_file, 'r') as f_in:
        input_text = f_in.read()

    output = []
    tag_stack = []

    # Define regex patterns for parsing tags, attributes, and content
    tag_pattern = re.compile(r'(\w+)<\s*([^<]*)\s*<\s*"([^"]*)"\s*')  # Standard tag with attributes and content
    self_closing_tag_pattern = re.compile(r'(\w+)<<\s*([^<]*)\s*<*\s*>>')  # Self-closing tag with attributes

    # Self-closing tags in HTML
    self_closing_tags = {'br', 'hr', 'img', 'input', 'link', 'meta', 'area', 'base', 'col',
                         'command', 'embed', 'keygen', 'param', 'source', 'track', 'wbr'}

    # Function to parse properties from attributes string
    def parse_properties(properties_str):
        properties = re.findall(r'(\w+)=?"([^"]*)"', properties_str)
        formatted_properties = ' '.join([f'{prop}="{value}"' if value else prop for prop, value in properties])
        return formatted_properties

    lines = input_text.splitlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check for standard tag pattern
        match = tag_pattern.match(line)
        if match:
            tag = match.group(1)
            properties_content = match.group(2).strip()
            content = match.group(3).strip()

            # Parse properties
            properties = parse_properties(properties_content)

            if tag in self_closing_tags:
                output.append(f'<{tag} {properties} />')
            else:
                output.append(f'<{tag} {properties}>{content}')
                tag_stack.append(tag)
            continue

        # Check for self-closing tag pattern
        match = self_closing_tag_pattern.match(line)
        if match:
            tag = match.group(1)
            properties_content = match.group(2).strip()

            # Parse properties
            properties = parse_properties(properties_content)

            output.append(f'<{tag} {properties} />')
            continue

        # Check for end tag marker >>
        if line.startswith('>>'):
            while tag_stack:
                last_open_tag = tag_stack.pop()
                output.append(f'</{last_open_tag}>')
            continue

    # Write output to file
    with open(output_file, 'w') as f_out:
        f_out.write('\n'.join(output))

    print(f'Conversion complete. Output written to {output_file}')

# Example usage
parse_cppml_to_html('input.cppml', 'output.html')
