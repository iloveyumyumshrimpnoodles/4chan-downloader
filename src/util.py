def split_url(
    url: str
    ) -> tuple[str, str, str]:
    """
    Parses the url into 3 pieces: host, board and thread

    Args:
        url str: Thread url
    
    Returns:
        tuple[str, str, str]: Host, body and thread
    """

    splitted = url.split("/")

    # i could unpack
    # but this looks better
    host = splitted[2]
    board = splitted[3]
    thread = splitted[5]

    return host, board, thread