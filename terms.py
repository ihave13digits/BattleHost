class Term:

    def __init__(self):
        self.a = 'ammunition'
        self.c = 'currency'
        self.i = 'image'
        self.m = 'matrix'
        self.mm = 'minimap'
        self.n = 'name'
        self.o = 'owner'
        self.p = 'chunk_position'
        self.P = 'world_position'
        self.r = 'rotation'
        self.s = 'selected'
        self.S = 'state'
        self.v = 'vessel'
        self.w = 'worth'

        self.a_0 = 'missile'
        self.a_1 = 'torpedo'
        self.a_2 = 'mortar'
        self.a_3 = 'strike'
        self.a_4 = 'nuke'

        self.c_d = 'description'
        self.c_a = 'arguments'
        self.c_o = 'optional'

        self.c_help = 'help'
        self.c_join = 'join'
        self.c_quit = 'quit'
        self.c_stat = 'stat'
        self.c_jump = 'jump'
        self.c_move = 'move'
        self.c_turn = 'turn'
        self.c_mod = 'mod'
        self.c_sel = 'sel'
        self.c_symbol = 'symbol'
        self.c_attack = 'attack'
        self.c_buy_ammo = 'ammo'
        self.c_buy_ship = 'ship'
        self.c_buy_zone = 'zone'
        self.c_minimap = 'map'

        self.c_amnt = 'amount'
        self.c_drct = 'direction'

        self.i_earth = 'earth' 

        self.s_move = 'state_moving'

        self.b_token = 'TOKEN'
        self.b_owner = 'OWNER'
        self.b_prefix = 'PREFIX'
        self.b_seed = 'SEED'

        self.r_low = .98
        self.r_high = .98

        self.img = 5
        self.octs = 1
        self.OCTS = 1
        self.chunk_x = 1
        self.chunk_y = 1
        self.world_x = 1
        self.world_y = 1
        self.chunk = 20
        self.world = 20
        self.output = 48
        self.loaded = 0
        self.complete = int((self.world*self.world)+self.OCTS)
        self.chunk_value = 10000

        self.data_dir = 'data'
        self.world_data = 'world_data'
        self.player_data = 'player_data'

        self.tileset = ['██','▓▓','▒▒','░░','##','::',':.','.:','..','. ']
        self.tile = self.generate_tiles([30, 20, 12, 15, 8, 5, 3, 3, 2, 2])
        self.part = [' {}','░{}','▒{}','▓{}','█{}']

        self.dirs = {
            'n' : ['▲', [0,-1]],
            's' : ['▼', [0,1]],
            'e' : ['▶', [1,0]],
            'w' : ['◀', [-1,0]],
            }

        self.ammo = {# Dimension, Worth, Damage
            self.a_0 : [1,0,1],
            self.a_1 : [1,0,1],
            self.a_2 : [3,10,2],
            self.a_3 : [6,50,2],
            self.a_4 : [7,50000,4],
            }

        self.ship = {# Worth, Image
            'carrier' : [40000, [
                    0,0,4,0,0,
                    0,0,4,0,0,
                    0,0,4,0,0,
                    0,0,4,0,0,
                    0,0,4,0,0,
                ]],
            'battleship' : [55000, [
                    0,0,4,0,0,
                    0,0,4,0,0,
                    0,0,4,0,0,
                    0,0,4,0,0,
                    0,0,0,0,0,
                ]],
            'cruiser' : [30000, [
                    0,0,0,0,0,
                    0,0,4,0,0,
                    0,0,4,0,0,
                    0,0,4,0,0,
                    0,0,0,0,0,
                ]],
            'submarine' : [40000, [
                    0,0,0,0,0,
                    0,0,4,0,0,
                    0,0,4,0,0,
                    0,0,4,0,0,
                    0,0,0,0,0,
                ]],
            'destroyer' : [15000, [
                    0,0,0,0,0,
                    0,0,4,0,0,
                    0,0,4,0,0,
                    0,0,0,0,0,
                    0,0,0,0,0,
                ]],
            }
        self.cmnds = self.generate_commands()

    def generate_commands(self):
        data = {
                self.c_help : {
                    self.c_d : 'Command reference',
                    self.c_a : '',
                    self.c_o : ''
                    },
                self.c_join : {
                    self.c_d : 'Joins game and grants access to commands',
                    self.c_a : '',
                    self.c_o : ''
                    },
                self.c_quit : {
                    self.c_d : 'Quits game and deletes player data',
                    self.c_a : '',
                    self.c_o : ''
                    },
                self.c_stat: {
                    self.c_d : 'Shows player stats',
                    self.c_a : '',
                    self.c_o : ''
                    },
                self.c_jump : {
                    self.c_d : 'Changes world position',
                    self.c_a : '',
                    self.c_o : self.c_amnt
                    },
                self.c_move : {
                    self.c_d : 'Changes chunk position',
                    self.c_a : '',
                    self.c_o : self.c_amnt
                    },
                self.c_turn : {
                    self.c_d : 'Changes ship rotation',
                    self.c_a : '',
                    self.c_o : ''
                    },
                self.c_sel : {
                    self.c_d : 'Changes selected ship',
                    self.c_a : 'index',
                    self.c_o : ''
                    },
                self.c_mod : {
                    self.c_d : 'Changes chunk depth at cursor position',
                    self.c_a : 'integer',
                    self.c_o : ''
                    },
                self.c_symbol : {
                    self.c_d : 'Updates your map symbol',
                    self.c_a : '',
                    self.c_o : ''
                    },
                self.c_attack : {
                    self.c_d : 'Attacks at cursor position',
                    self.c_a : '',
                    self.c_o : ''
                    },
                self.c_buy_ammo : {
                    self.c_d : 'Buys ammunition',
                    self.c_a : '',
                    self.c_o : self.c_amnt
                    },
                self.c_buy_ship : {
                    self.c_d : 'Buys ship',
                    self.c_a : '',
                    self.c_o : self.c_amnt
                    },
                self.c_buy_zone : {
                    self.c_d : 'Buys zone adjacent to you',
                    self.c_a : '',
                    self.c_o : ''
                    },
                self.c_minimap : {
                    self.c_d : 'Shows world map',
                    self.c_a : '',
                    self.c_o : ''
                    },
                }
        for i, c in enumerate(data):
            end = ', '
            if i == len(data)-1:
                end = ''
            data[self.c_help][self.c_o] += c+end
        for i, d in enumerate(self.dirs):
            end = ', '
            if i == len(self.dirs)-1:
                end = ''
            data[self.c_jump][self.c_a] += d+end
            data[self.c_move][self.c_a] += d+end
            data[self.c_turn][self.c_a] += d+end
            data[self.c_buy_zone][self.c_a] += d+end
        for i, a in enumerate(self.ammo):
            end = '\n'
            if i == len(self.ammo)-1:
                end = ''
            data[self.c_buy_ammo][self.c_a] += "{}{}{}".format(a, '.'*int(self.output-len(str("{}{}".format(a, self.ammo[a][1])))), self.ammo[a][1])+end
            data[self.c_attack][self.c_a] += "{}{}{}".format(a, '.'*int(self.output-len(str("{}{}".format(a, self.ammo[a][1])))), self.ammo[a][1])+end
        for i, s in enumerate(self.ship):
            end = '\n'
            if i == len(self.ship)-1:
                end = ''
            data[self.c_buy_ship][self.c_a] += "{}{}{}".format(s, '.'*int(self.output-len(str("{}{}".format(s, self.ship[s][0])))), self.ship[s][0])+end
        return data

    def generate_tiles(self, I):
        data = []
        for i, t in enumerate(self.tileset):
            for itr in range(I[i]):
                data.append(t)
        return data
