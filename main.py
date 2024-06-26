import re
import argparse
import io

def convert_cpp_to_html(input_text):
    custom_tag_pattern = re.compile(r'(\w+)<\s*\'([^\']*)\<\s*(.*?)\s*\>\>')

    def parse_properties(properties_str):
        print("parse_properties called")
        properties = re.findall(r'(\w+)=([^"\s]*)', properties_str)
        formatted_properties = ' '.join([f'{prop}="{value}"' for prop, value in properties])
        return formatted_properties

    def parse_content(content):
        print("parse_content called")
        output = []
        pos = 0
        while pos < len(content):
            custom_match = custom_tag_pattern.match(content, pos)
            if custom_match:
                tag = custom_match.group(1)
                properties_content = custom_match.group(2).strip()
                inner_content = custom_match.group(3).strip()
                properties = parse_properties(properties_content)

                output.append(f'<{tag} {properties}>{parse_content(inner_content)}</{tag}>')
                pos = custom_match.end()
                continue

            pos += 1  # Move to next character if no match

        if not output:
            output.append(content.strip())

        return ''.join(output)

    output = []
    lines = input_text.splitlines()
    print("lines:", lines)
    for line in lines:
        # Check for custom tag
        custom_match = custom_tag_pattern.match(line)
        if custom_match:
            tag = custom_match.group(1)
            properties_content = custom_match.group(2).strip()
            inner_content = custom_match.group(3).strip()
            properties = parse_properties(properties_content)

            output.append(f'<{tag} {properties}>{parse_content(inner_content)}</{tag}>')

    return '\n'.join(output)

def main():
    print("Script started")
    
    parser = argparse.ArgumentParser(description='Convert CPP-like code snippets to HTML-like snippets.')
    parser.add_argument('input_file', type=str, help='Path to the input file')
    parser.add_argument('output_file', type=str, help='Path to the output file')

    args = parser.parse_args()
    print(f"Input file: {args.input_file}")
    print(f"Output file: {args.output_file}")

    with open(args.input_file, 'r') as f:
        input_text = f.read()
        print("Input text:")
        print(input_text)

    converted_text = convert_cpp_to_html(input_text)

    output_buffer = io.StringIO()
    output_buffer.write(converted_text)

    with open(args.output_file, 'w') as f:
        f.write(output_buffer.getvalue())

    print("Output:")
    print(converted_text)
    print(f'Conversion complete. Output written to {args.output_file}')
    print("Script finished")

if __name__ == '__main__':
    main()