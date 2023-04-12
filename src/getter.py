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

from src.config import Config
from src.util import *
from src.logger import *

def get_thread(
    thread_url: str
    ) -> dict:
    """
    Fetches the thread contents.
    Checks for archived versions incase a 404 is found

    Args:
        thread_url str: Url of the thread
    
    Returns:
        dict: Thread information
    """
    
    host, board, thread = split_url(thread_url)

    req = Config.session.get(f"https://a.4cdn.org/{board}/thread/{thread}.json")
    response = {}

    try:
        if "<title>Just a moment...</title>" in req.text:
            logging.error("Blocked by cloudflare :(")
            exit()

        if req.status_code == 404:

            # iterate over each archive
            # until one returns a 200
            for url, boards in Config.archives:
                
                if board in boards:
                    url = url.format(board=board, thread=thread)
                    req = Config.session.get(url)

                    if req.status_code != 200:
                        continue

                    # TODO:
                    # scrape info from HTML
                    # and turn into json
                    response = {}
        
        else:
            response = req.json()
    
    except Exception as exc:
        logging.error(f"Failed to get thread: {str(exc).rstrip()}")
        logging.error(f"Response code: {req.status_code}")
        logging.error(f"Response body:")
        print(req.text)

        exit()
    
    return response