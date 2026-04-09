# Workflow: Migrace galerie fotek ze staré stránky

## Cíl
Stáhnout fotky ze zdrojové URL a zapojit je do galerie v `index.html`.

## Vstupy
- `SOURCE_URL` — URL staré stránky (např. https://m-autoservis.webnode.cz/)
- `PROJECT_DIR` — složka projektu (např. C:\Users\karel\weby\M-autoservis)

## Kroky

### 1. Stáhnout fotky
Spusť `tools/scrape_photos.py` (nebo jej vytvoř podle šablony níže).

Skript musí:
- Projít hlavní stránku + podstránky galerie/fotogalerie
- Stáhnout pouze JPG/JPEG/PNG/WEBP soubory větší než 5 kB
- Přeskočit ikony, loga, spacery (filtr: icon, logo, pixel, sprite, thumb, 1x1, arrow, btn)
- Uložit jako `foto-1.jpeg`, `foto-2.jpeg`, … do `photos/`
- Spouštět s `python -X utf8` (Windows encoding fix)

### 2. Zkontrolovat stažené fotky
```
ls photos/
```
Zapiš si počet fotek (N).

### 3. Aktualizovat HTML galerii
V `index.html` najdi sekci `<!-- GALLERY -->` a:
- Uprav počet `.gallery-item` bloků na přesně N (ne víc, ne míň)
- Každý blok musí mít:
  - `data-src="photos/foto-X.jpeg"` (pro lightbox)
  - `<img src="photos/foto-X.jpeg" alt="..." loading="lazy">` (pro zobrazení v gridu)
- Odstraň všechny `.gallery-placeholder` bloky
- Střídej delay classy: `d1`, `d2`, `d3`, `d1`, `d2`, `d3`, …

### 4. Ověřit
Otevři `index.html` v prohlížeči a zkontroluj:
- [ ] Fotky se zobrazují v gridu
- [ ] Hover efekt funguje (zoom + overlay)
- [ ] Klik na foto otevře lightbox
- [ ] Šipky v lightboxu listují fotky

## Šablona gallery-item bloku
```html
<div class="gallery-item fade-up dX" data-src="photos/foto-N.jpeg">
  <img src="photos/foto-N.jpeg" alt="Popis - foto N" loading="lazy">
  <div class="gallery-item-overlay">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/>
    </svg>
  </div>
</div>
```

## Časté problémy a řešení

| Problém | Příčina | Řešení |
|---|---|---|
| `UnicodeEncodeError` na Windows | Emoji/speciální znaky v print() | Spustit s `python -X utf8` |
| Fotky se nezobrazují | `<img>` tag chybí, pouze `data-src` nestačí | Přidat `<img src="...">` do každého bloku |
| Moc málo fotek staženo | Filtr je příliš přísný | Snížit limit min. velikosti (5 kB → 2 kB) nebo rozšířit regex |
| Fotky jsou ikonky/loga | Filtr nestačí | Zkontrolovat stažené soubory ručně, smazat nevhodné |
| 6 položek v HTML ale jen 5 fotek | Počet nesedí | Vždy smazat přebývající prázdné `.gallery-item` bloky |

## Poznámky
- Fotky ze Webnode CDN mají query param `?ph=...` — urllib to zvládne bez problémů
- Galerie grid je 3 sloupce na desktopu, 2 na tabletu, 1 na mobilu
- Lightbox čte `data-src` atribut — musí sedět s `src` v `<img>`
