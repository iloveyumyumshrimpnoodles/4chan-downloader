"""
Python tool to download all images, gifs and webms in a 4chan thread
Copyright (C) 2023 iloveyumyumshrimpnoodles

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

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