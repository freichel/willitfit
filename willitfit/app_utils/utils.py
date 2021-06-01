## Parse line function
def _parse_line(line):
    """
    Do a regex search against all defined regexes and
    return the key and match result of the first matching regex
    """
    for key, rx in rx_dict.items():
        match = rx.findall(line)
        if match:
            return key, match
    # if there are no matches
    return None, None