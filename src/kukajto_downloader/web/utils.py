import requests
from tqdm import tqdm


from .constants import CHUNK_SIZE

def download_file(url, file, headers={}, update=lambda percent: None):
    page = requests.get(url, headers=headers, stream=True)
    
    page.raise_for_status()

    total = int(page.headers.get("content-length", -1))

    pbar = tqdm(total=total, unit='iB', unit_scale=True, unit_divisor=1024)
    
    for chunk in page.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            wrote = file.write(chunk)

            pbar.update(wrote)
            update(int(pbar.n/pbar.total*100))
    
    pbar.close()