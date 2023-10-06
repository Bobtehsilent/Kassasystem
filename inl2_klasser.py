class Produkt:
    def __init__(self, produktid, pris, namn):
        self.namn = namn
        self.produktid = produktid
        self.pris = pris

class Kampanj:
    def __init__(self, produkt, nytt_pris, start_datum, slut_datum) -> None:
        self.produkt = produkt
        self.nytt_pris = nytt_pris
        self.start_datum = start_datum
        self.slut_datum = slut_datum

class Lager:
    def __init__(self) -> None:
        self.produkter = {}
        self.kampanjer = {}
        self.kvittonummer = 1
    
    def lägg_till_produkt(self, produkt):
        self.produkter[produkt.produktid] = produkt
    def ta_bort_produkt(self, produktid):
        if produktid in self.produkter:
            del self.produkter[produktid]
    
    def lägg_till_kampanj(self, kampanj):
        if kampanj.produkt.produktid not in self.kampanjer:
            self.kampanjer(kampanj.produkt.produktid)
