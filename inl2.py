class Produkt:
    def __init__(self, kod, namn, pris):
        self.kod = kod
        self.namn = namn
        self.pris = pris

class ProduktManager:
    def __init__(self):
        self.produkter = {}
    def lägg_till_produkt(self, kod, namn, pris):
            ny_produkt = Produkt(kod, namn, pris)
            self.produkter[kod] = ny_produkt
            self.data['produkter'][kod] = {'namn': namn, 'pris': pris}
            print(f"Varan {ny_produkt.namn} har lagts till med produktkoden {kod}")
            spara_data_till_fil(data, "Produkter.txt")
    def ta_bort_produkt(self, kod):
        if kod in self.produkter:
            borttagen_produkt = self.produkter[kod].namn
            del self.produkter[kod]
            del self.data['produkter'][kod]
            print(f"Varan {borttagen_produkt} med produktkod {kod} har tagits bort")
            spara_data_till_fil(data, "Produkter.txt")
        
    def visa_varor(self):
        for kod, produkt in self.produkter.items():
            print(f"Produktkod: {kod}")
            print(f"Namn: {produkt.namn}")
            print(f"Pris: {produkt.pris} kr")
            print("-"*20)
class RabattManager:
    def __init__(self, data):
        self.data = data
        self.produkter = data['rabatter']
    def ny_rabatt(self):
        pass
    def uppdatera_rabatt(self):
        pass
    def visa_rabatt(self):
        pass
class KvittoManager:
    def __init__(self, produkter_data):
        self.köpta_saker = []
        self.produkter_data = produkter_data
    def lägg_till_varor(self, kod, namn, pris, antal):
        saker = {
            'kod': kod,
            'namn': namn,
            'pris': pris,
            'antal': antal
        }
        self.köpta_saker.append(saker)
    def skriv_ut_kvitto(self):
        print("Kvitto:")
        total_kostnad = 0
        for item in self.köpta_saker:
            subtotal = item['pris'] * item['antal']
            total_kostnad += subtotal
            print(f"Namn: {item['kod']}")
            print(f"Pris per styck: {item['pris']} kr")
            print(f"Antal: {item['antal']}")
            print(f"Delsumma: {subtotal} kr")
        print(f"Total Kostnad : {total_kostnad} kr")
def spara_data_till_fil(data, filnamn):
    with open(filnamn, "w") as fil:
        for key, items in data.items():
            for item_key, item_value in items.items():
                fil.write(f"{key}: {item_key}\n")
                if isinstance(item_value, dict):
                    for attr, value in item_value.items():
                        fil.write(f"   {attr}: {value}\n")
def ladda_data_från_fil(data, filnamn):
    with open(filnamn, "r") as fil:
        lines = fil.readlines()
        key = None
        for line in lines:
            if line.startswith("produkter") or line.startswith("rabatter"
                            ) or line.startswith("kvitton"):
                key = line.strip().split(":")[0]
            if key:
                item_key, item_value = line.strip().split(": ")
                data[key][item_key] = item_value
def kundmeny():
    ny_kund_manager = KvittoManager(data['produkter'])
    while True:
        print("Kundmeny")
        print("1. Lägg till varor")
        print("2. Avsluta kund")
        n_c = input("Vad vill du göra?: ")

        if n_c == "1":


def main_meny():
    while True:
        print("Välkommen")
        print("1. Ny kund")
        print("2. Lägg till/Ta bort varor")
        print("3. Lägg till rabatt")
        print("4. Avsluta")
        c = input("Vad vill du göra?: ")

        if c == "1":
            kundmeny()
        elif c=="2":
            print("1. Lägga till varor")
            print("2. Ta bort varor")
            n_c = input("Vill du lägga till eller ta bort? ")
            if n_c == "1":
                try:
                    namn = input("Namn på varan du lägger till: ")
                    kod = int(input("Välj produktkod för varan: "))
                    pris = float(input("Pris på varan?: "))
                except ValueError:
                    print("Felaktig Inmatning. Ange Heltal för produktkod och pris")
                    continue
                produkter_manager.lägg_till_produkt(kod, namn, pris)
            if n_c == "2":            
                produkter_manager.visa_varor()
                try:
                    kod = int(input("Skriv produktkoden på varan som ska tas bort: "))
                except ValueError:
                        print("Error: Välj ett heltal som produktkod.")
                produkter_manager.ta_bort_produkt(kod)

        elif c=="3":
            pass
        elif c=="4":
            break
        else:
            pass


if __name__ == "__main__":
    data = {'produkter': {},
        'rabatter': {},
        'kvitton': {},
     }
    produkter_manager = ProduktManager(data)
    rabatter_manager = RabattManager(data)
    kvitto_manager = KvittoManager(data)
    ladda_data_från_fil(data, "Produkter.txt")
    ladda_data_från_fil(data, "Rabatter.txt")
    ladda_data_från_fil(data, "Kvitton.txt")
    main_meny()
    
            