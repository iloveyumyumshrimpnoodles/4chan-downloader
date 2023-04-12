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

from requests import Session, adapters

class Config:
    threads = 12
    archives = [

        # format:
        # (link, [archived boards])
        ("https://archived.moe/{board}/thread/{thread}", ["3", "a", "aco", "adv", "an", "asp", "b", "bant", "biz", "c", "can", "cgl", "ck", "cm", "co", "cock", "con", "d", "diy", "e", "f", "fa", "fap", "fit", "fitlit", "g", "gd", "gif", "h", "hc", "his", "hm", "hr", "i", "ic", "int", "jp", "k", "lgbt", "lit", "m", "mlp", "mlpol", "mo", "mtv", "mu", "n", "news", "o", "out", "outsoc", "p", "po", "pol", "q", "qa", "qst", "r", "r9k", "s", "s4s", "sci", "soc", "sp", "spa", "t", "tg", "toy", "trash", "trv", "tv", "u", "v", "vg", "vint", "vip", "vp", "vr", "w", "wg", "wsg", "wsr", "x", "y"]),
        ("https://thebarchive.com/{board}/thread/{thread}", ["b", "bant"]),
        ("https://archiveofsins.com/{board}/thread/{thread}", ["h", "hc", "hm", "r", "s", "soc"]),
        ("https://archive.4plebs.org/{board}/thread/{thread}", ["adv", "f", "hr", "o", "pol", "s4s", "sp", "tg", "trv", "tv", "x"]),
        ("https://archive.nyafuu.org/{board}/thread/{thread}", ["bant", "c", "con", "e", "n", "news", "out", "p", "toy", "vip", "vp", "w", "wg", "wsr"])
    ]

    adapter = adapters.HTTPAdapter(
        pool_connections=threads+2, 
        pool_maxsize=threads+2
    )

    session = Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.verify = False
    session.cert = None
    session.headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Dnt" : "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User":"?1",
        "Te": "trailers",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:103.0) Gecko/20100101 Firefox/103.0"
    }