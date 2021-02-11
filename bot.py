#!/usr/bin/python3

from os import system, chdir, path

from discord.ext import commands
from discord import Color, Embed

from battlehost import *

TOKEN, OWNER, PREFIX, SEED = get_bot_data()

bot = commands.Bot(command_prefix=PREFIX)

B = BattleHost()

def joined(ID):
    j = False
    if ID in B.players:
        j = True
    return j

def show_players():
    PLAYERS = ''
    for player in B.players:
        money, pstn, slct, ammos, ships = '', '', '', '', ''
        money += '\n  Currency:{}'.format(B.players[player][T.c])
        pstn += "\n  Position: World: {} Chunk: {}".format(B.players[player][T.P], B.players[player][T.p])
        slct += "\n  Selected: {}".format(B.players[player][T.s])
        for a in B.players[player][T.a]:
            ammos += "\n  {}: {}".format(a, B.players[player][T.a][a])
        for i, s in enumerate(B.players[player][T.v]):
            ships += "\n  {}: World: {} Chunk: {}".format(B.players[player][T.v][i][T.n], B.players[player][T.v][i][T.P], B.players[player][T.v][i][T.p])
        plyr = '{}:{}{}{}{}{}\n'.format(player, money, pstn, slct, ammos, ships)
        PLAYERS += plyr
    print(PLAYERS)

def view(ID, msg=''):
    response = "```"
    response += B.show_chunk(B.players[ID][T.P][0], B.players[ID][T.P][1])
    response += B.get_minimap()
    response += "```"
    if msg != '':
        response += "\n{}".format(msg)
    return response



### Connect ###
@bot.event
async def on_ready():
    print("BattleHost Online")
    B.start(SEED)
    print("BattleHost Ready")

bot.remove_command('help')
@bot.command(name='help')
async def help(ctx, *a):
    ID = str(ctx.author.id)
    response = "```\n{}\n\n\n".format(T.cmnds[T.c_help][T.c_d])
    response += "Arguments:\n\n{}```".format(T.cmnds[T.c_help][T.c_a])
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
        show_players()
        await ctx.send(response)

@bot.command(name=T.c_quit)
async def quit(ctx):
    ID = str(ctx.author.id)
    if joined(ID):
        response = B.player_quit(ID).format(ctx.author.name)
        show_players()
        await ctx.send(response)

@bot.command(name=T.c_stat)
async def stat(ctx):
    ID = str(ctx.author.id)
    if joined(ID):
        response = '```\n'
        response += "Currency:\n\n{}".format(B.players[ID][T.c])
        if B.players[ID][T.a]:
            response += "\n\n\nAmmunition:"
            for a in B.players[ID][T.a]:
                amnt = B.players[ID][T.a][a]
                response += "\n  {}:\n  {}".format(a, amnt)
        if B.players[ID][T.v]:
            response += '\n\n\nVessels:'
            for i, v in enumerate(B.players[ID][T.v]):
                img = ''
                for i, cell in enumerate(B.players[ID][T.v][i][T.i]):
                    end = ''
                    if i % 5 == 0:
                        end = '\n'
                    img.append(T.part[cell].format(end))
                X, Y = B.players[ID][T.v][i][T.P], B.players[ID][T.v][i][T.P]
                x, y = B.players[ID][T.v][i][T.p], B.players[ID][T.v][i][T.p]
                r = B.players[ID][T.v][i][T.r]
                response += "{}\n    Position: ({}, {}) ({}, {})\n    Rotation: {}\n\n".format(img, X,Y, x,y, r)
        response += '```'
        await ctx.send(response)

@bot.command(name=T.c_sel)
async def select(ctx, i):
    ID = str(ctx.author.id)
    if joined(ID):
        try:
            B.players[ID][T.s] = clamp(int(i), 0, len(B.players[ID][T.v])-1)
            show_players()
        except:
            response = 'Invalid Command'
            await ctx.send(response)

@bot.command(name=T.c_buy_ammo)
async def buy_ammo(ctx, A, *a):
    ID = str(ctx.author.id)
    if joined(ID):
        try:
            response = view(ID, msg=B.buy_ammo(ID, A, *a))
        except:
            response = 'Invalid Command'
        show_players()
        await ctx.send(response)

@bot.command(name=T.c_buy_ship)
async def buy_ship(ctx, S, *a):
    ID = str(ctx.author.id)
    if joined(ID):
        try:
            response = view(ID, msg=B.buy_ship(ID, S, *a))
        except:
            response = 'Invalid Command'
        show_players()
        await ctx.send(response)

@bot.command(name=T.c_attack)
async def attack(ctx, *a):
    ID = str(ctx.author.id)
    if joined(ID) and a:
        #try:
        response = view(ID)
        B.attack_ship(ID, a[0])
        #except:
        #    response = 'Invalid Command'
        show_players()
        await ctx.send(response)

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
            response = 'Invalid Command'
        show_players()
        await ctx.send(response)

@bot.command(name=T.c_move)
async def move(ctx, d, *a):
    ID = str(ctx.author.id)
    if joined(ID):
        try:
            amnt = 1
            if a:
                amnt += int(a[0])-1
            for i in range(amnt):
                x = T.dirs[d][1][0]
                y = T.dirs[d][1][1]
                B.step_cursor(ID, x, y)
            response = view(ID)
        except:
            response = 'Invalid Command'    
        show_players()
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
            response = 'Invalid Command'
        show_players()
        await ctx.send(response)

### Shutdown ###
@bot.command(name='shutdown')
async def shutdown(ctx, *a):
    can_do = False
    response = 'Permission Needed'
    if str(ctx.author.id) == OWNER:
        response = "Session Ended"
        can_do = True
    await ctx.send(response)
    if can_do:
        if a:
            if a[0] == 'save':
                B.save_data()
        print("Shutting down...")
        await bot.close()


bot.run(TOKEN)
