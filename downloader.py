import argparse, time, os, hashlib

from os.path import exists, join
from queue import Queue
from threading import Thread
from random import uniform

from src.util import *
from src.config import *
from src.logger import *
from src.getter import *

from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)

parser = argparse.ArgumentParser(description="4chan downloader")
parser.add_argument("thread", nargs=1, help="URL of the thread (or filename; one url per line)")
parser.add_argument("-c", "--counter",        action="store_true",  help="Show a counter next the the image that has been downloaded", default=False)
parser.add_argument("-t", "--title",          action="store_true",  help="Save original filenames", default=False)
parser.add_argument(      "--overwrite",      action="store_true",  help="Overwrite existing files", default=False)
parser.add_argument(      "--exit-when-done", action="store_true",  help="Don\"t reload the page for more downloads, but exit once done", default=False)
parser.add_argument("-s", "--sleeps",         action="store_true",  help="Introduce random sleeps to look more human-like", default=False)
parser.add_argument("-o", "--output",         metavar="directory",  help="Directory to store images in", default="output")
parser.add_argument("-p", "--proxy",          metavar="proxy",      help="Proxy to use (protocol://ip:port)", default=None)
parser.add_argument(      "--chunk-size",     metavar="chunk_size", help="Chunk size", default=2048, type=int)
args = parser.parse_args()

if not exists(args.output):
    os.mkdir(args.output)

proxy = args.proxy if args.proxy != "tor" else "socks5h://127.0.0.1:9050"
Config.session.proxies = {
    "http": proxy,
    "https": proxy
} if args.proxy else {
    "http": "", 
    "https": ""
}

logging.info("Loading MD5 blacklist")
md5_hashes = []
with open("src/files/blacklist.md5") as fd:
    for digest in fd:
        md5_hashes.append(digest.rstrip())

class Downloader:
    def __init__(self):

        # initialize queues
        self.responses = Queue(512)
        self.queue = Queue(512)
        self.exists = []

        # counters
        self.downloaded = self.failed = self.total = self.all = 0

    def check_output_dir(self) -> None:
        """
        Calculates a MD5 hash for every existing file in the output folder

        Returns:
            None: Nothing.
        """

        for entry in os.scandir(args.output):
            if not entry.is_file: # skip directories
                continue

            file = entry.path
            with open(file, "rb") as fd:

                hasher = hashlib.md5()
                for chunk in iter(lambda: fd.read(4096), b""):
                    hasher.update(chunk)
            
            digest = hasher.hexdigest()            
            self.exists.append(digest)

    def collect_files(self) -> None:
        """
        Collects all files, and appends them to a queue

        Returns:
            None: Nothing.
        """

        logging.info("Collecting files")

        if args.thread[0].startswith("http"):

            self.responses.put(
                (get_thread(args.thread[0]), *split_url(args.thread[0]))
            )

        else:
            with open(args.thread) as fd:
                for url in fd:
                    self.responses.put(
                        (get_thread(url), *split_url(url))
                    )
                
                if args.sleeps:
                    time.sleep(uniform(1, 2))
        
    def download_task(self):
        """
        Downloader task, grabs a file from the queue and downloads it

        Returns:
            None: Nothing.
        """

        while 1:

            if self.queue.empty():
                break

            outfile, dlink = self.queue.get()

            # request file
            try:
                req = Config.session.get(dlink, stream=True)

                chunks = []
                hasher = hashlib.md5()

                for chunk in req.iter_content(args.chunk_size):

                    if chunk:
                        hasher.update(chunk)
                        chunks.append(chunk)

                digest = hasher.hexdigest()
                if (not digest in self.exists) or args.overwrite:
                    msg = f"Downloading '{outfile}' ({dlink})"

                    self.exists.append(digest)

                    with open(join(args.output, outfile), "wb") as fd:
                        for chunk in chunks:
                            fd.write(chunk)

                    self.downloaded += 1
                
                else:
                    msg = None
                    
            except Exception as exc:

                msg = f"Failed to download '{outfile}' ({dlink}): {str(exc).rstrip()}"
                self.failed += 1

            if msg != None:
                if args.counter:
                    msg = f"[{str(self.downloaded).rjust(len(str(self.all)))}/{self.all}] {msg}"

                logging.info(msg)

            self.total += 1

            if args.sleeps:
                time.sleep(uniform(1, 2))

    def download_files(self) -> None:
        """
        Parses all posts, and adds them to the queue

        Returns:
            None: Nothing.
        """

        time.sleep(2) # let the queue fill up

        logging.info("Queue'ing files")
        while 1:

            if self.responses.empty():
                break

            self.all = 0 # reset the counter

            resp, domain, board, thread = self.responses.get()

            for post in resp["posts"]:

                fname = post.get("filename")
                ftim = post.get("tim")
                fext = post.get("ext")
                fmd5 = post.get("md5")
                fsize = post.get("fsize")
                filedeleted= post.get("filedeleted", 0)

                if not fname or not ftim or not fext \
                    or fmd5 in md5_hashes \
                    or filedeleted == 1:
                    continue

                dlink = f"https://i.4cdn.org/{board}/{ftim}{fext}"
                outfile = fname+fext if args.title else str(ftim)+fext
                if (not exists(outfile)) or args.overwrite:

                    #logging.info(f"Adding "{outfile}" ({dlink}) to queue")

                    self.all += 1
                    self.queue.put((outfile, dlink))
                
                #else:
                    #logging.info(f"Skipping "{outfile}": already exists")
        
        logging.info("Launching downloader tasks")
        threadbox = []
        for _ in range(Config.threads):
            kaboom = Thread(
                target=d.download_task, 
                daemon=False
            )

            threadbox.append(kaboom)

            kaboom.start()

        logging.info("Waiting for downloader tasks to finish...")
        for kaboom in threadbox:
            kaboom.join()

if __name__ == "__main__":
    d = Downloader()

    while 1:
        try:
            d.check_output_dir()
            d.collect_files()
            d.download_files()

            if args.exit_when_done:
                break

            time.sleep(
                uniform(15, 25) # wait between 15-25 seconds before rechecking
            )

            print() # empty line
            logging.info("Rechecking...")

        except:
            break

    print()
    logging.info("Finished...")