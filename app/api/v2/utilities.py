"""
    app.api.v2.utilities
    ~~~~~~~~~~~~~~~~~~

    General utility functions used for validating inputs

"""

def valid_location(location):
    """
    validates location input
    """
    try:
        coords_list_str = location.split(',')
        assert len(coords_list_str) == 2
        latitude, longitude = [float(c) for c in coords_list_str]
        assert -90 < latitude <= 90
        assert -180 <= longitude <= 180
        return location
    except (AssertionError, ValueError):
        return None

def valid_comment(comment):
    """
    Removes white spaces from comment
    """
    comment = comment.strip()
    return comment

def valid_status(status):
    """
    Returns True if status is one of Resolved, Investigation, Unresolved.
    Otherwise returns False
    """

    if status not in ['Resolved', 'Under Investigation', 'Unresolved']:
        return None
    return True
