#!/usr/bin/python3

from os import system, chdir, path

from discord.ext import commands
from discord import Color, Embed

from battlehost import *

TOKEN, OWNER, PREFIX, SEED, B = None, None, None, None, None

def debug():
    ID = str(OWNER)
    B.add_player(ID)
    B.players[ID][T.c] = 10000000000000000
    B.buy_ammo(ID, 'missile', 10000)
    B.buy_ammo(ID, 'torpedo', 5000)
    B.buy_ammo(ID, 'mortar', 1000)
    B.buy_ammo(ID, 'strike', 500)
    B.buy_ammo(ID, 'nuke', 100)
    B.step_cursor(ID, 10, 0)
    B.step_cursor(ID, 0, 10)
    #B.save_data()
    #B.attack_ship(ID, 10, 18, 'missile')

def start():
    from sys import argv
    global TOKEN, OWNER, PREFIX, SEED, B
    TOKEN, OWNER, PREFIX, SEED = get_bot_data()
    
    if len(argv) > 1:
        SEED = argv[1]
        print("New seed is {}".format(SEED))
    B = BattleHost(SEED)
    B.load_data(SEED)
    debug()

start()
bot = commands.Bot(command_prefix=PREFIX)

def joined(ID):
    j = False
    if ID in B.players:
        j = True
    return j

def show_player(ID):
    response = '```\n'
    response += "Currency: {}\n".format(B.players[ID][T.c])
    response += "Selected: {}\n".format(B.players[ID][T.s])
    response += "Position: ({}, {}) ({}, {})\n\n".format(B.players[ID][T.P][0], B.players[ID][T.P][1], B.players[ID][T.p][0], B.players[ID][T.p][1])
    if B.players[ID][T.a]:
        response += "\nAmmunition:"
        for a in B.players[ID][T.a]:
            amnt = B.players[ID][T.a][a]
            response += "\n  {}:\n  {}".format(a, amnt)
    if sum(B.players[ID][T.I].values()) > 0:
        response += "\nInventory:"
        for itm in B.players[ID][T.I]:
            if B.players[ID][T.I][itm] > 0:
                response += "\n  {}: {}".format(itm, B.players[ID][T.I][itm])
    if B.players[ID][T.v]:
        response += '\n\nVessels:\n'
        for i, v in enumerate(B.players[ID][T.v]):
            img = '  {}: {}\n'.format(i, B.players[ID][T.v][i][T.n])
            hp = 0
            for c, cell in enumerate(B.players[ID][T.v][i][T.i]):
                end = ''
                if c % T.img == 0:
                    end = '\n'
                img += T.part[cell].format(end)
                hp += cell
            X, Y = B.players[ID][T.v][i][T.P][0], B.players[ID][T.v][i][T.P][1]
            x, y = B.players[ID][T.v][i][T.p][0], B.players[ID][T.v][i][T.p][1]
            r = B.players[ID][T.v][i][T.r]
            response += "{}\n    Health : {}\n    Position: ({}, {}) ({}, {})\n    Rotation: {}\n".format(img, hp, X,Y, x,y, r)
    response += '```'
    return response

def view(ID, vw='chunk', msg=''):
    response = "```"
    if vw == 'chunk':
        response += B.show_chunk(B.players[ID][T.P][0], B.players[ID][T.P][1])
    if vw == 'world':
        B.generate_minimap()
        response += B.get_minimap()
    response += "```"
    if msg != '':
        response += "\n{}".format(msg)
    return response



### Connect ###
@bot.event
async def on_ready():
    print("BattleHost Online")

bot.remove_command(T.c_help)
@bot.command(name=T.c_help)
async def help(ctx, *a):
    ID = str(ctx.author.id)
    response = "```\n{}\n\n\n".format(T.cmnds[T.c_help][T.c_d])
    response += "Arguments:\n\n{}```".format(T.cmnds[T.c_help][T.c_o])
    try:
        if a:
            response = "```\n{}".format(T.cmnds[a[0]][T.c_d])
            if T.cmnds[a[0]][T.c_a]:
                response += "\n\n\nArguments:\n\n{}".format(T.cmnds[a[0]][T.c_a])
            if T.cmnds[a[0]][T.c_o]:
                response += "\n\n\nOptional Arguments:\n\n{}".format(T.cmnds[a[0]][T.c_o])
            response += "```"
        else:
            pass
    except:
        pass
    await ctx.send(response)

@bot.command(name=T.c_join)
async def join(ctx):
    ID = str(ctx.author.id)
    if not joined(ID):
        response = view(ID, msg=B.add_player(ID).format(ctx.author.name))
        await ctx.send(response)

@bot.command(name=T.c_quit)
async def quit(ctx):
    ID = str(ctx.author.id)
    if joined(ID):
        response = B.player_quit(ID).format(ctx.author.name)
        await ctx.send(response)

@bot.command(name=T.c_minimap)
async def minimap(ctx):
    ID = str(ctx.author.id)
    if joined(ID):
        response = view(ID, vw='world')
        await ctx.send(response)

@bot.command(name=T.c_stat)
async def stat(ctx):
    ID = str(ctx.author.id)
    if joined(ID):
        response = show_player(ID)
        await ctx.send(response)

@bot.command(name=T.c_sel)
async def select(ctx, i):
    ID = str(ctx.author.id)
    if joined(ID):
        try:
            B.players[ID][T.s] = clamp(int(i), 0, len(B.players[ID][T.v])-1)
        except:
            response = T.R_invalid
            await ctx.send(response)

@bot.command(name=T.c_mine)
async def mine(ctx, i):
    ID = str(ctx.author.id)
    if joined(ID):
        try:
            X, Y = B.players[ID][T.P][0], B.players[ID][T.P][1]
            x, y = B.players[ID][T.p][0], B.players[ID][T.p][1]
            response = B.modify_chunk(ID, int(i), T.c_mine)
        except:
            response = T.R_invalid
        await ctx.send(response)

@bot.command(name=T.c_pile)
async def pile(ctx, i):
    ID = str(ctx.author.id)
    if joined(ID):
        try:
            X, Y = B.players[ID][T.P][0], B.players[ID][T.P][1]
            x, y = B.players[ID][T.p][0], B.players[ID][T.p][1]
            response = B.modify_chunk(ID, int(i), T.c_pile)
        except:
            response = T.R_invalid
        await ctx.send(response)

@bot.command(name=T.c_refine)
async def refine(ctx, m, *a):
    ID = str(ctx.author.id)
    if joined(ID):
        try:
            response = B.refine_material(ID, m, *a)
        except:
            response = T.R_invalid
        await ctx.send(response)

@bot.command(name=T.c_buy_ammo)
async def buy_ammo(ctx, A, *a):
    ID = str(ctx.author.id)
    if joined(ID):
        try:
            response = view(ID, msg=B.buy_ammo(ID, A, *a))
        except:
            response = T.R_invalid
        await ctx.send(response)

@bot.command(name=T.c_buy_ship)
async def buy_ship(ctx, S, *a):
    ID = str(ctx.author.id)
    if joined(ID):
        #try:
        response = view(ID, msg=B.buy_ship(ID, S, *a))
        #except:
        #    response = 'Invalid Command'
        await ctx.send(response)

@bot.command(name=T.c_buy_zone)
async def buy_zone(ctx, d):
    ID = str(ctx.author.id)
    if joined(ID):
        try:
            x = B.players[ID][T.P][0]+T.dirs[d][1][0]
            y = B.players[ID][T.P][1]+T.dirs[d][1][1]
            response = B.buy_zone(ID, x, y)
        except:
            response = T.R_invalid
        await ctx.send(response)

@bot.command(name=T.c_attack)
async def attack(ctx, x, y, a):
    ID = str(ctx.author.id)
    if joined(ID) and a:
        response = view(ID)
        #try:
        B.attack_ship(ID, int(x), int(y), a)
        #except:
        #    pass
        await ctx.send(response)

@bot.command(name=T.c_symbol)
async def symbol(ctx, s):
    ID = str(ctx.author.id)
    if joined(ID):
        try:
            if s:
                if len(s) > 1:
                    s = s[0]
            else:
                s = ' '
            B.player_symbol(ID, s)
        except:
            response = T.R_invalid

@bot.command(name=T.c_jump)
async def jump(ctx, d, *a):
    ID = str(ctx.author.id)
    if joined(ID):
        try:
            amnt = 1
            if a:
                amnt += int(a[0])-1
            for i in range(amnt):
                x = T.dirs[d][1][0]
                y = T.dirs[d][1][1]
                B.step_player(ID, x, y)
            response = view(ID)
        except:
            response = T.R_invalid
        await ctx.send(response)

@bot.command(name=T.c_move)
async def move(ctx, d, *a):
    ID = str(ctx.author.id)
    if joined(ID):
        #try:
        amnt = 1
        if a:
            amnt += int(a[0])-1
        for i in range(amnt):
            x = T.dirs[d][1][0]
            y = T.dirs[d][1][1]
            B.step_cursor(ID, x, y)
        response = view(ID)
        #except:
        #    response = 'Invalid Command'    
        await ctx.send(response)

@bot.command(name=T.c_turn)
async def turn(ctx, d):
    ID = str(ctx.author.id)
    if joined(ID):
        response = view(ID)
        try:
            if d in T.dirs:
                B.players[ID][T.v][B.players[ID][T.s]][T.r] = d
        except:
            response = T.R_invalid
        await ctx.send(response)

### Owner Commands ###

@bot.command(name='load')
async def load(ctx, sd):
    ID = str(ctx.author.id)
    if ID == OWNER:
        B.load_data(sd)

@bot.command(name='restart')
async def restart(ctx, *a):
    can_do = False
    response = T.R_permission
    ID = str(ctx.author.id)
    if ID == OWNER:
        from os import system
        can_do = True
        await bot.close()
    else:
        await ctx.send(response)

    if can_do:
        from os import system
        print("Restarting...")
        if a:
            cmd = './restart.py ./bot.py {}'.format(a[0])
            if len(a) > 1:
                if a[1] == 'save':
                    B.save_data(SEED)
            system(cmd)
        else:
            system('./restart.py ./bot.py')

@bot.command(name='shutdown')
async def shutdown(ctx, *a):
    ID = str(ctx.author.id)
    can_do = False
    response = T.R_permission
    if ID == OWNER:
        response = "Session Ended"
        can_do = True
    await ctx.send(response)
    if can_do:
        if a:
            if a[0] == 'save':
                B.save_data(SEED)
        print("Shutting down...")
        await bot.close()


bot.run(TOKEN)
