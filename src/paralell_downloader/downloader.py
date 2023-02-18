import requests
import threading

class ParalellDownloaderError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ParalellDownloader:
    CHUNK_SIZE = 1 << 20 # 1 MiB

    def __init__(self, url, filename, parts, pbar=None, chunk_size=CHUNK_SIZE, headers={}, file_size=None):
        """
        Downloads file using paralell downloading.

        Parameters
        ----------
        url : str
            Url of the video.
        filename : str
            Name of file to download.
        parts : int
            Count of parts.
        pbar : tqdm, optional
            Progress bar object. By default no progress bar.
        chunk_size : int, optional
            Chunk size used while downloading. By default 1 MiB.
        user_agent : str, optional
            User agent string to use while downloading.
        headers : dict, optional
            Other http headers.
        file_size : int | None, optional
            Specify file size in bytes. If none,
            detects automatically vias head request.
        """

        self.url = url
        self.filename = filename
        self.parts = parts
        self.pbar = pbar
        self.chunk_size = chunk_size
        self.headers = headers
        self.file_size = file_size

        if parts <= 0:
            raise ValueError("parts must be a positive integer")


        self.lock = threading.Lock()
        self.close_event = threading.Event()
        self.threads = []
        self.file = None

    def _get_file_size(self):
        """
        Sends head request to server to determine file size if no file size is specified.
        """
        if self.file_size:
            return int(self.file_size)
        
        info = requests.head(self.url, allow_redirects=True, headers=self.headers)

        return int(info.headers.get("content-length", 0))
    
    def _get_byte_range(self, index):
        """
        Finds byte range

        Parameters
        ----------
        index : int
            Index of part
        
        Returns
        -------
        byte_range : tuple(start_position, end_position)
            Range of positions in bytes
        """
        if index + 1 == self.parts: # fix last part have more bytes
            byte_range = (self.size_per_part * index, self.file_size - 1)
        else:
            byte_range = (self.size_per_part * index, self.size_per_part * (index + 1) - 1)
        
        return byte_range
    
    def _download_part(self, index):
        """
        Downloads a part of file
        """
        byte_range = self._get_byte_range(index)
        
        headers = {"Range": "bytes={}-{}".format(*byte_range)}
        headers.update(self.headers)

        response = requests.get(
            self.url,
            headers=headers,
            allow_redirects=True,
            stream=True,
        )

        if response.status_code != 206: raise ParalellDownloaderError(f"got status code {response.status_code} instead of 206")

        file_offset = byte_range[0]
        for chunk in response.iter_content(chunk_size=self.chunk_size):
            if chunk: # ignore chunks without content
                with self.lock:
                    self.file.seek(file_offset)
                    self.file.write(chunk)
                    
                    file_offset += len(chunk)
                    
                    if self.pbar is not None: self.pbar.update(len(chunk))
            if self.close_event.is_set():
                break
    def start(self):
        """
        Starts downloading.
        """
        self.file = open(self.filename, "wb", self.chunk_size) # set buffer to chunk size

        self.file_size = self._get_file_size()
        
        if self.file_size == 0:
            # nothing to download, close file
            self.file.close()

        if self.pbar is not None:
            # set pbar to show total bytes
            self.pbar.total = self.file_size
        

        self.size_per_part = self.file_size // self.parts

        self.threads = [threading.Thread(target=self._download_part, args=[index]) for index in range(self.parts)]

        for thread in self.threads:
            thread.start()

    def wait(self):
        """
        Waits until downloading complete.
        """
        if not self.is_running():
            self.start()
        try:
            for thread in self.threads:
                thread.join()
        except KeyboardInterrupt:
            pass
        finally:
            self.terminate()
    
    def terminate(self):
        """
        Terminates downloading.
        """
        if self.is_running():
            self.close_event.set()

            for thread in self.threads:
                thread.join()
            
        self.file.close()
    
    def is_running(self):
        """
        Checks if is downloading running.
        """
        return any(thread.is_alive() for thread in self.threads)

if __name__ == "__main__":
    from tqdm import tqdm
    
    URL = input("Enter url: ")
    FILE = input("Enter file: ")
    PARTS = int(input("Enter number of parts: "))

    print(f"Downloading {URL} to {FILE} ...")
    
    pbar = tqdm(unit='iB', unit_scale=True, unit_divisor=1024)

    ParalellDownloader(URL, FILE, PARTS, pbar=pbar).wait()
