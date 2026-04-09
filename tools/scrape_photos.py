"""
Stáhne fotky z vtsimek.cz a uloží je do photos/
"""
import urllib.request
import urllib.parse
import re
import os
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

URL = "https://vtsimek.cz/"
OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'photos')

def fetch(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode('utf-8', errors='replace')

def fetch_binary(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

def find_subpages(html, base):
    """Hledá podstránky (galerie, fotogalerie, realizace)."""
    links = re.findall(r'href=["\']([^"\']*(?:galerie|galery|foto|photo|album|realizace|portfolio)[^"\']*)["\']', html, re.I)
    found = []
    for link in links:
        if link.startswith('http'):
            found.append(link)
        elif link.startswith('/'):
            found.append(urllib.parse.urljoin(base, link))
    return list(dict.fromkeys(found))

def extract_images(html, base):
    srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html, re.I)
    # also look for data-src, data-lazy-src
    srcs += re.findall(r'data-(?:src|lazy-src|original)=["\']([^"\']+)["\']', html, re.I)
    # look for background-image in style
    srcs += re.findall(r'url\(["\']?([^"\')\s]+)["\']?\)', html, re.I)
    full = []
    for s in srcs:
        if s.startswith('data:'):
            continue
        url = s if s.startswith('http') else urllib.parse.urljoin(base, s)
        full.append(url)
    return full

def filter_photos(urls):
    keep = []
    skip = re.compile(r'(icon|logo|pixel|sprite|thumb|\.gif$|1x1|spacer|arrow|btn|star|bg-|banner|pattern|gradient)', re.I)
    for u in urls:
        path = urllib.parse.urlparse(u).path.lower()
        if not re.search(r'\.(jpg|jpeg|png|webp)(\?|$)', path):
            continue
        if skip.search(path):
            continue
        keep.append(u)
    return list(dict.fromkeys(keep))

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"Stahuji hlavni stranku: {URL}")
    html = fetch(URL)

    subpages = find_subpages(html, URL)
    pages = [URL] + subpages
    if subpages:
        print(f"Nalezeny podstranky: {subpages}")
    else:
        print("Zadne podstranky galerie nenalezeny, skenuji jen hlavni stranku.")

    all_imgs = []
    for page in pages:
        page_html = html if page == URL else fetch(page)
        imgs = extract_images(page_html, page)
        all_imgs.extend(imgs)
        print(f"  {page}: {len(imgs)} obrazku nalezeno")

    photos = filter_photos(all_imgs)
    print(f"\nFotky k stazeni: {len(photos)}")
    for u in photos:
        print(f"  {u}")

    if not photos:
        print("\nZadne fotky nenalezeny.")
        sys.exit(1)

    print(f"\nStahuji do {OUT_DIR}/ ...")
    saved = 0
    for i, url in enumerate(photos, 1):
        path_part = urllib.parse.urlparse(url).path
        ext = os.path.splitext(path_part)[1].split('?')[0] or '.jpg'
        if ext not in ('.jpg', '.jpeg', '.png', '.webp'):
            ext = '.jpg'
        fname = f"foto-{i}{ext}"
        fpath = os.path.join(OUT_DIR, fname)
        try:
            data = fetch_binary(url)
            if len(data) < 5000:
                print(f"  SKIP {fname} (prilis maly: {len(data)} B)")
                continue
            with open(fpath, 'wb') as f:
                f.write(data)
            print(f"  OK {fname}  ({len(data)//1024} kB)  <- {url}")
            saved += 1
        except Exception as e:
            print(f"  ERR {url}: {e}")

    print(f"\nHotovo. Stazeno {saved} fotek.")

if __name__ == '__main__':
    main()
