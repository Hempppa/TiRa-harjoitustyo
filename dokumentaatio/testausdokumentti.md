## Miten testit on tehty
Yksikkötestejä pääosin. Näitä on toteutettu sekä itse pelilogiikasta vastaaville funktioille (shakin tarkastus, siirtojen laskeminen, yms.) sekä tekoälyyn liittyville funktioille (ainakin itse minimaxi sekä heuristinen shakkitilanteen arviointi) tosin näitä on vähän vaikeata erottaa toisistaan, mm. tekoäly tarvitsee jonkun funktion kaikkien laillisten siirtojen palauttamiseen. 

Yksikkötestit ovat mielestäni riittävän kattavat kaikille funktioille lukuunottamatta tekoalylle jolla on vaikeata testata muuta kuin, että funktio palauttaa laillisen siirron ja toimii ääritilanteissa sekä voittaa jos taattu voitto on laskentasyvyyden sisällä. Shakkibotin siirtojen hyvyyttä siis pääasiassa testataan vaan pelaamalla sitä vastaan. 

Testaamatta jätän myös varmaan kokonaan 'käyttöliittymän' eli funktiot alku(), yksinpeli() ja kaksinpeli() jotka siis vain käyttäjän syötteen mukaan kutsuvat pelilogiikkaa ja tekoälyä toteuttavia funktioita, sekä tulostavat pelikentän. Käyttöliittymä on siis testattu vain suorittamalla peliä, sillä kaikki mihin käyttöliittymä vaikuttaa (kenen vuoro on, pelikentän tulostus ja peli_id siirtäminen funktiolta toiselle) näkyvät helposti konsoliin tulostuksesta.
## Kattavuusraportti
![Kattavuusraportti!](https://github.com/Hempppa/TiRa-harjoitustyo/blob/main/dokumentaatio/Screenshot%20from%202024-03-08%2018-57-42.png)

Tämän voi siis alla olevilla komennoilla itse suorittaa ja avaamalla selaimella index.html tiedoston saa auki rivittäin jäsennellyn näkymän testikattavuudesta
## Miten testit ja kattavuusraportin saa itse suoritettua
Testit löytyvät app_test.py tiedostosta, testauksen voi suorittaa komennolla:

	pytest

Ja kattavuusraportin saa komennoilla:

	coverage run -m pytest
 	coverage html

Jolloin htmlcov/index.html löytyy tarkka jäsentely testikattavuudesta
