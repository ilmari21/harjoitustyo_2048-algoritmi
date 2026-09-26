# Käyttöohje

Projektin voi ladata [täältä](https://github.com/ilmari21/harjoitustyo_2048-algoritmi) klikkaamalla **Source code**.

## Sovelluksen käytön aloitus

1. Asenna poetry:

```
poetry install
```
tämä saattaa johtaa virheilmoitukseen "The current project could not be installed...", alustamisen pitäisi silti kuitenkin onnistua. Voit myös käyttää komentoa
```
poetry install --no-root
```
jolloin virheilmoitusta ei pitäisi tulla.
```

2. Sovelluksen käynnistäminen:

Algoritmin voi suorittaa komennolla:

```
poetry run invoke start
```

Peliä voi myös itse pelata komennolla:

```
poetry run invoke play
```
