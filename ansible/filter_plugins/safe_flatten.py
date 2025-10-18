def safe_flatten(data, include_strings=False):
    """
    Recursively flattens nested lists, tuples, and dicts.
    Optionally includes string/AnsibleUnsafeText values.
    
    Args:
        data: any structure (list, dict, tuple, string, etc.)
        include_strings (bool): if True, includes string values instead of skipping them.
    
    Returns:
        A flat list of items.
    """
    if data is None:
        return []

    # Dict → flatten its values
    if isinstance(data, dict):
        items = data.values()
    # List or tuple → flatten directly
    elif isinstance(data, (list, tuple)):
        items = data
    else:
        # If include_strings is True and this is a string, wrap it in a list
        if include_strings and isinstance(data, str):
            return [data]
        return [data]

    result = []
    for item in items:
        if isinstance(item, (list, tuple, dict)):
            result.extend(safe_flatten(item, include_strings))
        elif isinstance(item, str):
            if include_strings:
                result.append(item)
            # otherwise skip strings
        else:
            result.append(item)
    return result


class FilterModule(object):
    """Custom Ansible filters"""

    def filters(self):
        return {
            'safe_flatten': safe_flatten,
        }
