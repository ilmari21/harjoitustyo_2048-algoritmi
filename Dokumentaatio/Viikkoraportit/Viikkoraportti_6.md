# Viikkoraportti 6
Kuudennella viikolla keskityin parantamaan sekä testaamaan algoritmin suorituskykyä, pääasiallisesti luomalla dynaamisen hakusyvyyden ja optimoimalla pullonkauloina toimivia funktioita. Jonkin verran aikaa kului myös testien luomiseen, mutta ne jäivät vielä kesken. Invoke taskien tulisi nyt myös tukea eri alustoja (testasin itse Linuxin lisäksi Windowsilla). Tein myös joitain pienempiä parannuksia koodin laatuun perustuen pylint-raporttiin.

Opin käyttämään Pythonin cProfile-moduulia, jonka avulla sain tehokkaasti paikannettua algoritmini pullonkauloja ja parannettua suorituskykyä. Moduuli avulla voidaan mm. nähdä, kuinka monesti kutakin funktiota kutsutaan ja kuinka kauan näiden suorittamisessa menee.

Kysymyksiä minulla on lähinnä testauksen suhteen, eli minkälaiset testit tähän projektiin sopisivat parhaiten. Tahtoisin myös testata algoritmin suorituskykyä, mutta jotta saisi hyvän otannan tilastojen laskemiseksi, olisi testejä suoritettava niin monta, että aikaa algoritmin suorittamiseen alusta loppuun kymmenia tai satoja kertoja kuluisi hyvin paljon, ainakin nykyisellä nopeudella. Mietin, mikä olisi mielekkäin tapa testata algoritmia, kuten lähteenä olevassa Stanfordin tutkimuksen taulukoissa I-IV on testattu. 

Seuraavalla viikolla keskityn laajentamaan testausta ja dokumentaatiota, sekä mahdollisesti edelleen parantamaan suorituskykyä.

Aikaa käytin projektin parissa tällä viikolla yhteensä n. 12 tuntia.
