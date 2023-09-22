class Product:
    def __init__(self, kod, namn, pris):
        self.kod = kod
        self.namn = namn
        self.pris = pris
class Rabatt:
    def __init__(self, rabatt, datum):
        self.rabatt = rabatt
        self.datum = datum




produkter = {}

rabatter = {}















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

if __name__ == "__main::":
    try:
        with open("Produkter.txt", "r"):
            