#!/usr/bin/env python3
import argparse
import re

def strip_control_characters(text):
    control_char_pattern = re.compile(r'\x1b\[[0-9;]*[mGKH]')
    return control_char_pattern.sub('', text)

def find_fqdns(in_scope_domains_file, text_file, output_file=None):
    with open(in_scope_domains_file, 'r') as in_scope_domains_file:
        in_scope_domains = in_scope_domains_file.read().splitlines()

    with open(text_file, 'r') as text_file:
        text_to_search = text_file.read()

    fqdns = []

    for in_scope_domain in in_scope_domains:
        # Escape the in-scope domain for regex
        escaped_domain = re.escape(in_scope_domain)

        # Create a regex pattern to match the entire FQDN for the current in-scope domain
        pattern = fr'(?i)(\S*?\.{escaped_domain})\b'
        regex = re.compile(pattern)

        # Find all matches in the text
        matches = regex.findall(text_to_search)

        # Filter out wildcards and URLs from the results
        filtered_matches = [match for match in matches if '*' not in match and not match.startswith(('http://', 'https://'))]

        # Strip control characters from the filtered FQDNs
        stripped_fqdns = [strip_control_characters(fqdn) for fqdn in filtered_matches]

        # Add the stripped FQDNs to the result list
        fqdns.extend(stripped_fqdns)

    # Sort and create a unique list of FQDNs
    unique_sorted_fqdns = sorted(set(fqdns))

    if output_file:
        with open(output_file, 'w') as output_file:
            for fqdn in unique_sorted_fqdns:
                output_file.write(fqdn + '\n')

    return unique_sorted_fqdns

def main():
    parser = argparse.ArgumentParser(description='Find and list unique FQDNs matching in-scope domains in a text file.')
    parser.add_argument('in_scope_domains_file', help='Path to the file containing in-scope domains (one per line)')
    parser.add_argument('text_file', help='Path to the text file to search for FQDNs')
    parser.add_argument('-o', '--output', help='Path to the output file for results')

    args = parser.parse_args()

    result_fqdns = find_fqdns(args.in_scope_domains_file, args.text_file, args.output)

    print("Sorted and Unique FQDNs:")
    for fqdn in result_fqdns:
        print(fqdn)

if __name__ == "__main__":
    main()
