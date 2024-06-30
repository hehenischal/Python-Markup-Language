import argparse
import subprocess

def tokenize(input_string):
    input_string = input_string.replace('\n', '')  
    tokens = []
    buffer = ""

    i = 0
    while i < len(input_string):
        if input_string[i:i+2] in ("<<", ">>"):
            if buffer:
                tokens.append(buffer.strip())
                buffer = ""
            tokens.append(input_string[i:i+2])
            i += 2
        elif input_string[i] == '<':
            j = i + 1
            while j < len(input_string) and input_string[j] != '>':
                if input_string[j] == '<':
                    nested_tag = tokenize(input_string[j:])
                    tokens.extend(nested_tag)
                    i = j + len(''.join(nested_tag))  
                    break
                j += 1
            if j < len(input_string) and input_string[j] == '>':
                tokens.append(input_string[i:j + 1])
                i = j + 1
            else:
                tokens.append(input_string[i:])
                break
        else:
            buffer += input_string[i]
            i += 1
    
    if buffer:
        tokens.append(buffer.strip())

    return tokens

def convert_custom_html_to_html(input_string):
    tokens = tokenize(input_string)
    html = ''.join(tokens)
    return html



def main():
    parser = argparse.ArgumentParser(description='Convert custom CPP-like syntax to standard HTML and format it.')
    parser.add_argument('input_file', type=str, help='Path to the input file')
    parser.add_argument('output_file', type=str, help='Path to the output file')

    args = parser.parse_args()
    print(f"Input file: {args.input_file}")
    print(f"Output file: {args.output_file}")

    with open(args.input_file, 'r') as f:
        input_text = f.read()
        print("Input text:")
        print(input_text)

    converted_html = convert_custom_html_to_html(input_text)
    formatted_html = converted_html

    with open(args.output_file, 'w') as f:
        f.write(formatted_html)

if __name__ == '__main__':
    main()
