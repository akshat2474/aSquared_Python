import sys
from lexer import Lexer
from parser import Parser

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python asquared.py <script>", file=sys.stderr)
        sys.exit(1)

    try:
        with open(sys.argv[1], 'r') as f:
            source = f.read()
        tokens = Lexer(source).tokenize()
        Parser(tokens).parse_and_execute()
    except FileNotFoundError:
        print(f"Error: File not found: {sys.argv[1]}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)
