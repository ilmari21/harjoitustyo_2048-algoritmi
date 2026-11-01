# Toteutusdokumentti

## Ohjelman yleisrakenne

Ohjelma toteuttaa 2048-pelin tekoälyn Pythonilla. Pelilauta on 4×4
-kokoinen, ja yksi ruutu tallennetaan neljän bitin lukuna. Luku ei ole
suoraan laatan arvo, vaan eksponentti: esimerkiksi arvot 1 ja 2 tarkoittavat
laattoja 2 ja 4. Koko lauta mahtuu näin yhteen 64-bittiseen kokonaislukuun.

Ohjelman keskeiset moduulit ovat:

* [`bitboard.py`](../src/bitboard.py) sisältää `Bitboard`-tietorakenteen,
  ruutujen lukemisen ja asettamisen, siirrot sekä pelin päättymisen
  tarkistamisen.
* [`move_logic.py`](../src/move_logic.py) tiivistää yhden neljän ruudun rivin,
  yhdistää samanarvoiset laatat ja täyttää jäljelle jäävät ruudut nollilla.
* [`lookup_tables.py`](../src/lookup_tables.py) muodostaa välimuistitetut
  hakutaulukot kaikille 16-bittisille riveille. Samaa rivimuunnosta ei siten
  tarvitse laskea uudelleen jokaisella siirrolla.
* [`heuristics.py`](../src/heuristics.py) arvioi pelilaudan. Arvio koostuu
  tyhjien ruutujen määrästä ja siksak-kuvion mukaisesta painotetusta
  laattasummasta. Päättyneelle täydelle laudalle annetaan suuri negatiivinen
  rangaistus.
* [`expectimax.py`](../src/expectimax.py) toteuttaa päätöksenteon. Max-solmu
  valitsee parhaan laillisen siirron ja chance-solmu laskee uusien laattojen
  odotusarvon. Uusi laatta on eksponentiltaan 1 todennäköisyydellä 0,9 ja
  eksponentiltaan 2 todennäköisyydellä 0,1. Hakusyvyys valitaan dynaamisesti
  tyhjien ruutujen määrän perusteella.
* [`game_2048.py`](../src/game_2048.py) vastaa pelin tilasta, satunnaisen
  uuden laatan lisäämisestä ja pisteiden laskemisesta.
* [`main.py`](../src/main.py) käynnistää tekoälypelin. Ihmispelaamista varten
  on lisäksi [`human_playtest.py`](../src/human_playtest.py).

### Siirron käsittely

Vaakasiirrossa neljä 16-bittistä riviä muunnetaan hakutaulukon avulla.
Pystysiirrossa jokainen neljästä sarakkeesta pakataan 16-bittiseksi arvoksi,
muunnetaan samalla tavalla ja puretaan takaisin laudalle. Siirrot ovat
immuuttisia: ne palauttavat uuden `Bitboard`-olion. Tämä helpottaa
hakupuun haarojen käsittelyä, koska yhden haaran muutokset eivät vaikuta
toisiin haaroihin.

### Expectimax-haku

`get_best_move` tyhjentää ensin transpositiotaulun ja tutkii kaikki lailliset
siirrot. Siirron jälkeen chance-solmu käy läpi kaikki tyhjät ruudut sekä
mahdolliset uudet laatat. Max- ja chance-solmut vuorottelevat, kunnes
hakusyvyys päättyy, jolloin lauta arvioidaan heuristiikalla. Hakusyvyys
ilmaisee pelaajan max-solmujen määrän hakupuussa. Koska `get_best_move`
käsittelee ensimmäisen max-solmun erikseen, hakusyvyydellä 2 hakupolku on
`max → chance → max` ja hakusyvyydellä 3 `max → chance → max → chance → max`.
Sama tila,
solmutyyppi ja hakusyvyys tallennetaan Pythonin sanakirjaan, jotta
hakupuussa toistuva tila voidaan käyttää uudelleen.

## Aika- ja tilavaativuudet

Merkitään seuraavia suureita:

* $b$ = mahdollisten pelaajan siirtojen enimmäismäärä, tässä $b \leq 4$
* $n$ = mahdollisten satunnaistapahtumien määrä eli tyhjien ruutujen
  määrä kerrottuna uuden laatan mahdollisilla arvoilla
* $d$ = hakusyvyys.

Yhden siirtotason jälkeen chance-solmulla on enintään $n$ lasta.
Tässä toteutuksessa $n \leq 16 \cdot 2 = 32$.
Siksi hakupuun karkea aikavaativuus on

$O((b \cdot n)^d)$.

Tämä on yläraja: käytännössä osa pelaajan siirroista on epäkelpoja, tyhjien
ruutujen määrä muuttuu ja transpositiotaulu poistaa toistuvia laskuja.
Jos 4×4 -laudan kokoa pidetään kiinteänä, sekä $b$ että $n$ ovat
vakioita. Tällöin itse hakusyvyydestä esitetty kasvu voidaan kirjoittaa
muodossa $O(c^d)$, missä $c$ on vakio, mutta $c^d$ kasvaa nopeasti.

Hakupuun ulkopuoliset operaatiot ovat 4×4 -laudan takia vakioaikaisia:

* ruudun lukeminen ja asettaminen ovat $O(1)$
* tyhjien ruutujen etsiminen on tässä toteutuksessa $O(16)=O(1)$
* yhden siirron laskeminen on hakutaulujen ansiosta $O(1)$
* heuristinen arvio käy läpi 16 ruutua, joten se on $O(16)=O(1)$.

Hakutaulut sisältävät neljä taulukkoa, joissa kussakin on 65 536
16-bittisen rivin muunnos. Niiden kertaluontoinen alustaminen vie
$O(4 \cdot 2^{16})$ aikaa ja tilaa, mikä on tämän kiinteän laudan
tapauksessa $O(1)$. Yleistettäessä laudat suuremmiksi tämä ei enää olisi
vakio.

Transpositiotaulun tilankäyttö on $O(s)$, missä $s$ on välimuistiin
tallennettujen erilaisten `(solmutyyppi, lauta, syvyys)`-avainten määrä.
Ilman välimuistin osumia $s$ voi olla hakupuun solmujen suuruusluokkaa,
enintään $O((b \cdot n)^d)$. Koska pelilauta on kiinteä 4×4 -lauta ja
hakusyvyys on rajattu, tämä vastaa käytännön toteutuksessa rajattua
tilankäyttöä eli määrittelydokumentin merkintää $O(1)$. Rekursiivinen
kutsupino käyttää lisäksi $O(d)$ tilaa.

## Suorituskykyvertailu

Suorituskykyä mitattiin [`expectimax_depth_benchmark.py`](../src/expectimax_depth_benchmark.py)
-ohjelmalla. Sama lähtölauta tutkittiin kolme kertaa kullakin hakusyvyydellä,
ja tuloksena raportoitiin ajoaikojen mediaani. Mittaus tehtiin kutsumalla
`get_best_move`-metodia ja hakutaulukot sekä transpositiotaulu olivat käytössä.

| Hakusyvyys | Mediaaniaika | Valittu siirto |
|---:|---:|---|
| 2 | 0,002 s | left |
| 3 | 0,042 s | left |
| 4 | 0,439 s | left |
| 5 | 3,068 s | left |
| 6 | 16,539 s | left |

Tulokset havainnollistavat eksponentiaalista kasvua: hakusyvyyttä kasvatettiin
kahdesta kuuteen vain neljä tasoa, mutta mediaaniaika kasvoi noin
8 000-kertaiseksi. Mittaus on suuntaa-antava, koska siinä käytettiin
yhtä lähtölautaa ja kolmea toistoa hakusyvyyttä kohti.

Hakutaulukot siirtävät rivien käsittelyn pois varsinaisesta hakusilmukasta.
Transpositiotaulu puolestaan vähentää saman tilan uudelleenlaskentaa.
Näiden optimointien hyöty näkyy käytännössä erityisesti suuremmilla
hakusyvyyksillä, vaikka ne eivät muuta hakupuun pahimman tapauksen
eksponentiaalista ylärajaa.

### Koko pelin mittaukset

Edellä kuvattu benchmark mittaa yhden siirron laskemista. Lisäksi algoritmia
ajettiin kokonaan pelin alusta pelin päättymiseen kymmenen kertaa kullakin
`min_depth-max_depth`-asetuksella. Alla olevissa tuloksissa aika, siirtojen
määrä ja pisteet ovat kymmenen ajon keskiarvoja. Asetuksissa `2-4`, `2-6` ja
`4-6` hakusyvyys valitaan pelin aikana dynaamisesti tyhjien ruutujen määrän
perusteella, joten ne eivät vastaa yhtä kiinteää hakusyvyyttä.

| Hakusyvyys (min-max) | Keskimääräinen aika | Keskimääräinen siirtojen määrä | Keskimääräinen pistemäärä |
|---|---:|---:|---:|
| 2-2 | 0:02 | 1 151 | 20 905 |
| 2-4 | 14:25 | 3 061 | 66 824 |
| 4-4 | 15:06 | 3 283 | 72 260 |
| 2-6 | 5:39:00 | 4 505 | 103 475 |
| 4-6 | 6:25:00 | 5 180 | 121 572 |

Tulokset tukevat sitä, että suurempi hakusyvyys parantaa pelin tulosta, mutta
kasvattaa suoritusaikaa voimakkaasti. `2-2`-ajoissa keskimääräinen pistemäärä
oli 20 905, kun taas `4-4`-ajoissa se oli 72 260. Asetukset `2-6` ja `4-6`
saavuttivat korkeammat keskiarvot, mutta `4-6` tuotti 121 572 pistettä ja
5 180 siirtoa ja yhden pelin keskimääräinen kesto oli yli kuusi tuntia.
Näistä tuloksista ei kuitenkaan voi päätellä, että parempi tulos johtuisi 
nimenomaan dynaamisesta syvyyden valinnasta. Asetuksilla `2-6` ja `4-6` on 
suurempi mahdollinen maksimihakusyvyys kuin asetuksilla `2-2` ja `4-4`, joten 
ero voi johtua ensisijaisesti syvemmästä hausta.

Tuloksia tulee pitää suuntaa-antavina. Pelin satunnaiset uudet laatat
aiheuttavat suurta vaihtelua, ja mittaukset tehtiin osittain eri käyttöjärjestelmissä
sekä eri laitteilla. Lisäksi osa `2-6`- ja `4-6`-ajoista oli
mittaushetkellä merkitty vielä käynnissä oleviksi, vaikka niistä oli saatavilla
pelin päättymiseen johtanut tulos. Vertailukelpoisempi koe vaatisi saman
laitteen, saman Python-ympäristön ja ennalta määrätyt satunnaissiementen arvot.
Lisäksi dynaamisen syvyyden
vaikutuksen erottamiseksi pitäisi verrata
esimerkiksi samoilla siemenillä asetuksia `2-4` ja `4-4` sekä erikseen
asetuksia `2-6` ja `4-6`. Näistä rajoitteista huolimatta mittaukset
havainnollistavat hyvin hakusyvyyden, pelin laadun ja suoritusajan välistä
kompromissia.

## Puutteet ja parannusehdotukset

* Heuristiikka käyttää vain tyhjien ruutujen määrää ja yhtä siksak-painotusta.
  Parempi tulos voisi olla saavutettavissa lisäämällä esimerkiksi
  monotonisuuden, vierekkäisten laattojen yhteensopivuuden ja suurimman
  laatan sijainnin arviointi.
* Nykyinen suorituskykymittaus ei vertaile hakutaulujen tai
  transpositiotaulun vaikutusta. Jatkossa voisi ajaa samat lähtötilat 
  useita kertoja sekä verrata optimointien kanssa ja ilman niitä.
* Hakusyvyyden enimmäisarvo on rajattu kuuteen, koska syvempi haku muuttuu
  nopeasti hitaaksi. Iteratiivinen syventäminen, aikaraja tai tehokkaampi
  rinnakkaisuus voisi tehdä hakusyvyyden käytöstä joustavampaa.
* Visuaalinen käyttöliittymä voisi helpottaa pelilaudan, siirtojen, pistemäärän 
  ja käytetyn hakusyvyyden seuraamista. Nykyinen toteutus toimii
  komentorivillä.

Algoritmin suorituskyky muodostui projektin merkittävimmäksi kehityskohteeksi, ja käytin sen optimointiin eniten aikaa. Mittaustulosten perusteella hakusyvyys 4 tarjosi parhaan kompromissin suoritusajan ja saavutetun pistemäärän välillä. Pienemmän hakusyvyyden kasvattaminen pelin aikana säästi vain vähän aikaa, ja aikaisemmat heikommat siirtovalinnat saattoivat vaikuttaa pelin myöhempiin tilanteisiin. Hakusyvyyttä 4 suuremmilla asetuksilla suoritusaika kasvoi huomattavasti. Näin ollen 4-4 valikoitui ohjelman oletushakusyvyydeksi. Vertailussa oletettiin, että algoritmi suoritetaan kullakin hakusyvyydellä kerran; nopeammalla hakusyvyydellä tehtyjen useampien suoritusten määrää ei suhteutettu yhden hakusyvyydellä 4 tehdyn suorituksen kestoon.

## Laajojen kielimallien käyttö

Tässä projektissa käytin Googlen Geminiä projektin suurten linjojen sekä työjärjestyksen hahmottamiseen, sekä GitHubin Copilotia ongelmien paikantamiseen koodissa sekä algoritmin suorituskyvyn parannusehdotuksiin. Copilotia käytin lisäksi auttamaan dokumentaation ja docstringien muotoilussa sekä kieliopillisten ja loogisten virheiden tarkistuksessa.

## Lähteet

Pääasiallisina lähteinä toimivat:

* [Expectiminimax, Wikipedia](https://en.wikipedia.org/wiki/Expectiminimax)
  — expectimax-hakupuun ja odotusarvon periaate.
* [AI Plays 2048, Stanford CS229 -raportti](https://cs229.stanford.edu/proj2016/report/NieHouAn-AIPlays2048-report.pdf)
  — 2048-pelin tekoälyssä käytettyjen hakujen ja heuristiikkojen tausta.

Lisäksi [Stack Overflow](https://stackoverflow.com/questions) ja [GeeksforGeeks](https://www.geeksforgeeks.org/) toimivat apuna useiden käytännön toteutusratkaisujen selvittämisessä.
