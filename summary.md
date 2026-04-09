# VT Šimek – Web Progress Summary

## Stav: v1.0 HOTOVO

## Zdroj dat
Web scraping z https://vtsimek.cz/ — extrahováno:
- Název: Vodo-Topo Šimek, majitel David Šimek
- IČ: 073 04 897, od roku 2018
- Adresa: Sokolovská 1484, 686 01 Uherské Hradiště – Mařatice
- Tel: +420 737 789 088, Email: vtsimek@seznam.cz
- 9 služeb: čištění kanalizace, vodoinstalace, vytápění, plynoinstalace, jádrové vrtání, kotle/bojlery, úpravny vod (CosmoWATER, Trinnity), tepelná čerpadla, fototermické panely

## Design rozhodnutí

### Fonty
- **Urbanist** (700, 800) — nadpisy. Geometrický, moderní, lehce technický. Poprvé použit v DNA archivu.
- **DM Sans** (400, 500) — tělo textu. Čistý, profesionální, výborná čitelnost. Poprvé použit.

### Paleta
| Proměnná | Hex | Použití |
|----------|-----|---------|
| --navy   | #1A3152 | nav, hero bg, dark sekce, text důvěra |
| --orange | #F26419 | CTA buttony, akcentace, energie/teplo |
| --blue   | #3B9FD1 | service ikony, doplňkový akcent, voda |
| --light  | #F4F6F8 | střídající sekce, formulář bg |
| --dark   | #1C1C2E | základní text |

## Sekce webu
1. **Nav** — sticky, logo VT Šimek, hamburger na mobilu
2. **Hero** — full-height, námořní bg + grid lines + radiální gradienty, headline, 2 CTA, stats, service cards (desktop)
3. **Služby** — 9 karet v 3×3 gridu, SVG ikony, hover animace + oranžová linka
4. **O nás** — split layout, placeholder image, badge "2018", seznam benefitů
5. **Proč my** — dark sekce, 4 karty s ikonami
6. **Galerie** — CSS placeholder grid, 5 položek, hover overlay
7. **Kontakt** — info vlevo + formulář vpravo (poptávka), select dropdown služby
8. **Mapa** — Google Maps embed
9. **Footer** — 3 sloupce + copyright

## Responsivita (dle CLAUDE.md)
- overflow-x: hidden na html i body
- font-size nikdy pod 16px
- min-height: 44px na všech tlačítkách a interaktivních prvcích
- Breakpointy: 1024px, 768px, 640px, 428px, 375px, 320px
- 640px: hamburger menu, services → 1 sloupec, hero-actions → column
- 375px: nav logo sub skrytý, why grid → 1 sloupec
- 320px: h1 1.9rem, nav logo sub skrytý

## Animace
- IntersectionObserver fade-up (threshold 0.12)
- delay třídy d1–d6 (0.1–0.6s)
- Nav scroll shadow efekt
- Service card hover: translateY(-4px) + orange top border reveal
- Gallery hover: scale(1.06) + overlay

## Soubory
- `index.html` — kompletní jednostránkový web (vše v jednom souboru)
- `summary.md` — tento soubor
