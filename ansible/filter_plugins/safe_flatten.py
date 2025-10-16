def safe_flatten(data):
    """
    Flattens mixed nested lists/dicts while gracefully ignoring strings.
    Returns a list.
    """
    if data is None:
        return []

    if isinstance(data, dict):
        items = data.values()
    elif isinstance(data, list) or isinstance(data, tuple):
        items = data
    else:
        return [data]

    result = []
    for item in items:
        if isinstance(item, (list, tuple)):
            result.extend(safe_flatten(item))
        elif isinstance(item, dict):
            result.extend(safe_flatten(item.values()))
        elif isinstance(item, str):
            # Skip raw text (e.g., AnsibleUnsafeText) unless desired
            continue
        else:
            result.append(item)
    return result


class FilterModule(object):
    """Custom Ansible filters"""

    def filters(self):
        return {
            'safe_flatten': safe_flatten,
        }
