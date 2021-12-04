"""
Parses from raw text copied from: https://cran.r-project.org/web/packages/comorbidity/vignettes/comorbidityscores.html
"""


# Replaces hyphen with literal range of codes
def _range_expander(unexpanded: list):
    ret = list()
    for c in unexpanded:
        if '-' in c:
            start, end = c.split('-')
            start = start.strip()
            end = end.strip()

            # Assume all codes could start with a letter
            start_alpha_prefix = start[0] if start[0].isalpha() else ''
            start_numeric_part = int(start[1:]) if start[0].isalpha() else int(start)

            end_alpha_prefix = end[0] if end[0].isalpha() else ''
            end_numeric_part = int(end[1:]) if end[0].isalpha() else int(end)

            # If codes are ICD-10, they should both have same prefix (if ICD-9, prefix will be empty string)
            assert start_alpha_prefix == end_alpha_prefix

            # Assuming inclusive ranges here
            ret += [start_alpha_prefix + str(idx) for idx in range(start_numeric_part, end_numeric_part + 1)]

        else:
            ret += [c]

    return ret


def get_labeled_comorbidity_codes() -> (dict, dict):
    dropped_categories = [
        'Myocardial infarction',
        'Cerebrovascular disease'
    ]

    startswith_codes_by_category = dict()
    match_codes_by_category = dict()

    with open('raw_cci_codes.txt', 'r') as f:
        for line in f.readlines():
            if line == '':
                continue

            line = line.strip()
            category, raw_codes = line.split(':')

            if category in dropped_categories:
                continue

            # Codes with no '.x' are easy: just have to match them exactly
            match_codes = [c.replace('.', '').strip() for c in raw_codes.split(',') if '.x' not in c]
            match_codes = _range_expander(match_codes)

            # Codes with 'x' will be matched with any code that starts with the digits before the '.x'
            startswith_codes = [c.replace('.x', '').replace('.', '').strip() for c in raw_codes.split(',') if '.x' in c]
            startswith_codes = _range_expander(startswith_codes)

            if category not in match_codes_by_category:
                match_codes_by_category[category] = list()

            if category not in startswith_codes_by_category:
                startswith_codes_by_category[category] = list()

            match_codes_by_category[category] += match_codes
            startswith_codes_by_category[category] = startswith_codes

    return match_codes_by_category, startswith_codes_by_category


def get_comorbidity_codes() -> (set, set):
    mcodes, swcodes = get_labeled_comorbidity_codes()
    unlabeled_mcodes = [code for sublist in mcodes.values() for code in sublist]
    unlabeled_swcodes = [code for sublist in swcodes.values() for code in sublist]

    # Implicitly drop any codes that show up in multiple categories
    return set(unlabeled_mcodes), set(unlabeled_swcodes)
