#!/usr/bin/env python3
import json
import sys
import argparse

def format_graphql(json_str, indent=2):
    """
    Format a GraphQL JSON string into a properly indented GraphQL-like structure.

    Usage Instructions:
    1. Save this script as `format_graphql.py`.
    2. Run the script from the command line:
       - To format a GraphQL JSON string from a file:
         ```bash
         python format_graphql.py input.json
         ```
       - To display usage help:
         ```bash
         python format_graphql.py --help
         ```
       - To use the default sample input:
         ```bash
         python format_graphql.py
         ```
    3. Module Usage in Python:
       ```python
       from format_graphql import format_graphql
       json_input = '{"data":{"key":"value"}}'
       formatted = format_graphql(json_input, indent=2)
       print(formatted)
       ```
    4. Input Requirements:
       - The input must be a valid JSON string representing a GraphQL response.
       - Invalid JSON will return an error message.
    5. Customization:
       - Adjust the `indent` parameter to change the number of spaces per indentation level (default is 2).
    6. Output:
       - The formatted output is a string with proper GraphQL-like indentation, suitable for readability.
       - Strings are quoted unless they are URNs or identifiers (e.g., `urn:li:...` or types with colons).

    Args:
        json_str (str): The input JSON string to format.
        indent (int): Number of spaces for each indentation level (default: 2).

    Returns:
        str: Formatted GraphQL string or an error message if JSON is invalid.
    """
    try:
        # Parse the JSON string into a Python object
        data = json.loads(json_str)
        return format_value(data, indent_level=0, indent_size=indent)
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON input - {str(e)}"

def format_value(value, indent_level, indent_size):
    """
    Recursively format a value (dict, list, or primitive) into GraphQL-like structure.

    Args:
        value: The value to format (dict, list, str, int, bool, etc.).
        indent_level (int): Current indentation level.
        indent_size (int): Number of spaces per indentation level.

    Returns:
        str: Formatted string representation of the value.
    """
    indent = " " * (indent_level * indent_size)

    if isinstance(value, dict):
        if not value:
            return "{}"
        lines = ["{"]
        for key, val in value.items():
            formatted_val = format_value(val, indent_level + 1, indent_size)
            lines.append(f"{indent}{' ' * indent_size}{key}: {formatted_val}")
        lines.append(f"{indent}}}")
        return "\n".join(lines)

    elif isinstance(value, list):
        if not value:
            return "[]"
        lines = ["["]
        for item in value:
            formatted_item = format_value(item, indent_level + 1, indent_size)
            lines.append(f"{indent}{' ' * indent_size}{formatted_item},")
        lines.append(f"{indent}]")
        return "\n".join(lines)

    elif isinstance(value, str):
        # Enclose strings in quotes unless they are URNs or specific identifiers
        if value.startswith("urn:") or ":" in value and not value.startswith('"'):
            return value
        return f'"{value}"'

    elif value is None:
        return "null"

    elif isinstance(value, bool):
        return str(value).lower()

    else:
        return str(value)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Format a GraphQL JSON string into a properly indented GraphQL-like structure.",
        epilog="""Examples:
  %(prog)s                     # Use default sample input
  %(prog)s input.json          # Read from file
  echo '{}' | %(prog)s -       # Read from stdin
  %(prog)s - < input.json      # Read from stdin (redirect)
  %(prog)s -                   # Read from stdin (paste JSON, then Ctrl+D)""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        help="Path to JSON file, or '-' to read from stdin. If omitted, uses default sample."
    )

    args = parser.parse_args()

    # Determine input source
    if args.input_file == '-':
        # Read from stdin
        try:
            json_input = sys.stdin.read()
            if not json_input.strip():
                print("Error: No input received from stdin")
                sys.exit(1)
        except KeyboardInterrupt:
            print("\nInput cancelled")
            sys.exit(1)
    elif args.input_file:
        # Read from file
        try:
            with open(args.input_file, 'r') as file:
                json_input = file.read()
        except FileNotFoundError:
            print(f"Error: File '{args.input_file}' not found.")
            sys.exit(1)
    elif not sys.stdin.isatty():
        # Detect if input is being piped
        json_input = sys.stdin.read()
    else:
        # Default sample GraphQL JSON input
        json_input = '''
        {"data":{"data":{"*dashMySettings":"urn:li:fsd_mySettings:singleton","$recipeTypes":["com.linkedin.4e8f2aef27cc04d2d1b99173e6b3c8dd"],"$type":"com.linkedin.4e8f2aef27cc04d2d1b99173e6b3c8dd"},"extensions":{"webMetadata":{}}},"meta":{"microSchema":{"isGraphQL":true,"version":"2.1","types":{"com.linkedin.5b6de3e28a1594a050ca1d74938c3e1f":{"fields":{"enableSoundsDesktop":{"type":"boolean"},"videoAutoPlay":{"type":"com.linkedin.voyager.dash.common.VideoAutoPlaySetting"},"shareVisibilityType":{"type":"com.linkedin.voyager.dash.common.ShareVisibilityTypeSetting"},"entityUrn":{"type":"com.linkedin.voyager.dash.common.MySettingsUrn"},"adsPrivacyAllowUseOfThirdPartyData":{"type":"boolean"}},"baseType":"com.linkedin.voyager.dash.common.MySettings"},"com.linkedin.4e8f2aef27cc04d2d1b99173e6b3c8dd":{"fields":{"dashMySettings":{"type":"com.linkedin.5b6de3e28a1594a050ca1d74938c3e1f"}},"baseType":"com.linkedin.graphql.Query"}}}},"included":[{"shareVisibilityType":"PUBLIC","entityUrn":"urn:li:fsd_mySettings:singleton","enableSoundsDesktop":true,"videoAutoPlay":"ALWAYS","$recipeTypes":["com.linkedin.5b6de3e28a1594a050ca1d74938c3e1f"],"adsPrivacyAllowUseOfThirdPartyData":true,"$type":"com.linkedin.voyager.dash.common.MySettings"}]}
        '''

    # Format and print the result
    formatted_output = format_graphql(json_input)
    print(formatted_output)

if __name__ == "__main__":
    main()