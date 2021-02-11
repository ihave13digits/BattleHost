from os import path
from random import randint, seed

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



def can_move(x, y, w):
    data = False
    if ((x >= 0 and x < w) and
        (y >= 0 and y < w)):
        data = True
    return data



def new_client(x, y):
    data = {
            T.c : 100000,
            T.s : 0,
            T.p : [0, 0],
            T.P : [x, y],
            T.v : [],
            T.a : {
                T.a_0 : 0,
                T.a_1 : 0,
                T.a_2 : 0
                },
            T.S : {
                T.s_move : False,
                }
            }
    return data

def new_vessel(s):
    data = {
            T.n : s,
            T.i : T.ship[s][1],
            T.p : [0, 0],
            T.P : [0, 0],
            T.r : 'n'
            }
    return data



def avrg_matrix(mtrx):
    avrg = 0
    for v in mtrx:
        avrg += mtrx[v]
    avrg = round(avrg/len(mtrx))
    return avrg

def blend_matrix(mtrx):
    blnd = []
    MAX = len(T.tile)
    w = T.chunk
    for y in range(w):
        for x in range(w):
            BLND = []
            for j in range(-1, 1):
                for i in range(-1, 1):
                    v = round( ((mtrx[get_index(x, y, w)][0]) + (mtrx[get_index(i, j, w)][0])) / 2 )
                    BLND.append(v+randint(-1, 1))
            bv = 0
            for v in BLND:
                bv += v
            bv = int(bv/len(BLND))
            blnd.append(clamp(bv, 0, MAX))
    return blnd

def blend_values(mtrx, w):
    blnd = []
    MAX = len(T.tile)
    for y in range(w):
        for x in range(w):
            BLND = []
            for j in range(-1, 1):
                for i in range(-1, 1):
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
    avrg = 0
    for y in range(T.chunk):
        for x in range(T.chunk):
            cmn = randint(0, mn)
            cmx = randint(mn, mx)
            cmn = clamp(cmn, 0, cmx)
            vals.append([cmn, cmx])

    for o in range(T.octs):
        blnd = blend_values(vals, T.chunk)
    blnd = blend_matrix(vals)
    for y in range(T.chunk):
        for x in range(T.chunk):
            data[coords(x, y)] = blnd[get_index(x, y, T.chunk)]
    return data

def generate_world(sd):
    w = T.world
    seed(sd)
    data = {}
    MAX = len(T.tile)
    vals = []

    for y in range(T.world):
        for x in range(T.world):
            mn = randint(0, int(MAX*.96))
            mx = randint(int(MAX*.98), MAX)
            mn = clamp(mn, 0, mx)
            vals.append([mn, mx])
    
    blnd = vals
    for B in range(T.OCTS):
        blnd = blend_values(blnd, T.world)

    for y in range(T.world):
        for x in range(T.world):
            data[coords(x, y)] = new_chunk(
                    vals[get_index(x, y, T.world)][0], 
                    vals[get_index(x, y, T.world)][1])
    
    return data



class BattleHost:

    def __init__(self):
        self.players = {}
        self.matrix = {}
        
    def start(self, sd):
        self.generate_map(sd)
        self.make_minimap()



    def make_minimap(self):
        mini = []
        for y in range(T.world):
            for x in range(T.world):
                v = avrg_matrix(self.matrix[coords(x, y)])
                mini.append(v)
        self.matrix[T.mm] = mini

    def generate_map(self, sd):
        self.matrix = generate_world(sd)

    def add_player(self, player):
        ID = str(player)
        if not (ID in self.players):
            p = [randint(0, T.world-1), randint(0, T.world-1)]
            self.players[ID] = new_client(p[0], p[1])
            return "Welcome, {}"

    def player_quit(self,  player):
        ID = str(player)
        if ID in self.players:
            del(self.players[ID])
            return "Goodbye, {}"



    def save_data(self):
        import pickle
        data = {T.world_data : self.matrix, T.player_data : self.players}
        try:
            with open(T.data_dir, 'wb') as f:
                pickle.dump(data, f)
                f.close()
        except:
            pass

    def load_data(self):
        import pickle
        data = {}
        try:
            with open(T.data_dir, 'rb') as f:
                data = pickle.load(f)
                f.close()
        except:
            pass
        self.matrix = data[T.world_data]
        self.players = data[T.player_data]



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



    def attack_ship(self, player, A):
        if self.players[player][T.a][A] > 0:
            dmg = T.ammo[A][2]
            X, Y = self.players[player][T.P][0], self.players[player][T.P][1]
            x, y = self.players[player][T.p][0], self.players[player][T.p][1]
            for p in self.players:
                for v, vessel in enumerate(self.players[p][T.v]):
                    for i in range(T.img):
                        for j in range(T.img):
                            if self.players[p][T.v][v][T.i][get_index(i, j, T.img)] != 0 and (
                                    (self.players[p][T.v][v][T.P][0] == X and self.players[p][T.v][v][T.P][1] == Y) and
                                    (self.players[p][T.v][v][T.p][0] == x and self.players[p][T.v][v][T.p][1] == y)):
                                    
                                    print('hit')
                                    self.players[p][T.v][v][T.i][get_index(i, j, 5)] = clamp(self.players[p][T.v][v][T.i][get_index(i, j, 5)]-dmg, 0, 4)

    def place_ship(self, player):
        sel = self.players[player][T.s]
        self.players[player][T.v][sel][T.P][0] = self.players[player][T.P][0]
        self.players[player][T.v][sel][T.P][1] = self.players[player][T.P][1]
        self.players[player][T.v][sel][T.p][0] = self.players[player][T.p][0]
        self.players[player][T.v][sel][T.p][1] = self.players[player][T.p][1]

    def rotate_ship(self, player, r):
        sel = self.players[player][T.s]
        self.players[player][T.v][sel][T.r] = r



    def step_player(self, player, x, y):
        self.players[player][T.P][0] = clamp(self.players[player][T.P][0]+x, 0, T.world-1)
        self.players[player][T.P][1] = clamp(self.players[player][T.P][1]+y, 0, T.world-1)

    def step_cursor(self, player, x, y):
        self.players[player][T.p][0] = clamp(self.players[player][T.p][0]+x, 0, T.chunk-1)
        self.players[player][T.p][1] = clamp(self.players[player][T.p][1]+y, 0, T.chunk-1)



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
        for cell in self.matrix[T.mm]:
            data.append(T.tile[cell])

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
                data.append(T.tile[self.matrix[coords(X, Y)][coords(x, y)]])
        return data

    def overlay_chunk(self, X, Y):
        data = self.get_chunk(X, Y)
        for player in self.players:
            for vessel in range(len(self.players[player][T.v])):
                if (self.players[player][T.v][vessel][T.P][0] == X and
                    self.players[player][T.v][vessel][T.P][1] == Y):
                    for y in range(T.img):
                        for x in range(T.img):
                            if (self.players[player][T.v][vessel][T.i][get_index(x, y, T.img)] != 0 and
                                get_index(x, y, T.chunk) >= 0 and get_index(x, y, T.chunk) <= len(self.matrix[coords(X, Y)])-1):
                                vx, vy = self.players[player][T.v][vessel][T.p][0], self.players[player][T.v][vessel][T.p][1]
                                i = get_index(x+vx, y+vy, T.chunk)
                                try:
                                    data[i] = T.part[self.players[player][T.v][vessel][T.i][get_index(x, y, T.img)]].format(
                                            T.dirs[self.players[player][T.v][vessel][T.r]][0])
                                except:
                                    pass
            if (self.players[player][T.P][0] == X and
                self.players[player][T.P][1] == Y):
                i = get_index(self.players[player][T.p][0], self.players[player][T.p][1], T.chunk)
                data[i] = '[]'
        return data



