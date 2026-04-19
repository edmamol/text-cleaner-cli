#!/usr/bin/env python3
"""
text-cleaner-cli: A simple command-line utility to clean and normalize text files.

This utility removes extra spaces, normalizes line endings, removes citation references,
and produces clean text. Supports multiple input files that are combined and cleaned together.
Perfect for learning Python, Git, and CLI development!
"""

import argparse
import re
import sys
from pathlib import Path


def clean_text(text):
    """
    Clean and normalize text by:
    - Normalizing line endings to \\n
    - Removing citation references like [cite:11], [cite:22], etc.
    - Removing extra spaces within lines
    - Removing blank lines
    - Stripping leading/trailing whitespace from the entire text
    
    Args:
        text (str): Raw text to clean
        
    Returns:
        str: Cleaned text
    """
    # Normalize line endings across different systems (Windows, Linux, Mac)
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # Remove citation references like [cite:11], [cite:22], etc.
    text = re.sub(r'\[cite:[^\]]*\]', '', text)
    
    # Split into lines for processing
    lines = text.split('\n')
    
    # Clean each line: remove extra spaces and strip whitespace from edges
    cleaned_lines = []
    for line in lines:
        # Replace multiple spaces with single space and strip edges
        cleaned_line = ' '.join(line.split())
        
        # Only keep non-empty lines
        if cleaned_line:
            cleaned_lines.append(cleaned_line)
    
    # Join cleaned lines back together
    result = '\n'.join(cleaned_lines).strip()
    
    return result


def read_file(file_path):
    """
    Read content from a file with error handling.
    
    Args:
        file_path (str): Path to the file to read
        
    Returns:
        str: File content, or None if error occurs
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        return None


def write_file(file_path, content):
    """
    Write content to a file with error handling.
    
    Args:
        file_path (str): Path where to save the file
        content (str): Content to write
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create parent directories if they don't exist
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing file: {e}", file=sys.stderr)
        return False


def main():
    """
    Main entry point for the text-cleaner CLI.
    Parses command-line arguments and processes the text file(s).
    """
    # Set up argument parser for command-line interface
    parser = argparse.ArgumentParser(
        description='Clean and normalize text files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python text-cleaner.py input.txt
  python text-cleaner.py input.txt --output cleaned.txt
  python text-cleaner.py file1.txt file2.txt -o combined_cleaned.txt
  python text-cleaner.py *.txt --output all_cleaned.txt
        """
    )
    
    # Define command-line arguments
    parser.add_argument(
        'input_files',
        nargs='+',
        help='Path(s) to input text file(s) to clean (supports wildcards like *.txt)'
    )
    
    parser.add_argument(
        '-o', '--output',
        dest='output_file',
        default=None,
        help='Path to save cleaned text (default: prints to console)'
    )
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Read and combine all input files
    all_content = []
    failed_files = []
    
    print(f"Processing {len(args.input_files)} file(s)...")
    
    for input_file in args.input_files:
        print(f"Reading: {input_file}")
        content = read_file(input_file)
        if content is not None:
            all_content.append(content)
        else:
            failed_files.append(input_file)
    
    # Exit if no files were successfully read
    if not all_content:
        print("Error: No input files could be read successfully.", file=sys.stderr)
        sys.exit(1)
    
    # Warn about failed files but continue with successful ones
    if failed_files:
        print(f"Warning: {len(failed_files)} file(s) could not be read: {', '.join(failed_files)}")
    
    # Combine all content with double newlines between files
    combined_content = '\n\n'.join(all_content)
    
    # Clean the combined text
    cleaned_content = clean_text(combined_content)
    
    # Output the result
    if args.output_file:
        # Save to output file
        if write_file(args.output_file, cleaned_content):
            print(f"✓ Cleaned text saved to: {args.output_file}")
            print(f"   Combined {len(all_content)} file(s) into cleaned output")
        else:
            sys.exit(1)
    else:
        # Print to console
        print("\n--- Cleaned Output ---\n")
        print(cleaned_content)
        print("\n--- End of Output ---\n")


if __name__ == '__main__':
    main()
