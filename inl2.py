import os
class ProduktManager:
    def __init__(self):
        pass
    def ny_kund(self):
        pass
    def lägg_till_produk(self):
        pass
    def visa_varor(self):
        pass
class RabattManager:
    def __init__(self):
        pass
    def ny_rabatt(self):
        pass
    def uppdatera_rabatt(self):
        pass
    def visa_rabatt(self):
        pass
class KvittoManager:
    def __init__(self):
        pass
    def skapa_kvitto(self):
        pass
    def lägg_till_varor(self):
        pass
    def skriv_ut_kvitto(self):
        pass

def spara_data_till_fil(data, filnamn):
    with open(filnamn, "w") as fil:
        for key, items in data.items():
            for item_key, item_value in items.items():
                fil.write(f"{key}: {item_key}\n")
                for attr, value in vars(item_value).items():
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

produkter_manager = ProduktManager()
rabatter_manager = RabattManager()
kvitto_manager = KvittoManager()
def main_meny():
    while True:
        print("Välkommen")
        print("1. Ny kund")
        print("2. Lägg till produkt")
        print("3. Lägg till rabatt")
        print("4. Avsluta")
        c = input("Vad vill du göra?: ")

        if c == "1":
            pass
        elif c=="2":
            pass
        elif c=="3":
            pass
        elif c=="4":
            pass
        else:
            pass


if __name__ == "__main__":
    data = {'produkter': {},
            'rabatter': {},
            'kvitton': {},
     }
    spara_data_till_fil(data, "Produkter.txt")
    spara_data_till_fil(data, "Rabatter.txt")
    spara_data_till_fil(data, "Kvitton.txt")

    ladda_data_från_fil(data, "Produkter.txt")
    ladda_data_från_fil(data, "Rabatter.txt")
    ladda_data_från_fil(data, "Kvitton.txt")
    main_meny()
    
            