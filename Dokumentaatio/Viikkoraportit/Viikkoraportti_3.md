# Viikkoraportti 3
Kolmannella viikolla keskityin pelilogiikan ja bittitaulukon luomiseen, sekä asensin testaukseen vaadittavia työkaluja. Olemassa olevien ominaisuuksien yksikkötestejä en vielä saanut valmiiksi.

Tällä viikolla opin mm. käyttämään Pythonin functools.cache-dekoraattoria: tässä yhteydessä siten, että hakutaulukot lasketaan kerran, ja myöhemmät siirrot käyttävät valmista tulosta, jolloin samoja 65 536 rivimuunnosta ei tarvitse laskea uudestaan.

Suurimmat epäselvyydet liittyvät tällä hetkellä Expectimaxin toteutukseen Pythonissa sekä siihen, minkälaisella heuristiikalla pelitilannetta on mielekkäintä arvioida.

Ensi viikolla pyrin saamaan pelilogiikasta puuttuvat ominaisuudet valmiiksi, teen yksikkötestit ja testikattavuuden raportoinnin sekä siirryn itse expectimax-algoritmin toteutukseen.

Aikaa käytin projektin parissa tällä viikolla yhteensä n. 14 tuntia.
