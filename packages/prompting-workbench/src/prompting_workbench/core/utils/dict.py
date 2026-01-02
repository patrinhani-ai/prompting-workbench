def deep_merge(dict1, dict2):
    """
    Merge two dictionaries, including nested dictionaries, recursively.
    The values from dict2 overwrite values from dict1.
    """
    merged_dict = dict1.copy()  # Start with a copy of dict1
    for key, value in dict2.items():
        if (
            key in merged_dict
            and isinstance(merged_dict[key], dict)
            and isinstance(value, dict)
        ):
            # If both values are dictionaries, merge them recursively
            merged_dict[key] = deep_merge(merged_dict[key], value)
        else:
            # Otherwise, use the value from dict2 (overwrite)
            merged_dict[key] = value
    return merged_dict
