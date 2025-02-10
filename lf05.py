#aufgabe2:

class Game:
    def __init__(self,titel,entwickler,erscheinungsjahr):
        self.titel=titel
        self.entwickler=entwickler
        self.erscheinungsjahr=erscheinungsjahr
        
    def __str__(self):
        return f"{self.titel} von {self.entwickler}({self.erscheinungsjahr})"
    
class GameLibary:
    def __init__(self):
        self.spiele = []
        
    def spiele_anzahl(self):
        return len(self.spiele)
    
    def spiel_hinzufuegen(self, spiel):
        self.spiele.append(spiel)
        
    def spiel_suchen(self, titel):
        for spiel in self.spiele:
            if spiel.titel.lower() == titel.lower():
                return f"Gefunden: {spiel}"
        return "Spiel nicht gefunden."
    
    def __str__(self):
        a = ""
        for i in self.spiele:
            a =a + i + "\n"
        return(a)
            

        #return "\n".join(str(spiel) for spiel in self.spiele)
    
    
#aufgabe3:
    
if __name__ == "__main__":
    GameLibary1 = GameLibary()
    
    spiel1 = Game("The a","Penis","Lecker")
    spiel2 = Game("The a","Schwanz","Lecker")
    GameLibary1.spiel_hinzufuegen(spiel1)
    GameLibary1.spiel_hinzufuegen(spiel2)

    print(GameLibary1)