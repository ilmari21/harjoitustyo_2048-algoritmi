# Vaatimusmäärittely

## Kuvaus
Tämä projekti on osa Helsingin yliopiston tietojenkäsittelytieteen kandiohjelman kurssia Aineopintojen harjoitustyö: Algoritmit ja tekoäly. Projekti toteutetaan Pythonilla (käyttämäni versio on 3.12.8) ja dokumentaation kielenä on suomi. Vertaisarviointia voin tehdä Pythonin lisäksi C#-kielellä tehtyihin projekteihin, sekä suomeksi että englanniksi.

## Aihe ja toteutus
Tässä harjoitustyössä tarkoitukseni on toteuttaa mukautetulla Expectiminimax-algoritmilla tekoäly, joka toimii [2048](https://en.wikipedia.org/wiki/2048_(video_game))-pelin päätöksenteon taustalla. Algoritmia mukautetaan toimimaan yksinpelinä kaksinpelin sijaan, jossa vastapelaaja korvataan pelin satunnaistapahtumilla.

## Ydin
Ydin on satunnaistapahtumia sisältävän pelin päätöksentekoalgoritmin toteuttaminen, sekä heuristisen arviointifunktion käyttö pelitilanteen arvioimisessa. Algoritmin tulee arvioida pelitilannetta useamman siirron eteenpäin, ottaa huomioon parhaat mahdolliset siirrot sekä pelin satunnaisen luonteen sekä satunnaistapahtumien todennäköisyydet. Algoritmi pyrkii maksimoimaan laattojen arvon ja sitä myöten kokonaispisteet, ilman että peli päättyy.
Bittitaulukoiden sekä hajautustaulukon käytöllä pyritään optimoimaan suorituskykyä.

## Tietorakenteet ja syöte
Tietorakenne toteutetaan 64-bittisenä bittitaulukkona, joka soveltuu hyvin pelilaudan 4x4-tilan tallentamiseen. Kukin 4 bittiä edustaa yhtä pelilaudan ruutua ($2^n$). Tallennettua pelitilaa käytetään syötteenä, jonka perusteella algoritmi selvittää parhaan mahdollisen siirtosuunnan. Tämän lisäksi käytetään hakutaulukkoja sekä hajautustaulua. 

## Aika- ja tilavaativuudet
Aikavaativuus Expectiminimax-haulla on $O((b \cdot n)^d)$, jossa b on mahdollisten siirtojen määrä kyseisellä vuorolla (ylös, alas, oikea, vasen eli $b \le 4$, n on mahdollisten satunnaistapahtumien määrä (tyhjät ruudut $\times$ mahdolliset arvot uudelle ruudulle) ja d on hakusyvyys. Hakutaulukoiden ja hajautustaulun tilavaativuus on O(1), sekä hakupuun rekursiopinon O(d), jossa d on hakusyvyys.

## Lähteet
* [Expectiminimax (Wikipedia)](https://en.wikipedia.org/wiki/Expectiminimax)
* [AI Plays 2048 (Stanford CS229 Report)](https://cs229.stanford.edu/proj2016/report/NieHouAn-AIPlays2048-report.pdf)
