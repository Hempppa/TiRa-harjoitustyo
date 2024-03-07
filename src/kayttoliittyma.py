"""Nimensä mukaan käyttöliittymään liittyvä tavara eli pääasiassa tulostaa pelikentän, mutta vastaa myös vuoron vaihtamisesta.
Muuten kutsuu vain muita funktioita.
"""
import time
from tekoaly import tekoalya, tekoalyb, arvioi_tilanne
from pelilogiikka import tee_siirto, kone_siirto, matti
#ns config asetukset, tästä voi pääasiassa vain aloitusvuoron vaihtaa, uusien nappuloidne tai
#pelilaudan koon vaihtaminen tässä versiossa rikkoo pelin
PELILAUTA = [["R","N","B","Q","K","B","N","R"],
            ["P","P","P","P","P","P","P","P"],
            ["-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-"],
            ["p","p","p","p","p","p","p","p"],
            ["r","n","b","q","k","b","n","r"]]
KAANNOSTAULU = {"p":chr(9817), "r":chr(9814), "n":chr(9816), "b":chr(9815), "q":chr(9813), "k":chr(9812),
                "P":chr(9823), "R":chr(9820), "N":chr(9822), "B":chr(9821), "Q":chr(9819), "K":chr(9818)}
TYHJA = "-"

#!!! Puuttuu vielä ohesta 

def alku():
    """Funktion kutsuminen käynnistää sovelluksen. Funktio kutsuu kaksin tai yksinpeliin liittyvän funktion.
    """
    print("Pelistä voi poistua kirjoittamalla quit")
    print("Peli ei tunnista ohestalyöntiä tai tornitusta")
    print("Siirrot syötetään muodossa x1 y1 x2 y2 eli d7d5. Korottamisen siirrolle lisää haluttu pelinappula perään, esim. d6d7Q tai d1d0p.")
    print("Korottamisessa käyettävät nappulat;")
    print(KAANNOSTAULU)
    while True:
        valinta = input("Kaksinpeli (2p) vai tekoalya vastaan (1p): ")
        if valinta in ("quit", "q"):
            break
        if valinta in ("2p", "2P", "2"):
            if kaksinpeli() == "quit":
                break
        if valinta in ("1p", "1P", "1"):
            if yksinpeli() == "quit":
                break

def yksinpeli():
    """Yksinpeli shakkibottia vastaan. Funktio vain kutsuu muita ja tulostaa pelikentän yms.

    Returns:
        string: palauttaa 'quit' jos se jossain kohtaa konsoliin vastataan
    """
    vuoro = 0
    pelitilanne = []
    valkoiset_syoty = []
    mustat_syoty = []
    for rivi in PELILAUTA:
        pelitilanne.append(rivi[:])
    while True:
        valinta = input("Aloittaako pelaaja [y] vai ei [n]? ")
        if valinta in ("quit", "q"):
            return "quit"
        if valinta in ("y", "Y"):
            pelaaja = 0
            aly_vuoro = 1
            break
        if valinta in ("n", "N"):
            pelaaja = 1
            aly_vuoro = 0
            break
    siirto = (0, "")
    while True:
        print()
        tulosta_peli(pelitilanne, valkoiset_syoty, mustat_syoty, pelaaja)
        print()

        print("Pelaajan", vuoro+1, "vuoro")
        tilanne = matti(pelitilanne, vuoro)
        if tilanne[0]:
            print()
            if tilanne[2]:
                print("Tasapeli")
            elif vuoro == 0:
                print("Tekoäly voitti!!!")
            else:
                print("Pelaaja voitti!!!")
            print()
            return ""
        siedettavammat = []
        for siirto in tilanne[1]:
            siedettavammat.append(chr(siirto[0]+97) + str(siirto[1]+1) + chr(siirto[2]+97) + str(siirto[3]+1))
        print("mahdolliset siirrot ", siedettavammat)
        if vuoro == pelaaja:
            siirtop = input("Syötä siirto: ")
            if siirtop in ("quit", "q"):
                return "quit"
            if siirtop in siedettavammat:
                pois = tee_siirto(pelitilanne, siirtop)
                if vuoro == 1:
                    if pois != TYHJA:
                        valkoiset_syoty.append(pois)
                    vuoro = 0
                else:
                    if pois != TYHJA:
                        mustat_syoty.append(pois)
                    vuoro = 1
            else:
                print("Laiton siirto")
        else:
            print()
            print("miettii.....")
            #Ennen looppia määrätään ensimmäisen iteraation syvyys ja tyhjä siirtotaulu joka annetaan tekoaly funktioille
            ihan_alku = time.time()
            syvyys = 1
            siirto_taulu = {}
            print("Syvyys: ...")
            while True:
                print(syvyys)
                alku_aika = time.time()
                if aly_vuoro == 1:
                    siirto = tekoalya(pelitilanne, syvyys, -5000000, 5000000, aly_vuoro, (0, ""), siirto_taulu)
                else:
                    siirto = tekoalyb(pelitilanne, syvyys, -5000000, 5000000, aly_vuoro, (0, ""), siirto_taulu)
                loppu_aika = time.time()
                #Jos aikaa iteraation laskemiseen kesti yli kokonaisluvun osoittama määrä sekunneissa niin looppi katkaistaan
                if loppu_aika-alku_aika > 5:
                    break
                    #
                syvyys += 1
            ihan_loppu = time.time()
            #
            print("Valmis! siirto; ", siirto[0], siirto[1])
            print("Aikaa miettimiseen kului: ", ihan_loppu-ihan_alku, "s")
            print("Iteraatioita: ", syvyys)
            if siirto[1] in tilanne[1]:
                pois = kone_siirto(pelitilanne, siirto[1])
                if vuoro == 1:
                    if pois != TYHJA:
                        valkoiset_syoty.append(pois)
                    vuoro = 0
                else:
                    if pois != TYHJA:
                        mustat_syoty.append(pois)
                    vuoro = 1
            else:
                print("Tekoäly rikki!!! Sori, laita palautetta jossain jotenkin, mieluusti pelitilanteen kera")
                return "quit"

def kaksinpeli():
    """Pelimuoto missä kaksi pelaajaa pelaa toisiaan vastaan. Tämä funktio vain vaihtaa vuoroja ja kutsuu muita funktioita

    Returns:
        String: voi palauttaa vain 'quit' jolloin pelin suoritus pysähtyy. Jos mitään ei palauteta niin sovelluksen suoritus jatkuu
    """
    vuoro = 0
    pelitilanne = []
    valkoiset_syoty = []
    mustat_syoty = []
    for rivi in PELILAUTA:
        pelitilanne.append(rivi[:])
    while True:
        print()
        tulosta_peli(pelitilanne, valkoiset_syoty, mustat_syoty, vuoro)
        print()
        arvio = arvioi_tilanne(pelitilanne, [], [])
        print("Pelikenttä arvio: ", arvio/100)
        print("Pelaajan", vuoro+1, "vuoro")
        tilanne = matti(pelitilanne, vuoro)
        siedettavammat = []
        for siirto in tilanne[1]:
            siedettavammat.append(chr(siirto[0]+97) + str(siirto[1]+1) + chr(siirto[2]+97) + str(siirto[3]+1))
        if tilanne[0]:
            print()
            if tilanne[2]:
                print("Tasapeli")
            elif vuoro == 0:
                print("Pelaaja 2 voitti!!!")
            else:
                print("Pelaaja 1 voitti!!!")
            print()
            return ""
        print("mahdolliset siirrot ", siedettavammat)
        siirto = input("Syötä siirto: ")
        if siirto in ("quit", "q"):
            return "quit"
        if siirto in siedettavammat:
            pois = tee_siirto(pelitilanne, siirto)
            if vuoro == 1:
                if pois != TYHJA:
                    mustat_syoty.append(pois)
                vuoro = 0
            else:
                if pois != TYHJA:
                    valkoiset_syoty.append(pois)
                vuoro = 1
        else:
            print("Laiton siirto")

def tulosta_peli(pelitilanne, valkoiset_syoty, mustat_syoty, suunta):
    if suunta == 0:
        print("  --------------------")
        for y in range(8):
            rivi = str(y+1) + " |"
            for x in range(8):
                if pelitilanne[y][x] == TYHJA:
                    if (x+y)%2 == 0:
                        rivi += " " + chr(9633)
                    else:
                        rivi += " " + chr(9639)
                else:
                    rivi +=  " " + KAANNOSTAULU[pelitilanne[y][x]]
            print(rivi + "  |")
        print("  --------------------")
        print("    a b c d e f g h")
        print()
        ms = ""
        for merkki in mustat_syoty:
            ms += KAANNOSTAULU[merkki] + " "
        vs = ""
        for merkki in valkoiset_syoty:
            vs += KAANNOSTAULU[merkki] + " "
        print(ms)
        print(vs)
    else:
        kaannetty = []
        for rivi in pelitilanne:
            temp = rivi[:]
            temp.reverse()
            kaannetty.append(temp)
        kaannetty.reverse()
        print("  --------------------")
        for y in range(8):
            rivi = str(8-y) + " |"
            for x in range(8):
                if kaannetty[y][x] == TYHJA:
                    if (x+y)%2 == 0:
                        rivi += " " + chr(9633)
                    else:
                        rivi += " " + chr(9639)
                else:
                    rivi +=  " " + KAANNOSTAULU[kaannetty[y][x]]
            print(rivi + "  |")
        print("  --------------------")
        print("    h g f e d c b a")
        print()
        ms = ""
        for merkki in mustat_syoty:
            ms += KAANNOSTAULU[merkki] + " "
        vs = ""
        for merkki in valkoiset_syoty:
            vs += KAANNOSTAULU[merkki] + " "
        print(vs)
        print(ms)
    print()
    arvio = arvioi_tilanne(pelitilanne, [], [])
    print("Pelikenttä arvio: ", arvio, " (ns. centipawn)")