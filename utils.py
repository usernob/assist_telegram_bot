import urllib
import re


def clear_md(text: str):
    """
    escape the markdown syntax
    :param text: string to escape
    :return: escaped string
    """
    char_md = ['*','[',']','(',')','~','_','`','|']
    for i in char_md: text = text.replace(i, f'\{i}')
    return text

def clear_html(text: str):
    """
    escape the HTML syntax
    :param text: string to escape
    :return: escaped string
    """
    char = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}
    for old, new in char.items(): text = text.replace(old,new)
    return text

def encode_url(url: str):
    """
    make url safety with url encode
    :param url: url to be endcode
    :return: encode url
    """
    match = re.search('^(https?\:\/\/)(.+?)$',url)
    path = urllib.parse.quote(match.group(2))
    text = match.group(1) + path
    return text

def humansized(byte):
    '''
    human readable size in bytes
    :param byte: byte to convert
    :return: kilobyte and etc
    '''
    try:
        byte = int(byte)
    except:
        return 'invalid'
    for unit in ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB"]:
        if abs(byte) < 1024.0:
            return f"{byte:3.1f} {unit}"
        byte /= 1024.0
    return f"{byte:.1f}YiB"


