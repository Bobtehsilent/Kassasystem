import datetime
import os
#Konstanter av filer
PRODUKT_FIL = "produkt.txt"
KAMPANJ_FIL = "kampanjer.txt"
KVITTO_FIL = "kvitton.txt"

class Produkt:
    def __init__(self, produkt_kod, namn, pris):
        self.produkt_kod = produkt_kod
        self.namn = namn
        self.pris = pris

class Kampanj:
    def __init__(self, produkt, start_datum, slut_datum, nytt_pris) -> None:
        self.produkt = produkt
        self.start_datum = start_datum
        self.slut_datum = slut_datum
        self.nytt_pris = nytt_pris

class Lager:
    def __init__(self) -> None:
        self.produkter = {}
        self.kampanjer = {}
        self.kvitto_nummer = 1
    
    def lägg_till_produkt(self, produkt):
        self.produkter[produkt.produkt_kod] = produkt

    def ta_bort_produkt(self, produkt_kod):
        if produkt_kod in self.produkter:
            del self.produkter[produkt_kod]
    
    def lägg_till_kampanj(self, kampanj):
        if kampanj.produkt.produkt_kod not in self.kampanjer:
            self.kampanjer[kampanj.produkt.produkt_kod] = []
        self.kampanjer[kampanj.produkt.produkt_kod].append(kampanj)
    def ta_bort_kampanj(self, produkt_kod, kampanj):
        if produkt_kod in self.kampanjer and kampanj in self.kampanjer[produkt_kod]:
            self.kampanjer[produkt_kod].remove(kampanj)

class Köp:
    def __init__(self) -> None:
        self.items = []
    def lägg_till_vara(self, produkt, antal):
        self.items.append({"produkt": produkt, "antal": antal})
    def lägg_vara_i_korgen(self, lager):
        köpval = input("Gör ditt val (1-2): ")
        if köpval == "1":
            while True:
                print("<produktkod><spacebar><antal>")
                produkt_input = input("Skriv in produktkod och antal som ovan eller PAY för att betala: ").strip().upper()# noqa: E501
                if "PAY" in produkt_input:
                    if self.items:
                        total = Betala().räkna_total(self)
                        Betala().skriv_kvitto(self, total)
                        spara_kvitton(KVITTO_FIL, self, total)
                        nuvarande_köp = None
                        break
                    else:
                        print("Det finns inga varor i korgen att betala för.")
                        continue
                delar = produkt_input.strip().split()
                if len(delar) != 2:
                    print("Felaktigt Format. Försök igen")
                    continue
                produkt_kod, antal = delar
                produkt_kod = int(produkt_kod)
                produkt = lager.produkter.get(produkt_kod)
                if produkt:
                    try:
                        int(produkt_kod)
                        antal = int(antal)
                        if antal > 0:
                            nuvarande_köp.lägg_till_vara(produkt, antal)
                            subtotal = produkt.pris * antal
                            print(f"{antal} {produkt.namn} har lagts till i korgen för {subtotal} kr")  # noqa: E501
                        else:
                            print("Antalet måste vara större än 0.")
                    except ValueError:
                            print("Antalet måste vara ett heltal.")
                else:
                    print(f"Produkt med kod {produkt_kod} hittades inte")
        elif köpval == "2":
            return
        else:
            print("Ogiltigt val. Försök igen.")

class Betala:
    def __init__(self, lager) -> None:
        self.lager = lager
    def räkna_total(self, köp):
        total = 0
        for item in köp.items:
            produkt = item["produkt"]
            antal = item["antal"]
            total += produkt.pris * antal
        return total
    def skriv_kvitto(self, köp, total):
        kvitto_datum = datetime.date.today()
        print(f"Kvitto ({kvitto_datum})")
        for item in köp.items:
            produkt = item["produkt"]
            antal = item["antal"]
            subtotal = produkt.pris * antal
            print(f"Produkt: {produkt.namn}")
            print(f"Antal: {antal}")
            print(f"Pris: {produkt.pris} kr")
            print(f"Delsumma: {subtotal} kr")
            print("-"*50)
        print(f"Totalt att betala: {total} kr")

class Administrering:
    def __init__(self, lager) -> None:
        self.lager = lager
    def ändra_produkt(self, produkt_kod, nytt_namn, nytt_pris):
        produkt = self.lager.produkter.get(produkt_kod)
        if produkt:
            produkt.namn = nytt_namn
            produkt.pris = nytt_pris
        else:
            print(f"Produkt med kod {produkt_kod} hittades inte.")
    def ny_produkt(self, produkt):
        if produkt.produkt_kod not in self.lager.produkter:
            self.lager.lägg_till_produkt(produkt)
        else:
            print(f"Produkt med kod {produkt.produkt_kod} finns redan.")
    def ta_bort_produkt(self, produkt_kod):
        self.lager.ta_bort_produkt(produkt_kod)
    def ny_kampanj(self, kampanj):
        self.lager.lägg_till_kampanj(kampanj)
    def ta_bort_kampanj(self, produkt_kod, kampanj):
        self.lager.ta_bort_kampanj(produkt_kod, kampanj)

def ladda_produkter(filnamn, lager):
    try:
        with open(filnamn, "r") as fil:
            lines = fil.readlines()
            for line in lines:
                delar = line.strip().split()
                if len(delar) == 3:
                    produkt_kod, namn, pris = delar
                    produkt = Produkt(produkt_kod, namn, float(pris))
                    lager.lägg_till_produkt(produkt)
    except FileNotFoundError:
        print(f"Filen '{filnamn}' kunde inte hittas")

def spara_produkter(filnamn, lager):
    with open(filnamn, "w") as fil:
        for produkt_kod, produkt in lager.produkter.items():
            fil.write(f"{produkt_kod} {produkt.namn} {produkt.pris}\n")

def ladda_kampanjer(filnamn, lager):
    try:
        with open(filnamn, "r") as fil:
            lines = fil.readlines()
            for line in lines:
                delar = line.strip().split()
                if len(delar)==4:
                    produkt_kod, start_datum, slut_datum, nytt_pris = delar
                    produkt = lager.produkter.get(produkt_kod)
                    if produkt:
                        kampanj = Kampanj(produkt, datetime.date.fromisoformat(start_datum), datetime.date.fromisoformat(slut_datum), float(nytt_pris))  # noqa: E501
                        lager.lägg_till_kampanj(kampanj)
    except FileNotFoundError:
        print(f"Filen '{filnamn}' kunde inte hittas")
def spara_kampanjer(filnamn, lager):
    with open(filnamn, "w") as fil:
        for produkt_kod, kampanjer in lager.kampanjer.items():
            for kampanj in kampanjer:
                fil.write(f"{produkt_kod} {kampanj.start_datum} {kampanj.slut_datum} {kampanj.nytt_pris}\n")  # noqa: E501

def spara_kvitton(filnamn, köp, total):
    with open(filnamn, "a") as fil:
        fil.write("Kvitto:\n")
        for item in köp.items:
            fil.write("-"*100)
            fil.write(f"Produkt: {item['produkt'].namn}\n")
            fil.write(f"Antal: {item['antal']}\n")
            fil.write(f"Pris: {item['produkt'].pris} kr\n")
            fil.write(f"Delsumma: {item['produkt'].pris * item['antal']} kr\n")
            fil.write("-"*100)

def main():
    lager = Lager()
    administrera = Administrering(lager)
    ladda_produkter(PRODUKT_FIL, lager)
    print(lager.produkter)
    ladda_kampanjer(KAMPANJ_FIL, lager)
    print(lager.kampanjer)
    nuvarande_köp = None
    while True:
        print("-"*40)
        print("Huvudmeny")
        print("1. Börja ett köp")
        print("2. Lägg till/ta bort produkter")
        print("3. Lägg till/ta bort kampanjer")
        print("4. Spara och stäng ner")
        print("-"*40)
        val = input("Gör ditt val (1-4): ")
        if val == "1":
            nuvarande_köp = Köp()
            while True:
                print("-"*40)
                print("Handlingsmeny")
                print("1. Lägg till en vara\n2. Tillbaks till huvudmenyn")
                print("-"*40)
                nuvarande_köp.lägg_vara_i_korgen(lager)
        elif val == "2":
            while True:
                print("-"*40)
                print("Produktadministration")
                print("1. Lägg till produkt\n2. Ta bort produkt\n3. Tillbaka till huvudmenyn")  # noqa: E501
                print("-"*40)
                produktval = input("Gör ditt val (1-3): ")
                if produktval == "1":
                    produkt_kod = input("Ange Produktkod: ")
                    namn = input("Ange Produktnamn: ")
                    pris = float(input("Ange pris: "))
                    produkt = Produkt(produkt_kod, namn, pris)
                    administrera.ny_produkt(produkt)
                    print(f"{namn} har lagts till i produktlagret")
                elif produktval == "2":
                    produkt_kod = input("Ange produktkoden som ska tas bort: ")
                    administrera.ta_bort_produkt(produkt_kod)
                    print(f"Produkten med kod {produkt_kod} har tagits bort.")
                elif produktval == "3":
                    spara_produkter(PRODUKT_FIL, lager)
                    break
                else:
                    print("Ogiltigt val. Försök igen")
        elif val == "3":
            while True:
                print("-"*40)
                print("Kampanjadministration")
                print("1. Lägg till kampanj\n2. Ta bort kampanj\n3. Tillbaka till huvudmenyn")  # noqa: E501
                print("-"*40)
                kampanjval = input("Gör ditt val (1-3): ")
                if kampanjval == "1":
                    produkt_kod = input("Ange produktkod: ")
                    produkt = lager.produkter.get(produkt_kod)
                    if produkt:
                        start_datum = input("Ange startdatum (YYYY-MM-DD): ")
                        slut_datum = input("Ange slutdatum (YYYY-MM-DD): ")
                        nytt_pris = float(input("Ange rabatterat pris: "))
                        kampanj = Kampanj(produkt, datetime.date.fromisoformat(start_datum), datetime.date.fromisoformat(slut_datum), nytt_pris)  # noqa: E501
                        administrera.ny_kampanj(kampanj)
                        print(f"Kampanj för {produkt.namn} har lagts till")
                    else:
                        print(f"Produkt med koden {produkt_kod} hittades inte.")
                if kampanjval == "2":
                    produkt_kod = input("Ange produktkod: ")
                    produkt = lager.produkter.get(produkt_kod)
                    if produkt:
                        start_datum = input("Ange startdatum för kampanjen som ska tas bort: ")  # noqa: E501
                        kampanjer = lager.kampanjer.get(produkt_kod, [])
                        for kampanj in kampanjer:
                            if kampanj.start_datum.strftime("%y-%m-%d") == start_datum:
                                administrera.ta_bort_kampanj(produkt_kod, kampanj)
                                print(f"Kampanj för {produkt.namn} har tagits bort.")
                        else:
                            print(f"Ingen kampanj hittades för {produkt.namn} med startdatum {start_datum}")  # noqa: E501
                    else:
                        print(f"Produkt med kod {produkt_kod} hittades inte.")
                elif kampanjval == "3":
                    break
        elif val == "4":
            spara_kampanjer(KAMPANJ_FIL, lager)
            spara_produkter(PRODUKT_FIL, lager)
            print("Programmet har sparat och stänger nu ner.")
            break
        else:
            print("Ogiltigt val. Försök igen")
if __name__ == "__main__":
    if not os.path.isfile(PRODUKT_FIL) or not os.path.isfile(KAMPANJ_FIL):
        with open(PRODUKT_FIL, "w"):
            #Pass bara för att öppna sen fortsätta.
            pass
        with open(KAMPANJ_FIL, "w"):
            pass
    main()

