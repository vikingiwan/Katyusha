 #####KatyushaV2#####
import discord
from discord.ext import commands
import asyncio
import sys
import random
import time
import configparser
import os
import sqlite3
import pyjokes
from cleverwrap import CleverWrap

##Variables & objects##
#Bot stuff
global VERSION
VERSION = '0.6'
global DEBUG
DEBUG = True
global iwanID
iwanID = 142076624072867840
global botID
botID = 217108205627637761
global vtacGuild
vtacGuild = 183107747217145856
global mainChannel
mainChannel= 622144477233938482
global activeGiveaway
activeGiveaway = False
bot = commands.Bot(command_prefix="!")
connection = sqlite3.connect('KatyushaData.db')
cur = connection.cursor()
#Lists
killResponses = ["%s 'accidentally' fell in a ditch... RIP >:)", "Oh, %s did that food taste strange? Maybe it was.....*poisoned* :wink:", "I didn't mean to shoot %s, I swear the gun was unloaded!", "Hey %s, do me a favor? Put this rope around your neck and tell me if it feels uncomfortable.", "*stabs %s* heh.... *stabs again*....hehe, stabby stabby >:D", "%s fell into the ocean whilst holding an anvil...well that was stupid."]
userCommands = ["test", "hug", "pat", "roll", "flip", "remind", "kill", "calc", "addquote", "quote", "joke", "dirtyjoke", "pfp", "info", "version", "changelog", "links", "link", "giveaway"]
operatorCommands = ["say", "purge", "getBot", "!update", "addLink", "terminate", "startGiveaway", "endGiveaway"]
op_roles = [183109993686499328, 183109339991506945]
officer_roles = [183110198188179456, 183109339991506945, 183109993686499328]

welcome_message='''
Welcome to Viking Tactical!

If you'd like to apply for full-membership, you can submit an application at <http://vikingtactical.ml/index.php?link-forums/apply-here.3/> (It usually takes 3-5 mins to complete) and then someone would read your application and either accept or decline it. Either way, you'd receive an e-mail with the decision (might need to check your spam folder, sometimes our emails end up in there, i'm working on fixing that lol)

Some of the benefits of becoming a full member are access to more channels on discord and categories on our forums, assignment to a division which has its own private chat channels, access to giveaways, and the ability to climb the ranks and gain promotions within the clan.
There's no rush, obligation or pressure to make an app though!
'''

##########
###RANKS###

#Recruit Rank
rank_rec = 469376345672253451

#Enlisted Ranks
rank_msg = 492802360616419338
rank_sfc = 492802199668129826
rank_sgt= 492802074140999691
rank_cpl = 492801929794158612
rank_pfc = 492801780002979850
rank_pvt = 281727465968369665

#Officer Ranks
rank_lt = 183110198188179456
rank_cap = 183109339991506945
rank_com = 183109993686499328

enlisted_ranks = [rank_pvt, rank_pfc, rank_cpl, rank_sgt, rank_sfc, rank_msg, rank_lt, rank_cap, rank_com]
##########



#Remove default help command
bot.remove_command('help')

#Util funcs
def getTokens():
    config = configparser.ConfigParser()
    if not os.path.isfile("tokens.cfg"):
        print("tokens file missing. ")
        print("Creating one now.")
        config.add_section("Tokens")
        config.set("Tokens", "Bot", "null")
        config.set("Tokens", "Cleverbot", "null")
        with open ('tokens.cfg', 'w') as configfile:
            config.write(configfile)
        print("File created.")
        print("Please edit tokens.cfg and then restart.")
        _ = input()
    else:
        config.read('tokens.cfg')
        global botToken
        botToken = config.get('Tokens', 'Bot')
        global cb
        cb = CleverWrap(config.get('Tokens', 'Cleverbot'))
        
def isOp(member):
    for r in member.roles:
        if r.id in op_roles:
            return True
            return
    return False
    
def isOfficer(member):
    for r in member.roles:
        if r.id in officer_roles:
            return True
            return
    return False
    
def isEnlisted(member):
    for r in member.roles:
        if  r.id in enlisted_ranks:
            return True
            return
    return False
    
def getPromoRank(member):
    for r in member.roles:
        #_promoRank = None
        if r.id == rank_cap:
            _promoRank == None
        elif r.id == rank_lt:
            _promoRank = rank_cap
        elif r.id == rank_msg:
            _promoRank = rank_lt
        elif r.id == rank_sfc:
            _promoRank = rank_msg
        elif r.id == rank_sgt:
            _promoRank = rank_sfc
        elif r.id == rank_cpl:
            _promoRank = rank_sgt
        elif r.id == rank_pfc:
            _promoRank = rank_cpl
        elif r.id == rank_pvt:
            _promoRank = rank_pfc
    return _promoRank
    
def debug(msg):
    if DEBUG == True:
        print(msg)
    
def create_tables():
    cur.execute('''CREATE TABLE IF NOT EXISTS quoteList
                     (QUOTES TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Links
                     (name TEXT, link TEXT)''')
                     
def register_quote(usr, quote):
    quote = usr.name + ': "' + quote + '"'
    cur.execute("INSERT INTO quoteList (quotes) VALUES (?)", (quote,))
    connection.commit()
    
def load_quotes():
    print("Loading Quotes...")
    cur.execute('''SELECT * FROM quoteList''')
    global quotes
    quotes = cur.fetchall()
def get_quote():
    quote = random.choice(quotes)
    quote = str(quote)
    quote = quote.strip("('',)")
    return quote
    
def get_changelog(ver):
    with open ('changelogs/' + ver + '.txt', 'r') as changelog:
        changelog = changelog.read()
        changelog = changelog.splitlines()
    changelog = str(changelog)
    changelog = changelog.replace("',", "\n")
    changelog = changelog.split("['],")
    return changelog
    
    
    
def get_link(name):
    cur.execute("SELECT link FROM Links WHERE name = (?)", (name,))
    link = str(cur.fetchall())
    link = link.strip("[(',)]")
    return link
    
def add_link(name, link):
    cur.execute("INSERT INTO Links (name, link) VALUES (?, ?)", (name, link))
    connection.commit()
    print("Link Added")
    
def list_links():
    list = []
    cur.execute('''SELECT name FROM Links''')
    rows = cur.fetchall()
    for row in rows:
        _row = str(row)
        _row = _row.strip("[(',)]")
        list.append(_row)
    print(list)
    return list
    

    
    

#Bot Events
@bot.event
async def on_ready():
    print("Discord version: " + discord.__version__)
    print("Logged in as: " + bot.user.name)
    print("ID: " + str(bot.user.id))
    print("------------------")
    _activity = discord.Game("Victory Through Comradery!")
    await bot.change_presence(activity=_activity)
    #_debugRoles = bot.get_guild(vtacGuild).get_role(rank_rec).name
    #print("Roles: " + _debugRoles)
    
@bot.event
async def on_member_join(member):
    print(member.name + " has joined the guild...assigning rank...")
    _role = bot.get_guild(vtacGuild).get_role(rank_rec)
    await member.add_roles(_role, reason="New member", atomic=True)
    print("Recruit rank added to " + member.display_name)
    print("Adding rank prefix...")
    _nick = "Rec. " + member.display_name
    await member.edit(nick=_nick, reason="New User")
    print("Added prefix to " + member.display_name)
    _chan = bot.get_guild(vtacGuild).get_channel(mainChannel)
    await _chan.send(":thumbsup: " + member.mention + " has joined Viking Tactical.")
    #await bot.send_message(member, welcome_message)
    
@bot.event
async def on_member_remove(member):
    _chan = bot.get_guild(vtacGuild).get_channel(mainChannel)
    await _chan.send(":thumbsdown: " + member.display_name + " has left Viking Tactical.")

#OPERATOR ONLY COMMANDS:
@bot.command(pass_context = True)
async def say(ctx, *, msg: str):
    if isOp(ctx.message.author) == True:
        await bot.delete_message(ctx.message)
        await bot.say(msg)
    else:
        await bot.say("ERROR: UNAUTHORIZED!")

@bot.command(pass_context = True)
async def purge(ctx):
    if isOp(ctx.author) == True:
        await ctx.send("UNDERSTOOD, COMMANDER. I WILL DESTROY THE EVIDENCE!")
        await asyncio.sleep(4)
        await ctx.channel.purge(limit=100, bulk=True)
        await ctx.send("CHANNEL HAS BEEN PURGED, SIR!")
    else:
        await ctx.send("ERROR: UNAUTHORIZED")
        
@bot.command(pass_context = True)
async def getBot(ctx):
    if isOp(ctx.message.author) == True:
        await bot.delete_message(ctx.message)
        await bot.send_message(ctx.message.author, "Invite link:\nhttps://discordapp.com/api/oauth2/authorize?client_id=217108205627637761&scope=bot&permissions=1")
    else:
        await bot.say("ERROR: UNAUTHORIZED!")
        
@bot.command(pass_context = True)
async def addLink(ctx, name: str=None, *, link: str=None):
    if isOp(ctx.message.author) == True:
        print("name: " + name)
        print("link: " + link)
        add_link(name, link)
        await bot.delete_message(ctx.message)
        await bot.say("Link Saved!")
        
@bot.command(pass_context = True)
async def terminate(ctx):
    if isOp(ctx.message.author) == True:
        await bot.say("Affirmative. Terminating now...")
        await bot.change_presence(status=discord.Status.offline)
        sys.exit()
    else:
        await bot.say("ERROR: UNAUTHORIZED!")
        
        
@bot.command(pass_context = True)
async def startGiveaway(ctx, *, msg: str=None):
    if isOp(ctx.message.author) == True:
        global activeGiveaway
        if activeGiveaway == True:
            await bot.say("ERROR: There is already a giveaway in progress!")
        else:
            if msg == None:
                await bot.say("ERROR: You cannot start a giveaway with a blank message!")
            else:
                global giveawayEntries
                giveawayEntries = []
                await bot.delete_message(ctx.message)
                await bot.send_message(bot.get_guild(vtacGuild).get_channel(mainChannel), "@everyone A giveaway is  starting!\n(Remember, you must be a full member to participate in giveaways)\n")
                await asyncio.sleep(5)
                msg = "\n" + msg + "\n\nUse !giveaway to enter the giveaway!"
                em = discord.Embed(title='', description=msg, colour=0xFF0000)
                em.set_author(name='Giveaway Info:', icon_url="https://i.imgur.com/0DCg8JB.png")
                await bot.send_message(bot.get_guild(vtacGuild).get_channel(mainChannel), embed=em)
                activeGiveaway = True
    else:
        await bot.say("ERROR: UNAUTHORIZED!")
        
@bot.command(pass_context = True)
async def endGiveaway(ctx):
    if isOp(ctx.message.author) == True:
        global activeGiveaway
        activeGiveaway = False
        await bot.send_message(bot.get_guild(vtacGuild).get_channel(mainChannel), "@everyone The current giveaway is ending! I'm now deciding the winner...")
        await asyncio.sleep(5)
        await bot.send_message(bot.get_guild(vtacGuild).get_channel(mainChannel), "And the winner is...")
        winner = random.choice(giveawayEntries)
        await bot.send_typing(bot.get_guild(vtacGuild).get_channel(mainChannel))
        await asyncio.sleep(10)
        await bot.send_message(bot.get_guild(vtacGuild).get_channel(mainChannel), winner.mention + "! Congratulations! :clap:")    
    else:
        await bot.say("ERROR: UNAUTHORIZED!")
   
        
#OFFICER COMMANDS
@bot.command(pass_context = True)
async def promote(ctx, *, member: discord.Member = None):
    if isOfficer(ctx.message.author) == True:
        if member is None:
            await bot.say("Invalid target!\nCommand Usage Example: `!promote @Iwan`")
        else:
            _rank = getPromoRank(member)
            if _rank == None:
                await bot.say("ERROR: This user cannot be promoted!")
            else:
                _role = discord.utils.get(bot.get_guild(vtacGuild).roles, id=_rank)
                await bot.add_roles(member, _role)
                if _rank == rank_pfc:
                    await bot.change_nickname(member, "Pfc. " + member.name)
                elif _rank == rank_cpl:
                    await bot.change_nickname(member, "Cpl. " + member.name)
                elif _rank == rank_sgt:
                    await bot.change_nickname(member, "Sgt. " + member.name)
                elif _rank == rank_sfc:
                    await bot.change_nickname(member, "Sfc. " +  member.name)
                elif _rank == rank_msg:
                    await bot.change_nickname(member,  "Msg. " +  member.name)
                elif _rank == rank_lt:
                    await bot.change_nickname(member,  "Lt. " +  member.name)
                elif _rank == rank_cap:
                    await bot.change_nickname(member,  "Cpt. " +  member.name)
                await asyncio.sleep(5)
                await bot.send_message(bot.get_guild(vtacGuild).get_channel(mainChannel), "@everyone Congratulations to " + member.mention + " on their promotion!")
    else:
        await bot.say("ERROR: UNAUTHORIZED")
            
    
        
        
#USER COMMANDS
@bot.command(pass_context = True)
async def help(ctx):
    usrCmds = '\n'.join("!" + str(c) for c in userCommands)
    em = discord.Embed(title='', description=usrCmds, colour=0xFF0000)
    em.set_author(name='Commands:', icon_url=bot.user.avatar_url)
    await bot.send_message(ctx.message.channel, embed=em)
    #If  user is operator, send dm with op commands
    if isOp(ctx.message.author) == True:
        opCmds = '\n'.join("!" + str(c) for c in operatorCommands)
        em = discord.Embed(title='', description=opCmds, colour=0xFF0000)
        em.set_author(name='High-Command Commands:', icon_url=bot.user.avatar_url)
        await bot.send_message(ctx.message.author, embed=em)

@bot.command()
async def version():
    await bot.say("I am currently on version " + VERSION)
        
@bot.command()
async def test():
    await bot.say("Hello World!")
    
@bot.command(pass_context = True)
async def changelog(ctx, ver: str=VERSION):
    await bot.say("Changelog for version " + ver + ":")
    for x in get_changelog(ver):
        await bot.say("`" + str(x).strip("['],").replace("'", "") + "`")
    
@bot.command(pass_context = True)
async def hug(ctx):
    hug = random.choice([True, False])
    if hug == True:
        await bot.say(ctx.message.author.mention + ": :hugging:")
    else:
        await bot.say(ctx.message.author.mention + ": You don't deserve a hug, cyka.")
        
@bot.command()
async def roll(dice : str=None):
    if dice == None:
        await bot.say('Format has to be in NdN!')
        return
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)
      
@bot.command(pass_context = True)
async def flip(ctx):
    await bot.say("Okay, I'll flip it!")
    await bot.send_typing(ctx.message.channel)
    await asyncio.sleep(3)
    if random.choice([True, False]) == True:
        await bot.say(ctx.message.author.mention + ": the result is.......**HEADS**!")
    else:
        await bot.say(ctx.message.author.mention + ": the result is.......**TAILS**!")
      
@bot.group(pass_context = True)
async def remind(ctx, time: str = "0", *, reminder: str="null"):
    time = int(time)
    if time == 0 or reminder == "null":
        await bot.say("Correct Usage: !remind <time in minutes> <reminder>")
        await bot.say("Example: !remind 5 Tell me how reminders work")
        return
    else:
        await bot.delete_message(ctx.message)
        await bot.say("Okay, " + ctx.message.author.mention + "! I'll remind you :smile:")
        await asyncio.sleep(time * 60)
        await bot.send_message(ctx.message.author, "You wanted me to remind you: " + reminder)
        
@bot.command(pass_context = True)
async def kill (ctx, *, member: discord.Member = None):
    if member is None:
        await bot.say(ctx.message.author.mention + ": I need a target!")
        return

    if member.id == botID and ctx.message.author.id == iwanID:
        await bot.say(ctx.message.author.mention + ": C-Commander, p-please...I'm useful! Please don't terminate me! :cry:")
    elif member.id == ctx.message.author.id:
        await bot.say(ctx.message.author.mention + ": Why do you want me to kill you? :open_mouth:")
    elif member.id == botID:
        await bot.say(ctx.message.author.mention + ": Hah! Don't get cocky kid, I could end you in less than a minute! :dagger:")
    elif member.id == iwanID:
        await bot.say(ctx.message.author.mention + ": Kill the Commander? I could never!")
    else:
        random.seed(time.time())
        choice = killResponses[random.randrange(len(killResponses))] % member.mention
        await bot.say(ctx.message.author.mention + ": " + choice)
      
@bot.command(pass_context = True)
async def pat(ctx, *, member: discord.Member = None):
    if member is None:
        await bot.say("Aww, does somebody need a headpat? I'll pat you, " + ctx.message.author.mention)
        await bot.send_file(ctx.message.channel, "img/headpat.gif")
    else:
        await bot.say(ctx.message.author.mention + " pats " + member.mention)
        await bot.send_file(ctx.message.channel, "img/headpat.gif")
        
@bot.group(pass_context = True)
async def calc(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say("Invalid arguments! Supported operations are: `add` `subract` `multiply` `divide`")
        await bot.say("Example: `!calc add 1 1` will yield a result of 2")
@calc.command()
async def add(left: float, right: float):
    ans = left + right
    await bot.say(str(left) + " + " + str(right) + " = " + str(ans))
@calc.command()
async def subtract(left: float, right: float):
    ans = left - right
    await bot.say(str(left) + " - " + str(right) + " = " + str(ans))
@calc.command()
async def multiply(left: float, right: float):
    ans = left * right
    await bot.say(str(left) + " * " + str(right) + " = " + str(ans))
@calc.command()
async def divide(left: float, right: float):
    ans = left / right
    await bot.say(str(left) + " / " + str(right) + " = " + str(ans))
    
@bot.command(pass_context = True)
async def addquote(ctx, member: discord.Member = None, *, quote: str=None):
    if member == None or quote == None:
        await bot.say("You must mention a user and add a quote!")
        await bot.say("Example: `!addquote @Iwan I love quotes`")
    elif member.id == botID:
        await bot.say("ERROR: UNAUTHORIZED! You are not allowed to quote me. Muahahaha!")
        return
    else:
        register_quote(member, quote)
        await bot.delete_message(ctx.message)
        await bot.say("Quote added :thumbsup:")
        load_quotes()
       
@bot.command()
async def quote():
    await bot.say(get_quote())
    
@bot.command(pass_context = True)
async def poke(ctx, member: discord.Member=None):
    if member==None:
        await bot.say("I can't poke nobody! Try mentioning someone with `@`, like this\n`!poke @Iwan`")
        return
    else:
        await bot.say(ctx.message.author.mention + " just poked " + member.mention + "!")
        await bot.send_file(ctx.message.channel, "img/poke.gif")
        
@bot.command(pass_context = True)
async def joke(ctx):
    await bot.say(ctx.message.author.mention + ": " + pyjokes.get_joke())
    
@bot.command(pass_context = True)
async def dirtyjoke(ctx):
    await bot.say(ctx.message.author.mention + ": " + pyjokes.get_joke('en', 'adult'))
    
@bot.command(pass_context = True)
async def pfp(ctx, member: discord.Member=None):
    if member==None:
        member = ctx.message.author
#        await bot.say("You forgot to give me a user! try mentioning someone with @ next time!")
#        await bot.say("Example: `!pfp @Katyusha`")
#        return
    await bot.say(ctx.message.author.mention + ": Here you go!\n" + member.avatar_url)
        
@bot.command(pass_context = True)
async def info(ctx, member: discord.Member=None):
    if member == None:
        member = ctx.message.author
    info = "Joined guild on: " + member.joined_at.strftime("%A %B %d, %Y at %I:%M%p") + "\n"
    info = info + "Account created on: " + member.created_at.strftime("%A %B %d, %Y at %I:%M%p")
    em = discord.Embed(title='', description=info, colour=0xFF0000)
    em.set_author(name=member.name, icon_url=member.avatar_url)
    await bot.send_message(ctx.message.channel, embed=em)

@bot.command(pass_context = True)
async def link(ctx, name: str=None):
    if name == None:
        await bot.say("ERROR: LINK NOT FOUND!")
    else:
        await bot.say(ctx.message.author.mention + " " + get_link(name))
        
@bot.command(pass_context = True)
async def links(ctx):
    await bot.say(list_links())
    
    
@bot.command(pass_context = True)
async def giveaway(ctx):
    if isEnlisted(ctx.message.author) == True:
        global activeGiveaway
        if activeGiveaway == False:
            await bot.say(ctx.message.author.mention + " There is no active giveaway!")
        else:
            global giveawayEntries
            if ctx.message.author in giveawayEntries:
                await bot.say(ctx.message.author.mention + " You're already entered into the giveaway. No cheating!")
            else:
                _entry = [ctx.message.author]
                giveawayEntries = giveawayEntries + _entry
                await bot.say(ctx.message.author.mention + " has entered into the giveaway!")
    else:
        await bot.say("ERROR: UNAUTHORIZED\nYou are not a full member! To gain access to giveaways, please submit an application.")
    
        
        
#Cleverbot integration
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.content.startswith(message.guild.get_member(botID).mention):
        if message.author.id != botID:
            await bot.send_typing(message.channel)
            stripmsg = message.content.replace('Katyusha, ', "")
            botmsg = cb.say(stripmsg)
            await bot.send_message(message.channel, message.author.mention + ': ' + botmsg)
    
    
#Runtime, baby! Let's go!    
print ('Getting ready...')
print('Loading Katyusha2 v' + VERSION)
create_tables()
load_quotes()
getTokens()
bot.run(botToken)