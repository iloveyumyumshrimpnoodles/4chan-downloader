# 4chan-downloader

Python tool to download all images, gifs and webms in a 4chan thread

# Installation
1. Clone repository
```
git clone https://github.com/iloveyumyumshrimpnoodles/4chan-downloader
cd 4chan-downloader
```
2. Install required libraries
```
pip install requests
```
3. Run the tool
```
python3 downloader.py --help
```

# Usage

The main script is called `downloader.py` and can be called like this: `python3 downloader.py [thread/filename] [args]`

```
usage: downloader.py [-h] [-c] [-t] [--overwrite] [--exit-when-done] [-s] [-o directory] [-p proxy] [--chunk-size chunk_size] thread

4chan downloader

positional arguments:
  thread                URL of the thread (or filename; one url per line)

options:
  -h, --help            show this help message and exit
  -c, --counter         Show a counter next the the image that has been downloaded
  -t, --title           Save original filenames
  --overwrite           Overwrite existing files
  --exit-when-done      Don't reload the page for more downloads, but exit once done
  -s, --sleeps          Introduce random sleeps to look more human-like
  -o directory, --output directory
                        Directory to store images in
  -p proxy, --proxy proxy
                        Proxy to use (protocol://ip:port)
  --chunk-size chunk_size
                        Chunk size
```

You can parse a file instead of a thread url. In this file you can put as many links as you want, you just have to make sure that there's one url per line. A line is considered to be a url if the first 4 letters of the line start with 'http'.

# License
```
This project is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, 
either version 3 of the License, or any later version.

This project is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this code. 
If not, see <https://www.gnu.org/licenses/>. 
```