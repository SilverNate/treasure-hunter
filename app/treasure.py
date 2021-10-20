import random, os

class TreasureHunter:
    jumlah_treasure = 0
    map_data = []
    posisi_user = []
    posisi_jalan = []
    posisi_treasure = []
    option = {
        1: 'Print Map',
        2: 'Print Map with Treasure',
        3: 'Print Treasure Position',
        4: 'Re-position of Treasure',
        5: 'Play Time!',
        0: 'Exit'
    }

    def __init__(self):
        f = open("treasure_map.txt", 'r')
        self.maps = f.read()
        self.map_data = []

        for corX in self.maps.split('\n'):
            mapped = []
            for corY in corX:
                mapped.append(corY)
            self.map_data.append(mapped)

    def load_game(self, jumlah_treasure=1):
        self.jumlah_treasure = jumlah_treasure
        self.load_coordinate()
        self.load_treasure(jumlah_treasure)
        self.pick_option()

    def pick_option(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for op in self.option.keys():
            print(str(op) + ' : ' + self.option[op])

        input_option = int(input('Option :'))

        if input_option == 1:
            self.print_maps(treasure=False)

        if input_option == 2:
            self.print_maps(treasure=True)

        if input_option == 3:
            print(self.posisi_treasure)

        if input_option == 4:
            self.input_treasure()

        if input_option == 5:
            self.play_game()

        if input_option == 0:
            exit()

        input('Press any key to return back')
        return self.pick_option()

    def play_game(self):
        self.print_maps(treasure=False, clear=False)
        self.print_maps(treasure=True, clear=False)
        print('Treasure position : '+ str(self.posisi_treasure))

        posX = self.posisi_user[0][0]
        posY = self.posisi_user[0][1]

        moving_operation = []
        moving_operation.append(['up/north','UP',False])
        moving_operation.append(['right/east','RIGHT',True])
        moving_operation.append(['down/south','DOWN',True])

        result = None

        for operation in moving_operation:
            result = self.set_updated_coordinate(posX, posY, operation[0], operation[1], operation[2])
            
            if result:
                posX = result[0]
                posY = result[1]
            else:
                break

        if result and result in self.posisi_treasure:
            print('Congratz, You just found the treasure ...')
        elif result:
            print('Nothing here, try again ...')
        else:
            print('Road is blocked...')

    def set_updated_coordinate(self, posX, posY, pos_text='up/north', pos='UP', ignore_wall=True):
        posCombine = [posX,posY]
        possible_count = '0-'+str(self.count_coordinate_possibily(posCombine,pos=pos,ignore_wall=ignore_wall))
        moving = input(pos_text+' ('+possible_count+'):')

        is_blocked = self.is_route_blocked(posCombine,int(moving),pos)

        if is_blocked:
            return None

        add = int(moving)
        
        if pos == 'UP':
            posX -= add
        elif pos == 'RIGHT':
            posY += add
        elif pos == 'DOWN':
            posX += add

        return [posX,posY]

    def is_route_blocked(self, coordinate, move, pos = 'UP'):
        posX = coordinate[0]
        posY = coordinate[1]

        for add in range(1,move+1):
            if pos == 'UP':
                posX = coordinate[0] - add
            elif pos == 'RIGHT':
                posY = coordinate[1] + add
            elif pos == 'DOWN':
                posX = coordinate[0] + add

            if posX < 0 or posX > len(self.map_data) or posY <0 or posY > len(self.map_data[0]):
                return True

            if self.map_data[posX][posY] == '#':
                return True
        return False

    def count_coordinate_possibily(self, coordinate, pos = 'UP', ignore_wall=True):
        found = 0
        move = 1
        posX = 0
        posY = 0
        
        while True:
            if pos == 'UP':
                posX = coordinate[0]-move
                posY = coordinate[1]
            if pos == 'RIGHT':
                posX = coordinate[0]
                posY = coordinate[1]+move
            if pos == 'DOWN':
                posX = coordinate[0]+move
                posY = coordinate[1]

            # if position is negative of more than length of array then break
            if posX < 0 or posY < 0 or posX >= len(self.map_data) or posY >= len(self.map_data[0]):
                if ignore_wall:
                    move -= 3
                break
            
            # if target position is not possible road then break
            if ignore_wall:
                if self.map_data[posX][posY] == '.' or self.map_data[posX][posY] == '$' or self.map_data[posX][posY] == '#':
                    found +=1
            else:
                if self.map_data[posX][posY] == '#':
                    break
                if self.map_data[posX][posY] == '.' or self.map_data[posX][posY] == '$':
                    found +=1
            move +=1
        
        return found

    '''
        print map
        treasure : show position of all treasure with $ symbol
    '''
    def print_maps(self, treasure=False, clear=True):
        if clear:
            os.system('cls' if os.name == 'nt' else 'clear')
        
        if treasure:
            print('>> Map With Treasure <<')
        else:
            print('>> Map <<')

        for rows in range(len(self.map_data)):
            output = ''
            for column in range(len(self.map_data[0])):
                if treasure and [rows,column] in self.posisi_treasure:
                    output += '$'
                else:
                    output += self.map_data[rows][column]
            print(output)
    
    '''
        load coordinate for avaiable road and position of user
        
        X = User Position
        . = Avaiable position
        
        if user position not found, we generated random user
        if user have more than 1 position, we will discard others
    '''
    def load_coordinate(self):
        for row in range(len(self.map_data)):
            for column in range(len(self.map_data[row])):
                if self.map_data[row][column] == 'X':
                    self.posisi_user.append([row,column])
                if self.map_data[row][column] == '.':
                    self.posisi_jalan.append([row,column])
        
        if len(self.posisi_user) == 0:
            posT = random.randint(0, len(self.posisi_jalan)-1)
            
            pX = self.posisi_jalan[posT][0]
            pY = self.posisi_jalan[posT][1]
            
            self.map_data[pX][pY] = 'X'
            self.posisi_user.append([pX,pY])

        # if user more than 1
        if len(self.posisi_user) > 1:
            temp_post = []
            temp_post.append(self.posisi_user[0])
            
            for pos in range(1,len(self.posisi_user)):
                pX = self.posisi_jalan[pos][0]
                pY = self.posisi_jalan[pos][1]
                
                self.map_data[pX][pY] = '.'
            
            self.posisi_user = temp_post

    '''
        Generate random treasure position by input
        
        num : number of treasure
    '''
    def load_treasure(self, num):
        # if num > possible road count, then num = length of possible road array
        if num > len(self.posisi_jalan):
            num = len(self.posisi_jalan)
            
        while not len(self.posisi_treasure) == num:
            # Generated random number
            posT = random.randint(0, len(self.posisi_jalan)-1)
            
            if not posT in self.posisi_treasure:
                self.posisi_treasure.append(self.posisi_jalan[posT])

    def input_treasure(self):
        treasure_count = input('Treasure Count (empty: default 1) :')
        self.posisi_treasure = []
        
        if not treasure_count == '':
            self.jumlah_treasure = int(treasure_count)
            
        self.load_treasure(self.jumlah_treasure)
        self.print_maps(treasure=True, clear=False)
        
