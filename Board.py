import random
import re

# GENERAL GAME SETTINGS:
# 1. Board size. Length of aplphabet list below sets size of the board. From "A" to "J" board size is 10 x 10 cells
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']#, 'K', 'L', 'M', 'N'] 

# 2. Fleet configuration. First numbers in list below are ship sizes, second numbers are number of ships 
fleet_config = [[4, 1], [3, 2], [2, 3], [1, 4]]  

# 3. Ship class names. In dictionaries below  
ship_class_names = {4: "Battleship", 3: "Cruiser", 2: "Destroyer", 1: "Torpedo boat"}

# 4. Space factor. Defines the size of spaces between cells
space_factor = 2

class Board:

    def __init__(self, player_name):
        self.player_name = player_name
        self.array = generate_empty_board_array()
        self.size = len(self.array)
        self.fleet_array = []
    
    def __repr__(self) -> str:
        return self.id
    
    def show(self):
        string = "\n" * space_factor
        for row in self.array:
            for cell in row:
                string += cell + " " * space_factor
            string += "\n" * space_factor
        print(string)

    def place_ship(self, ship_size, begining_coord_and_direction, manual_input = True):
        
        x, y = coordinates_from_string(begining_coord_and_direction)
        direction = ship_direction_from_string(begining_coord_and_direction)

        if direction == "S":
            x_d = 0
            y_d = 1
        elif direction == "N":
            x_d = 0
            y_d = -1
        elif direction == "W":
            x_d = -1
            y_d = 0
        elif direction == "E":
            x_d = 1
            y_d = 0
        else:
            if manual_input:
                print("ERROR: Wrong ship direction!!")
                input("Press any key to continue")
            return False

        ship_array = []

        for i in range(ship_size):

            if x <= self.size-1 and y <= self.size-1 and x > 0 and y > 0:
                if self.array[y][x] == "H":
                    if manual_input:
                        print("ERROR: Intersection with existing ship!!")
                        input("Press any key to continue")
                    return False
                else:
                    ship_array.append([x,y])
            else:
                if manual_input:
                    print("ERROR: Coordinates go beyond the board limits!!")
                    input("Press any key to continue")
                return False
            
            x += x_d
            y += y_d

        for i in range(ship_size):
            self.array[ship_array[i][1]][ship_array[i][0]] = "H"

        self.fleet_array.append(ship_array)
        return True

    def place_fleet(self):
        message = "OK. Allow the first player " + self.player_name + " to secretly place his fleet. Try not to peek)"
        print("\n")
        print(message)
        self.show()
        for ship in fleet_config:
            
            for n in range(ship[1]):
                
                while not self.place_ship(ship[0], str(input("Input begining coordinates and heading of the ship: "))):
                    pass
                clear()
                print(message)
                self.show()
             
        print("All ships are on positions.")
        print(self.fleet_array)
        return (self.fleet_array)

    def place_fleet_random(self):
        for ship in fleet_config:
            
            for n in range(ship[1]):
                
                while not self.place_ship(ship[0], random.choice(alphabet) + str(random.randint(1, 10)) + random.choice(['N', 'E', 'S', 'W']), False):
                    pass
        clear()
        self.show()
             
        print("All ships are on positions.")
        print(self.fleet_array)
        return (self.fleet_array)


    def shot(self, coord):
        x, y = coordinates_from_string(coord)
        self.array[y][x] = 'X'




def generate_empty_board_array():
    
    array = ["  "]
    array.extend(alphabet)
    array = [array] 
    
    for i in range(len(alphabet)):
        
        if (i+1) < 10: 
            row = [" " + str(i+1)]
        else: 
            row = [str(i+1)]

        for i in range(len(alphabet)):
            row += "~"   
        array.append(row)
    
    return array

def coordinates_from_string(string):
        string = string.strip().upper()

        ints  = re.findall("\d+",string) # one or more digits
        strings = re.findall("[A-Z]+",string) # one or more uppercase  letters 

        x = alphabet.index(strings[0]) + 1
        y = int(ints[0])
        return x, y

def ship_direction_from_string(string):
    string = string.strip().upper()
    strings = re.findall("[A-Z]+",string) # one or more uppercase  letters
    if len(strings) == 1:
        return 'N'
    elif len(strings) == 2:
        return strings[1]