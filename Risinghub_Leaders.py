# imports
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
import asyncio
import math

# prefix
client = commands.Bot(command_prefix="!")

# to remove builtin help command
client.remove_command("help")

# bot token
token = "TOKEN HERE"

# on ready & presence activity event
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("battlefield heroes | !help"))
    print("Ready")

# cooldown event
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
       msg = await ctx.send("Cooldown soldier!! please retry in **{}s**.".format(math.ceil(error.retry_after)))
       await asyncio.sleep(5) 
       await msg.delete()
       await asyncio.sleep(6)
    else:
        print(error, on_command_error)

# rising hub logo
gameicon = "https://cdn.discordapp.com/attachments/710552597886664774/821345909883011082/rh_logo.png"

leaderboards = '''
    ``!top elo``, ``!top score``, ``!top level``, ``!top vp``, ``!top time``,
    ``!top kills``, ``!top assists``, ``!top deaths``, ``!top capture``,
    ``!top killstreak``, ``!top deathstreak``, ``!top prestige``
'''

# help
@client.command(pass_context=True, aliases=['Help'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def help(ctx):
    async with ctx.typing():
        embed = discord.Embed(
            discription = "discription",
            color = discord.Color.green()
        )

        embed.set_thumbnail(url=gameicon)
        
        embed.set_author(name="RisingHub leaderboards")

        embed.add_field(name="Usage", value=leaderboards, inline=False)

        embed.add_field(name="Links", value="[RisingHub](https://risinghub.net/) **|** [RisingHub Leaderboard](https://risinghub.net/leaderboard/score)\n \n Developer: <@289106753277263872>", inline=False)

        await ctx.send(embed=embed)

# leaderboards
@client.command(aliases=['Top', 'TOP'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def top(ctx,*value):
    async with ctx.typing():
        embed = discord.Embed(
            discription = "discription",
            color = discord.Color.green()
        )
    if not value:
        embed.add_field(name="Error", value="Value is not supplied, ``!help`` for usage info.", inline=False)
        await ctx.send(embed=embed)
        return        

    values = {"elo", "score", "level", "vp", "time", "kills", "assists", "deaths", "capture", "killstreak", "deathstreak", "prestige"}

    if value[0] in values:

        ses = requests.Session()

        # get token
        url1 = "https://risinghub.net/"
        response1 = ses.get(url1)
        soup1 = BeautifulSoup(response1.text, "html.parser")
        token = soup1.find("input")['value']

        # login
        url2 = "https://risinghub.net/login"
        username, password = "USERNAME HERE", "PASSWORD HERE"
        data = f"_token={token}&username={username}&password={password}&submit="
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }
        response2 = ses.post(url2, data=data, headers=headers)

        # leaderboard
        if value[0] == 'elo':
            url3 = "https://risinghub.net/leaderboard/elo"
        elif value[0] == 'score':
            url3 = "https://risinghub.net/leaderboard/score"
        elif value[0] == 'level':
            url3 = "https://risinghub.net/leaderboard/level"
        elif value[0] == 'vp':
            url3 = "https://risinghub.net/leaderboard/vp"
        elif value[0] == 'time':
            url3 = "https://risinghub.net/leaderboard/time"
        elif value[0] == 'kills':
            url3 = "https://risinghub.net/leaderboard/kills"
        elif value[0] == 'assists':
            url3 = "https://risinghub.net/leaderboard/assists"
        elif value[0] == 'deaths':
            url3 = "https://risinghub.net/leaderboard/deaths"
        elif value[0] == 'capture':
            url3 = "https://risinghub.net/leaderboard/capture"
        elif value[0] == 'killstreak':
            url3 = "https://risinghub.net/leaderboard/kill_streak"
        elif value[0] == 'deathstreak':
            url3 = "https://risinghub.net/leaderboard/death_streak"
        elif value[0] == 'prestige':
            url3 = "https://risinghub.net/leaderboard/prestige"
        response3 = ses.get(url3)
        soup2 = BeautifulSoup(response3.text, "html.parser")
        test = soup2.find("table")
        data = []
        table_body = soup2.find('tbody')
        rows = table_body.find_all('tr')
        for index, row in enumerate(rows):
            td = row.find_all('td')
            idx, name, score = [ele.text.strip() for ele in td]
            if index == 10:
                break
            embed.set_thumbnail(url=gameicon)
            embed.add_field(name=f"[{idx}] {name}", value=f"{score}", inline=False)
            embed.set_footer(text="Rising Hub Leaderboard active in 30 days.")
        await ctx.send(embed=embed)
    else:
        embed.add_field(name="Error", value="Value is not found, ``!help`` for usage info.", inline=False)
        await ctx.send(embed=embed)  

        
client.run(token)
