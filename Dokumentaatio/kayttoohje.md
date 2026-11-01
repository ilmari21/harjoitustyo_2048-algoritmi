# Käyttöohje

## Projektin lataaminen ja asentaminen

Projektin voi ladata [GitHubista](https://github.com/ilmari21/harjoitustyo_2048-algoritmi)
valitsemalla **Code** ja sen jälkeen **Download ZIP**. Projektin voi myös
kloonata Gitillä:

```text
git clone https://github.com/ilmari21/harjoitustyo_2048-algoritmi.git
```

Projektin suorittamiseen tarvitaan Pythonin versio 3.12 tai uudempi. Riippuvuudet asennetaan Poetrylla projektin
juurihakemistossa:

```text
poetry install
```

Jos Poetry yrittää asentaa projektia pakettina ja ilmoittaa, ettei projektia
voida asentaa, riippuvuudet voi asentaa ilman projektipakettia:

```text
poetry install --no-root
```

## Tekoälyn suorittaminen

Käynnistä tekoäly komennolla:

```text
poetry run invoke start
```

Ohjelma kysyy ensin vähimmäis- ja enimmäishakusyvyydet:

```text
Enter the minimum search depth for the AI (2-6, default is 4):
Enter the maximum search depth for the AI (4-6, default is 4):
```

Hakusyvyydet ovat kokonaislukuja väliltä 2–6, ja enimmäissyvyyden täytyy olla
vähintään vähimmäissyvyyden suuruinen. Jos kysymyksiin vastataan painamalla
Enter, käytetään oletusarvoja 4 ja 4. Asetuksilla `min_depth-max_depth` ohjelma
valitsee pelin aikana hakusyvyyden tyhjien ruutujen määrän perusteella kyseisen
välin sisältä.

Ohjelma tulostaa jokaisen siirron, käytetyn hakusyvyyden, pistemäärän ja
pelilaudan. Peli päättyy, kun tekoäly ei löydä enää laillista siirtoa.

## Pelin pelaaminen itse

Käynnistä ihmispeli komennolla:

```text
poetry run invoke play
```

Syötteenä käytetään seuraavia näppäimiä:

| Näppäin | Siirto |
|---|---|
| `w` | ylös |
| `a` | vasemmalle |
| `s` | alas |
| `d` | oikealle |

Virheellinen syöte tai siirto, joka ei muuta lautaa, ilmoitetaan eikä kuluta
vuoroa.

## Testien suorittaminen

Kaikki yksikkötestit voi ajaa komennolla:

```text
poetry run invoke test
```

Kattavuustestin ja HTML-raportin voi muodostaa komennoilla:

```text
poetry run invoke coverage
poetry run invoke coverage-report
```

Muita projektin Invoke-tehtäviä ovat:

```text
poetry run invoke lint
poetry run invoke format
```

`lint` tarkistaa lähdekoodin Pylintillä ja `format` muotoilee `src`-hakemiston
Autopep8:lla.
