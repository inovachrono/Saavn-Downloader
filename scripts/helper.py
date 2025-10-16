import os
import re
import json
import argparse
from typing import NoReturn

import requests
from tqdm import tqdm

def scan_url(url):
    url_parts = url.split("/")
    if "album" in url_parts:
        return "album"
    elif "artist" in url_parts:
        return "artist"
    elif "playlist" in url_parts or "featured" in url_parts:
        return "playlist"
    elif "song" in url_parts:
        return "song"

def setProxy():
    proxy_ip = ""
    if ("http_proxy" in os.environ):
        proxy_ip = os.environ["http_proxy"]
    proxies = {
        "http": proxy_ip,
        "https": proxy_ip,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
        "cache-control": "private, max-age=0, no-cache"
    }
    return proxies, headers

def download_file(url, dest_path=None, timeout=30, show_progress=False, retries=3):
    """
    Download a file from a URL with retry logic and optional progress bar.
    
    Args:
        url (str): URL of the file to download
        dest_path (str, optional): Destination path. If None, uses current directory
        timeout (int): Timeout in seconds for each request
        show_progress (bool): Whether to show progress bar
        retries (int): Number of retry attempts (default: 3)
    
    Returns:
        str: Path to the downloaded file
        
    Raises:
        Exception: If download fails after specified retries
    """
    # Determine filename from URL if not provided in path
    if dest_path is None:
        filename = url.split("/")[-1] or "downloaded_file"
        dest_path = os.path.join(os.getcwd(), filename)
    elif os.path.isdir(dest_path):
        filename = url.split("/")[-1] or "downloaded_file"
        dest_path = os.path.join(dest_path, filename)

    for attempt in range(retries + 1):
        try:
            # Head request to get file size for progress bar
            total_size = 0
            progress_bar: tqdm[NoReturn] | None = None
            if show_progress:
                with requests.head(url, timeout=timeout) as response:
                    total_size: int = int(response.headers.get("content-length", 0))
            
            # Stream download
            with requests.get(url, stream=True, timeout=timeout) as response:
                response.raise_for_status()
                
                # Initialize progress bar
                if show_progress and total_size > 0:
                    progress_bar = tqdm(
                        total=total_size,
                        unit="B",
                        unit_scale=True,
                        desc=os.path.basename(dest_path),
                        bar_format="{percentage:3.0f}%|{bar:40}{r_bar}",
                    )
                
                # Download file
                directory = os.path.dirname(dest_path)
                if directory and not os.path.exists(directory):
                    os.makedirs(directory, exist_ok=True)
                with open(dest_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            if show_progress and total_size > 0 and progress_bar:
                                progress_bar.update(len(chunk))
                
                if show_progress and total_size > 0 and progress_bar:
                    progress_bar.close()
            
            # Download completed successfully
            return dest_path
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == retries:
                raise Exception(f"Download failed after {retries + 1} attempts: {str(e)}")
            print("Retrying...")

def argManager():
    parser = argparse.ArgumentParser()
    parser.add_argument("-artist", "--artist", action="store_true", help="Download for an Artist")
    parser.add_argument("-song", "--song", action="store_true", help="Download Songs")
    parser.add_argument("-album", "--album", action="store_true", help="Download Albums")
    parser.add_argument("-fast", "--fast", action="store_true", help="Get details asynchronously")

    parser.add_argument("-user", "--user", action="store_true", help="Signin as JioSaavn user")
    parser.add_argument("-p", "--p", action="store_true", help="Download Playlists by signing in")
    parser.add_argument("-a", "--a", action="store_true", help="Download Albums by signing in")
    parser.add_argument("-s", "--s", action="store_true", help="Download Shows by signing in")

    parser.add_argument("-clone", "--clone", action="store_true", help="Clone songs,albums,playlists to new account")
    parser.add_argument("-create", "--create", action="store_true", help="To create new account for cloning")
    parser.add_argument("-copy", "--copy", action="store_true", help="To copy to another account")

    parser.add_argument("-o", "--outFolder", help="Path to store the Downloaded songs folder")
    parser.add_argument("-u", "--url", help="URL of the song, playlist, album, artist")
    parser.add_argument("-e", "--email", help="Email of the Jio Saavn User")
    parser.add_argument("-pw", "--password", help="Password of the Jio Saavn User")
    parser.add_argument("-f", "--file", help="file with the urls of songs, albums, playlists, artists")
    args = parser.parse_args()
    return args