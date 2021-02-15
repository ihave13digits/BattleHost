class Term:

    def __init__(self):
        self.a = 'ammunition'
        self.c = 'currency'
        self.i = 'image'
        self.I = 'inventory'
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
        self.a_4 = 'drone'
        self.a_5 = 'nuke'

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
        self.c_refine = 'refine'
        self.c_mine = 'mine'
        self.c_pile = 'pile'
        self.c_sel = 'sel'
        self.c_buy = 'buy'
        self.c_sell = 'sell'
        self.c_symbol = 'symbol'
        self.c_attack = 'attack'
        self.c_buy_ammo = 'ammo'
        self.c_buy_ship = 'ship'
        self.c_buy_zone = 'zone'
        self.c_minimap = 'map'

        self.c_amnt = 'amount'
        self.c_drct = 'direction'

        self.R_invalid = 'Invalid Command'
        self.R_permission = 'Permission Denied'

        self.s_move = 'state_moving'

        self.b_token = 'TOKEN'
        self.b_owner = 'OWNER'
        self.b_prefix = 'PREFIX'
        self.b_seed = 'SEED'

        self.m_sediment = 'sediment'
        self.m_boulder = 'boulder'
        self.m_gravel = 'gravel'
        self.m_stone = 'stone'
        self.m_rock = 'rock'
        self.m_dirt = 'dirt'
        self.m_sand = 'sand'
        self.m_silt = 'silt'
        self.m_soil = 'soil'

        self.m_coal = 'coal'
        self.m_clay = 'clay'
        self.m_lime = 'lime'

        self.m_iron = 'iron'
        self.m_gold = 'gold'
        self.m_silver = 'silver'
        self.m_copper = 'copper'

        self.item = {
                self.m_sediment : 1,
                self.m_boulder : 10,
                self.m_gravel : 1,
                self.m_stone : 5,
                self.m_rock : 5,
                self.m_dirt : 1,
                self.m_sand : 1,
                self.m_silt : 1,
                self.m_soil : 1,
                self.m_coal : 10,
                self.m_clay : 5,
                self.m_lime : 10,
                self.m_iron : 25,
                self.m_gold : 25000,
                self.m_silver : 150,
                self.m_copper : 75,
                }

        self.drops = {
            self.m_sediment : {
                self.m_clay : 5,
                self.m_silt : 5,
                },
            self.m_boulder : {
                self.m_rock : 6,
                self.m_stone : 4,
                },
            self.m_stone : {
                self.m_gold : 1,
                self.m_silver : 2,
                self.m_copper : 3,
                self.m_gravel : 4,
                },
            self.m_rock : {
                self.m_iron : 4,
                self.m_gravel : 6,
                },
            self.m_dirt : {
                self.m_sand : 1,
                self.m_clay : 1,
                self.m_silt : 2,
                self.m_soil : 3,
                self.m_gravel : 3,
                },
            self.m_silt : {
                self.m_clay : 2,
                self.m_sand : 4,
                self.m_gravel : 4,
                },
            self.m_sand : {
                self.m_clay : 8,
                self.m_gravel : 2
                },
            }

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
        self.collect, self.tile = self.generate_tiles([30, 20, 12, 15, 8, 5, 3, 3, 2, 2],
                [self.m_sediment,self.m_silt,self.m_sand,self.m_sand,self.m_soil,
                self.m_dirt,self.m_gravel,self.m_stone,self.m_rock,self.m_boulder])
        self.part = [' {}','░{}','▒{}','▓{}','█{}']
        self.dirs = {
            'n' : ['▲', [0,-1]],
            's' : ['▼', [0,1]],
            'e' : ['▶', [1,0]],
            'w' : ['◀', [-1,0]],
            }

        self.ammo = {# Dimension, Worth, Damage
            self.a_0 : [1,100,1],
            self.a_1 : [1,100,1],
            self.a_2 : [3,250,2],
            self.a_3 : [5,5000,2],
            self.a_4 : [7,7500,2],
            self.a_5 : [9,50000,4],
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
                self.c_buy : {
                    self.c_d : 'Buys a chosen material',
                    self.c_a : '',
                    self.c_o : ''
                    },
                self.c_sell : {
                    self.c_d : 'Sells a chosen material',
                    self.c_a : '',
                    self.c_o : ''
                    },
                self.c_refine : {
                    self.c_d : 'Refines a chosen material',
                    self.c_a : '',
                    self.c_o : ''
                    },
                self.c_mine : {
                    self.c_d : 'Sets chunk depth at cursor position',
                    self.c_a : 'integer',
                    self.c_o : ''
                    },
                self.c_pile : {
                    self.c_d : 'Sets chunk depth at cursor position',
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
        for i, d in enumerate(self.drops):
            end = ', '
            if i == len(self.drops)-1:
                end = ''
            data[self.c_refine][self.c_a] += "{}{}".format(d, end)
        for i, d in enumerate(self.item):
            end = ', '
            if i == len(self.item)-1:
                end = ''
            data[self.c_buy][self.c_a] += "{}{}".format(d, end)
            data[self.c_sell][self.c_a] += "{}{}".format(d, end)

        return data

    def generate_tiles(self, I, C):
        clct = []
        data = []
        for i, t in enumerate(self.tileset):
            for itr in range(I[i]):
                clct.append(C[i])
                data.append(t)
        return clct, data
