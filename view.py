import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# ================== CONFIG ==================
target_base = "https://kingbokep.tv"
upload_view = "https://kingbokep.fit/view/upload.php"
local_folder = "bokep_views"
proxy_url = "https://kingbokep.fit/proxy.php?url="
custom_link = "https://iklan.situsbaik777.com/register/J5G7BGD4"
# ============================================

os.makedirs(local_folder, exist_ok=True)

def replace_custom_img(html, link):
    # cari pola <customtag ...><img ...></customtag>
    pattern = r"<[a-z0-9\-]+[^>]*>\s*(<img[^>]+>)\s*</[a-z0-9\-]+>"
    return re.sub(pattern, rf'<a href="{link}">\1</a>', html, flags=re.DOTALL)

os.makedirs(local_folder, exist_ok=True)

page_num = 1
while True:
    page_url = target_base + "/" if page_num == 1 else f"{target_base}/page/{page_num}/"
    print(f"[+] Fetching page {page_num} => {page_url}")

    r = requests.get(page_url)
    if r.status_code != 200:
        print(f"[-] Tidak ada page {page_num}, stop.")
        break

    soup = BeautifulSoup(r.text, "html.parser")
    links = [a["href"] for a in soup.find_all("a", href=True) if "/view/" in a["href"]]

    if not links:
        print(f"[-] Page {page_num} kosong, stop.")
        break

    for link in links:
        if not link.startswith("http"):
            link = target_base.rstrip("/") + link

        print(f"    [+] Fetching view {link}")
        rv = requests.get(link)
        if rv.status_code == 200:
            slug = os.path.basename(urlparse(link).path.strip("/"))

            # ==== parse & replace video ====
            html = rv.text

            # cari .m3u8 di dalam page
            match = re.search(r'(https?://[^\s\'"]+\.m3u8)', html)
            if match:
                m3u8_url = match.group(1)
                proxied = proxy_url + m3u8_url

                # ganti script/video lama jadi player custom
                player_html = f"""
<div style="background:black;display:flex;justify-content:center;align-items:center;width:100%;max-width:800px;margin:auto;">
  <video id="video" controls style="width:100%;height:auto;object-fit:contain;background:black;"></video>
</div>

<script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
<script>
  const video = document.getElementById('video');
  const videoSrc = "{proxied}";
  if (Hls.isSupported()) {{
    const hls = new Hls();
    hls.loadSource(videoSrc);
    hls.attachMedia(video);
  }} else if (video.canPlayType('application/vnd.apple.mpegurl')) {{
    video.src = videoSrc;
  }}
</script>
"""
                html = re.sub(r'<video.+?</video>', player_html, html, flags=re.S | re.I)
                if "hls.js" not in html:
                    # fallback kalau di page aslinya gak ada <video>
                    html = player_html + html

                # ==== ganti logo & teks KingBokep di nav ====
                html = r.text

                # ubah custom tag jadi <a href=...><img...></a>
                html = replace_custom_img(html, custom_link)


                #FAVICON
                html = html.replace(
                    'https://cdn.kingbokep.video/favicon-16x16.png',
                    'https://kingbokep.fit/image/icon.png'
                )
                html = html.replace(
                    'https://cdn.kingbokep.video/favicon-32x32.png',
                    'https://kingbokep.fit/image/icon.png'
                )
                html = html.replace(
                    'https://cdn.kingbokep.video/logo.svg',
                    'https://kingbokep.fit/image/icon.png'
                )
                html = html.replace(
                    'https://cdn.kingbokep.video/_astro/_path_.CKI63zVN.css',
                    'https://kingbokep.fit/_astro/_path_.CKI6.css'
                )
                html = html.replace(
                    'https://cdn.kingbokep.video/favicon.ico',
                    'https://kingbokep.fit/image/icon.png'
                )


                #GIF
                #BAIK777
                html = html.replace(
                    'https://cdn.kingbokep.video/thumbs/atunas4d-header.gif',
                    'https://i.postimg.cc/SxG1HWJc/BAIK777-GIFT.gif'
                )
                #388HERO
                html = html.replace(
                    '<img class="lazy" data-src="https://cdn.kingbokep.video/thumbs/atunas4d-footer.gif" alt=""/>',
                    '<a href="https://link388hero.com/register/YPKGR8K6"><img class="lazy" data-src="https://i.postimg.cc/j2dSQ6wv/388-HERO-GIFT.gif" alt=""/></a>'
                )
                #BANDARXL
                html = html.replace(
                    '<img class="lazy" data-src="https://cdn.kingbokep.video/thumbs/atst4d-middle.gif" alt=""/>',
                    '<a href="https://linkbandarxl.com/register/YL3B1K31"><img class="lazy" data-src="https://i.postimg.cc/MGyS6K9S/BANDARXL-GIFT.gif" alt=""/></a>'
                )

                html = html.replace(
                    '<form method="get" action="/search/"><div class="mx-auto"><div class="relative"><div class="absolute top-0 bottom-0 left-0 flex items-center pl-3 pointer-events-none"><svg class="text-primary-foreground/50" style="width:1rem;height:1rem" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"></path></svg></div><input type="text" name="keyword" enterKeyHint="search" class="block w-full p-3 pl-10 text-base border rounded-lg border-primary/30 placeholder-primary-foreground/50 focus:outline-none focus:ring-1 text-foreground focus:ring-primary focus:border-primary bg-[rgb(16,3,42)]" placeholder="Pencarian Bokep..." required="" data-clarity-unmask="true"/><button type="submit" class="text-primary-foreground/70 absolute right-1 bottom-1.5 bg-accent hover:bg-primary focus:ring-2 focus:outline-none focus:ring-primary font-medium rounded-lg text-base px-4 py-2">Cari</button></div></div></form>',
                    ''
                )         


                #TELEGRAM
                html = html.replace(
                    'Channel Tele Baru',
                    ''
                )
                html = html.replace(
                    '<a tabindex="-1" href="https://t.me/kingbokep_tv" class="fixed bottom-5 right-5 z-50 rounded-full flex items-center gap-2"> <span class="font-medium text-primary-foreground/80 [text-shadow:_0_1px_1px_rgb(0_0_0_/_0.8)] hover:text-primary">',
                    ''
                )
                html = html.replace(
                    '</span> <img style="width:35px;height:35px" src="/telegram-logo.svg" alt=""> </a>',
                    ''
                )


            # === simpan lokal pakai slug ===
            view_folder = os.path.join(local_folder, slug)
            os.makedirs(view_folder, exist_ok=True)
            view_file = os.path.join(view_folder, "index.html")
            with open(view_file, "w", encoding="utf-8") as f:
                f.write(html)

            # === upload ke server ===
            with open(view_file, "rb") as f:
                files = {"file": ("index.html", f, "text/html")}
                data = {"slug": slug}
                resp = requests.post(upload_view, files=files, data=data)

            print(f"        Upload resp: {resp.text}")

    page_num += 1

print("Done!")
