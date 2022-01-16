import os

import requests


def download_file(url, filename):
    try:
        with requests.get(url) as req:
            with open(filename, 'wb') as f:
                for chunk in req.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return filename
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    root_dir = os.getcwd()
    filename = os.path.join(root_dir, 'apple.jpeg')
    download_image_url = 'https://media.istockphoto.com/photos/red-apple-with-leaf-isolated-on-white-background-picture-id185262648?b=1&k=20&m=185262648&s=170667a&w=0&h=2ouM2rkF5oBplBmZdqs3hSOdBzA4mcGNCoF2P0KUMTM='
    download_file(download_image_url, filename)
