class Titandex():
    def __init__(self, name, height,strength,winning_streak):
        self.name = name
        self.height = height
        self.strength=strength
        self.winning_streak= winning_streak
    
    
    def TitanvsScout(self):
        n=input("Enter the number of rounds: ")
        i=1
        while i<=int(n):
            scout_name=input("Enter your Scout Name: ")
            scout_strength=int(input("Enter your Scout strength: "))
            if (scout_strength==self.strength):
                print('It is a DRAW')
                self.winning_streak=0
                print('Winning streak for Titan is reset to ' + str (self.winning_streak))
            elif (scout_strength>self.strength):
                print(str(scout_name) + ' is the WINNER')
                self.winning_streak=0
                print('Winning streak for Titan is reset to'+ str (self.winning_streak))
            else:
                print(str(self.name) + ' is the WINNER')
                self.winning_streak+=1
                print('Winning streak for Titan is ' + str(self.winning_streak))
            i+=1
        else:print("Match Over")

    def TitanvsTitan(self):
        n=input("Enter the number of rounds: ")
        i=1
        while i<=int(n):
            Titan_name=input("Enter Titan 2 Name: ")
            if(self.name==Titan_name):
                print("Titan can't fight with itself")
                break
            else:
                Titan_strength=int(input("Enter Titan 2 strength: "))
                if (Titan_strength==self.strength):
                    print('It is a DRAW')
                    self.winning_streak=0
                    print('Winning streak for Titan 1 is reset to ' + str (self.winning_streak))
                elif (Titan_strength>self.strength):
                    print(str(Titan_name) + ' is the WINNER')
                    self.winning_streak=0
                    print('Winning streak for Titan 1 is reset to'+ str (self.winning_streak))
                else:
                    print(str(self.name) + ' is the WINNER')
                    self.winning_streak+=1
                    print('Winning streak for Titan 1 is ' + str(self.winning_streak))
                i+=1
        else:print("Match Over")
            

name_1=input("Enter your Titan Name: ")
height_1=input("Enter your Titan's height: ")
strength_1=int(input("Enter your Titan strength: "))
winning_streak=0
Titan_1=Titandex(name_1,height_1,strength_1,winning_streak)
Titan_1.TitanvsScout()
Titan_1.TitanvsTitan()





