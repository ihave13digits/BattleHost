from os import path
from random import randint, choice, seed

from terms import Term
T = Term()

def get_bot_data():
    import json
    data = {}
    with open(path.join('res', 'config.json'),"r") as f:
        data = json.loads(f.read())
    return data[T.b_token], data[T.b_owner], data[T.b_prefix], data[T.b_seed]



def clamp(n, minv, maxv):
    return max(min(maxv, n), minv)

def get_index(x, y, w):
    return y * w + x

def coords(x, y):
    return '{}-{}'.format(x, y)



def get_drops(m):
    data = {}
    choices = []
    count = 0
    for drop in T.drops[m]:
        data[drop] = 0
        for i in range(T.drops[m][drop]):
            choices.append(drop)
            count += 1
    for d in range(count):
        data[choice(choices)] += 1
    return data



def can_move(x, y, w):
    data = False
    if ((x >= 0 and x < w) and
        (y >= 0 and y < w)):
        data = True
    return data



def new_client(x, y):
    data = {
            T.i : ' ',
            T.c : 25000,
            T.s : 0,
            T.p : [0, 0],
            T.P : [x, y],
            T.v : [],
            T.a : {},
            T.I : {},
            T.S : {
                T.s_move : False,
                }
            }
    for a in T.ammo:
        data[T.a][a] = 0
    for i in T.item:
        data[T.I][i] = 0
    return data

def new_vessel(s):
    data = {
            T.n : s,
            T.i : [],
            T.p : [0, 0],
            T.P : [0, 0],
            T.r : 'n'
            }
    for cell in T.ship[s][1]:
        data[T.i].append(cell)
    return data



def rotate_matrix(mtrx, w):
    rot = []
    for y in range(w):
        for x in range(w):
            rot.append(0)
    for y in range(w):
        for x in range(w):
            rot[get_index(y, x, w)] = mtrx[get_index(x, y, w)]
    return rot

def avrg_matrix(mtrx, f=int):
    return f(sum(mtrx.values())/len(mtrx))

def blend_matrix(mtrx):
    blnd = []
    MAX = len(T.tile)-1
    w = T.chunk
    for y in range(w):
        for x in range(w):
            BLND = []
            for j in range(-T.chunk_y, T.chunk_y):
                for i in range(-T.chunk_x, T.chunk_x):
                    v = round( ((mtrx[get_index(x, y, w)][0]) + (mtrx[get_index(i, j, w)][0])) / 2 )
                    BLND.append(v+randint(-1, 1))
            bv = 0
            for v in BLND:
                bv += v
            bv = int(bv/len(BLND))
            blnd.append(clamp(bv, 0, MAX))
    return blnd

def blend_values(mtrx, w, W, H):
    blnd = []
    MAX = len(T.tile)-1
    for y in range(w):
        for x in range(w):
            BLND = []
            for j in range(-H, H):
                for i in range(-W, W):
                    cmn = round( ((mtrx[get_index(x, y, w)][0]) + (mtrx[get_index(i, j, w)][0])) / 2 )
                    cmx = round( ((mtrx[get_index(x, y, w)][1]) + (mtrx[get_index(i, j, w)][1])) / 2 )
                    BLND.append([cmn, cmx+randint(1, 5)])
            bv = 0
            bV = 0
            for v in BLND:
                bv += v[0]
                bV += v[1]
            bv = int(bv/len(BLND))
            bV = int(bV/len(BLND))
            blnd.append([clamp(bv, 0, MAX), clamp(bV, 0, MAX)])
    return blnd

def new_chunk(mn, mx):
    data = {}
    vals = []
    for y in range(T.chunk):
        for x in range(T.chunk):
            cmn = randint(0, mn)
            cmx = randint(mn, mx)
            cmn = clamp(cmn, 0, cmx)
            vals.append([cmn, cmx])
    for o in range(T.octs):
        blnd = blend_values(vals, T.chunk, T.chunk_x, T.chunk_y)
    blndd = blend_matrix(blnd)
    for y in range(T.chunk):
        for x in range(T.chunk):
            data[coords(x, y)] = blndd[get_index(x, y, T.chunk)]
    return data

def generate_world(sd):
    w = T.world
    seed(sd)
    data = {}
    MAX = len(T.tile)
    vals = []
    for y in range(T.world):
        for x in range(T.world):
            mn = randint(0, int(MAX*T.r_low))
            mx = randint(int(MAX*T.r_high), MAX)
            vals.append([mn, mx])
    blnd = vals
    for B in range(T.OCTS):
        blnd = blend_values(blnd, T.world, T.world_x, T.world_y)
        T.loaded += 1
        show_progress('Generating World Values')
    for y in range(T.world):
        for x in range(T.world):
            data[coords(x, y)] = {}
            data[coords(x, y)][T.o] = ''
            data[coords(x, y)][T.m] = new_chunk(
                    vals[get_index(x, y, T.world)][0], 
                    vals[get_index(x, y, T.world)][1])
            T.loaded += 1
            show_progress('Building Chunks')
    return data

def show_progress(txt):
    prcnt = 100*T.loaded/T.complete
    print('{}{} {:.1f}%\n|{}{}|'.format('\n'*64, txt, prcnt, '.'*int(prcnt), ' '*(100-int(prcnt))))



class BattleHost:

    def __init__(self, seed):
        self.seed = seed
        self.players = {}
        self.matrix = {}
        


    def generate_maps(self, sd):
        from time import time
        start = time()
        self.matrix = generate_world(sd)
        self.generate_minimap()
        stop = time()
        params = 'Seed: {}\n'.format(sd)
        params += 'Dimensions:\n  World: ({},{})\n  Chunk: ({},{})\n'.format(T.world, T.world, T.chunk, T.chunk)
        params += 'World Octaves: {}\n  Blend Area: ({},{})\n'.format(T.OCTS, T.world_x, T.world_y)
        params += 'Chunk Octaves: {}\n  Blend Area:({},{})\n'.format(T.octs, T.chunk_x, T.chunk_y)
        print(self.get_minimap())
        print("\nGenerating and blending {} tiles took {} seconds with parameters:\n\n{}".format(int((T.world*T.world)*(T.chunk*T.chunk)), stop-start, params))

    def generate_minimap(self):
        mini = []
        for y in range(T.world):
            for x in range(T.world):
                v = avrg_matrix(self.matrix[coords(x, y)][T.m])
                mini.append(v)
        self.matrix[T.mm] = mini

    def add_player(self, player):
        ID = str(player)
        if not (ID in self.players):
            message = "Welcome, {}"
            p = [randint(0, T.world-1), randint(0, T.world-1)]
            tries = 1
            MAX = T.world*T.world
            while self.matrix[coords(p[0], p[1])][T.o] != '':
                p = [randint(0, T.world-1), randint(0, T.world-1)]
                tries += 1
                if tries >= MAX:
                    message = "Sorry, {}.  The battlefield is full."
                    break
            if tries < MAX:
                self.players[ID] = new_client(p[0], p[1])
                self.matrix[coords(p[0], p[1])][T.o] = ID
            
            return message

    def player_quit(self,  player):
        ID = str(player)
        if ID in self.players:
            for x in range(T.world):
                for y in range(T.world):
                    if self.matrix[coords(x, y)][T.o] == ID:
                        self.matrix[coords(x, y)][T.o] = ''
            del(self.players[ID])
            return "Goodbye, {}"

    def player_symbol(self, player, img):
        self.players[player][T.i] = img



    def save_data(self, sd):
        import pickle
        data = {T.world_data : self.matrix, T.player_data : self.players}
        try:
            with open(path.join(T.data_dir, sd),'wb') as f:
                pickle.dump(data, f)
                f.close()
        except:
            from os import mkdir
            mkdir(T.data_dir)
            self.save_data(sd)

    def load_data(self, sd):
        import pickle
        data = {}
        try:
            with open(path.join(T.data_dir, sd), 'rb') as f:
                data = pickle.load(f)
                f.close()
        except:
            self.generate_maps(self.seed)
        if data:
            self.matrix = data[T.world_data]
            self.players = data[T.player_data]



    def buy_material(self, player, m, *a):
        count = 0
        amnt = 1
        if a:
            amnt += int(a[0])-1
        for s in range(amnt):
            if self.players[player][T.c] >= T.item[m]:
                self.players[player][T.I][m] += 1
                self.players[player][T.c] -= T.item[m]
                count += 1
            else:
                amnt -= 1
        if count == 0 or count > 1:
            plr = 's'
        return "You purchased {} {} for {}".format(count, m, count*T.item[m])

    def sell_material(self, player, m, *a):
        count = 0
        amnt = 1
        if a:
            amnt += int(a[0])-1
        for s in range(amnt):
            if self.players[player][T.I][m] > 0:
                self.players[player][T.I][m] -= 1
                self.players[player][T.c] += T.item[m]
                count += 1
            else:
                amnt -= 1
        if count == 0 or count > 1:
            plr = 's'
        return "You sold {} {} for {}".format(count, m, count*T.item[m])



    def buy_ammo(self, player, A, *a):
        plr = ''
        count = 0
        amnt = 1
        if a:
            amnt += int(a[0])-1
        for prch in range(amnt):
            if self.players[player][T.c] >= T.ammo[A][0]:
                count += 1
                self.players[player][T.c] -= T.ammo[A][0]
                self.players[player][T.a][A] += 1
        if count == 0 or count > 1:
            plr = 's'
        msg = "You purchased {} {}{}.".format(count, A, plr)
        return msg

    def buy_ship(self, player, S, *a):
        plr = ''
        count = 0
        amnt = 1
        if a:
            amnt += int(a[0])-1
        for prch in range(amnt):
            if self.players[player][T.c] >= T.ship[S][0]:
                count += 1
                self.players[player][T.c] -= T.ship[S][0]
                self.players[player][T.v].append(new_vessel(S))
                self.players[player][T.s] = len(self.players[player][T.v])-1
                self.place_ship(player)
        if count == 0 or count > 1:
            plr = 's'
        msg = "You purchased {} {}{}.".format(count, S, plr)
        return msg

    def buy_zone(self, player, x, y):
        message = 'You purchased zone at coordinates ({}, {})'.format(x, y)
        if coords(x, y) in self.matrix:
            if self.players[player][T.c] >= T.chunk_value:
                if self.matrix[coords(x, y)][T.o] == '':
                    self.players[player][T.c] -= T.chunk_value
                    self.matrix[coords(x, y)][T.o] = player
                else:
                    message = 'This zone is already owned'
            else:
                message = 'You need {} currency to purchase that'.format(T.chunk_value)
        else:
            message = 'Invalid Request: ({},{})'.format(x, y)
        return message



    def get_area(self, player, A):
        data = []
        size = round(T.ammo[A][0]*.5)
        x, y = self.players[player][T.p][0], self.players[player][T.p][1]
        if size >= 1:
            for j in range(-size+1, size):
                for i in range(-size+1, size):
                    if ((x+i >= 0 and x+i < T.chunk) and
                        (y+j >= 0 and y+j < T.chunk)):
                        ofst = get_index(x+i, y+j, T.chunk)
                        data.append(ofst)
        else:
            data.append(get_index(x, y, T.chunk))
        
        debug = ''
        for Y in range(T.chunk):
            for X in range(T.chunk):
                if X % T.chunk == 0:
                    debug += '\n'
                cell = '--'
                i = get_index(X, Y, T.chunk)
                for h in data:
                    if i == h:
                        cell = '[]'
                debug += '{}'.format(cell)
        print(debug)

        return data

    def take_damage(self, player, v, atk, dmg):
        x, y = self.players[player][T.v][v][T.p][0], self.players[player][T.v][v][T.p][1]
        size = int(T.img*.5)
        for i in range(-size, size+1):
            for j in range(-size, size+1):
                ship_index = get_index(x+i, y+j, T.chunk)
                if ship_index == atk:
                    self.players[player][T.v][v][T.i][get_index(i+size, j+size, T.img)] = clamp(
                            self.players[player][T.v][v][T.i][get_index(i+size, j+size, T.img)]-dmg, 0, 4)

    def attack_ship(self, player, X, Y, A):
        if self.matrix[coords(X, Y)][T.o] != '':
            own = self.matrix[coords(X, Y)][T.o]
            if self.players[player][T.a][A] > 0:
                self.players[player][T.a][A] -= 1
                
                dmg = T.ammo[A][2]
                area = self.get_area(player, A)
                for atk in area:
                    for v, V in enumerate(self.players[own][T.v]):
                        if ((self.players[own][T.v][v][T.P][0] == X) and
                            (self.players[own][T.v][v][T.P][1] == Y)
                                ):
                            self.take_damage(own, v, atk, dmg)
                        hp = 0
                        for val in self.players[player][T.v][v][T.i]:
                            hp += val
                        if hp <= 0:
                            del(self.players[player][T.v][v])

    def place_ship(self, player):
        size = int(T.img*.5)
        sel = self.players[player][T.s]
        X, Y = self.players[player][T.P][0], self.players[player][T.P][1]
        x, y = self.players[player][T.p][0], self.players[player][T.p][1]
        if x < size: x += size
        if x > T.chunk-size: x -= size
        if y < size: y += size
        if y > T.chunk-size: y -= size
        self.players[player][T.v][sel][T.P][0] = X
        self.players[player][T.v][sel][T.P][1] = Y
        self.players[player][T.v][sel][T.p][0] = x
        self.players[player][T.v][sel][T.p][1] = y

    def rotate_ship(self, player, r):
        d = {
                'n':{'n' : 0, 's' : 2, 'e' : 3, 'w' : 1},
                's':{'n' : 2, 's' : 0, 'e' : 1, 'w' : 3},
                'e':{'n' : 1, 's' : 3, 'e' : 0, 'w' : 2},
                'w':{'n' : 3, 's' : 1, 'e' : 2, 'w' : 0}
            }
        sel = self.players[player][T.s]
        new_img = []

        for itr in range(d[self.players[player][T.v][sel][T.r]][r]):
            new_img = rotate_matrix(self.players[player][T.v][sel][T.i], T.img)

        self.players[player][T.v][sel][T.r] = r
        self.players[player][T.v][sel][T.i] = new_img



    def step_player(self, player, x, y):
        if self.matrix[coords(self.players[player][T.P][0]+x, self.players[player][T.P][1]+y)][T.o] == player:
            self.players[player][T.P][0] = clamp(self.players[player][T.P][0]+x, 0, T.world-1)
            self.players[player][T.P][1] = clamp(self.players[player][T.P][1]+y, 0, T.world-1)

    def step_cursor(self, player, x, y):
        self.players[player][T.p][0] = clamp(self.players[player][T.p][0]+x, 0, T.chunk-1)
        self.players[player][T.p][1] = clamp(self.players[player][T.p][1]+y, 0, T.chunk-1)



    def modify_chunk(self, player, value, mode):
        X, Y = self.players[player][T.P][0], self.players[player][T.P][1]
        x, y = self.players[player][T.p][0], self.players[player][T.p][1]
        count = 0
        if mode == T.c_mine:
            value = clamp(value, 0, self.matrix[coords(X, Y)][T.m][coords(x, y)])
            while count < value:
                self.matrix[coords(X, Y)][T.m][coords(x, y)] -= 1
                self.players[player][T.I][T.collect[count]] += 1
                count += 1
            message = 'You mined {} units of earth'.format(count)
        if mode == T.c_pile:
            value = clamp(value, 0, (len(T.tile)-1)-self.matrix[coords(X, Y)][T.m][coords(x, y)])
            while count < value:
                if self.players[player][T.I][T.collect[count]] > 0:
                    self.matrix[coords(X, Y)][T.m][coords(x, y)] += 1
                    self.players[player][T.I][T.collect[count]] -= 1
                    count += 1
                else:
                    value -= 1
            message = 'You used {} units of earth'.format(count)
        return message

    def refine_material(self, player, m, *a):
        data = get_drops(m)
        self.players[player][T.I][m] -= 1
        if a:
            for i in range(int(a[0])-1):
                if self.players[player][T.I][m] > 0:
                    itr = get_drops(m)
                    for d in itr:
                        data[d] += itr[d]
                        self.players[player][T.I][m] -= 1
        response = 'Collected:'
        for drop in data:
            response += '\n  {}: {}'.format(drop, data[drop])
            self.players[player][T.I][drop] += data[drop]
        return response



    def show_chunk(self, X, Y):
        data = self.overlay_chunk(X, Y)
        field = '   '
        for x in range(T.chunk):
            if x % 2 == 0:
                field += '{}{}'.format(' '*(2-len(str(x))), x)
            else:
                field += '  '
        y = 0
        for i, cell in enumerate(data):
            if i % T.chunk == 0:
                if y % 2 == 0:
                    field += '\n{}{} '.format(' '*(2-len(str(y))), y)
                else:
                    field += '\n   '
                y += 1
            field += cell
        field += "\n"
        return field

    def get_minimap(self):
        data = []
        for y in range(T.world):
            for x in range(T.world):
                val = self.matrix[T.mm][get_index(x, y, T.world)]
                if self.matrix[coords(x, y)][T.o] != '':
                    player_tile = self.players[self.matrix[coords(x, y)][T.o]][T.i]
                    data.append('{}{}'.format(T.tile[val][0], player_tile))
                else:
                    val = self.matrix[T.mm][get_index(x, y, T.world)]
                    data.append(T.tile[val])

        for player in self.players:
            x, y = self.players[player][T.P][0], self.players[player][T.P][1]
            data[get_index(x, y, T.world)] = '[]'
        
        field = '   '
        for x in range(T.world):
            if x % 2 == 0:
                field += '{}{}'.format(' '*(2-len(str(x))), x)
            else:
                field += '  '
        y = 0
        for i, d in enumerate(data):
            if i % T.world == 0:
                if y % 2 == 0:
                    field += '\n{}{} '.format(' '*(2-len(str(y))), y)
                else:
                    field += '\n   '
                y += 1
            field += d

        return field

    def get_chunk(self, X, Y):
        data = []
        for y in range(T.chunk):
            for x in range(T.chunk):
                data.append(T.tile[self.matrix[coords(X, Y)][T.m][coords(x, y)]])
        return data

    def overlay_chunk(self, X, Y):
        size = int(T.img*.5)
        data = self.get_chunk(X, Y)
        player = self.matrix[coords(X, Y)][T.o]
        for vessel in range(len(self.players[player][T.v])):
            if (self.players[player][T.v][vessel][T.P][0] == X and
                self.players[player][T.v][vessel][T.P][1] == Y):
                for y in range(T.img):
                    for x in range(T.img):
                        try:
                            if self.players[player][T.v][vessel][T.i][get_index(x, y, T.img)] != 0:
                                vx, vy = self.players[player][T.v][vessel][T.p][0], self.players[player][T.v][vessel][T.p][1]
                                i = get_index(x+vx-size, y+vy-size, T.chunk)
                                data[i] = T.part[self.players[player][T.v][vessel][T.i][get_index(x, y, T.img)]].format(
                                        T.dirs[self.players[player][T.v][vessel][T.r]][0])
                        except:
                            pass
        i = get_index(self.players[player][T.p][0], self.players[player][T.p][1], T.chunk)
        data[i] = '[]'
        return data



