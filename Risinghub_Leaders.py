# imports
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
import asyncio
import math


# bot prefix
client = commands.Bot(command_prefix="PREFIX_HERE")

# to remove builtin help command
client.remove_command("help")

# bot token
token = "TOKEN_HERE"


# on ready & presence activity event
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("battlefield heroes | !help"))
    print('{0.user} bot is ready'.format(client))

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

# ping 
@client.command()
async def ping(ctx):
    await ctx.send(f"**{round(client.latency *1000)}** milliseconds!")

# logout the bot
@client.command(hidden=False, aliases=['Kill', 'logout', 'Logout'])
@commands.cooldown(1, 60, commands.BucketType.user)
async def kill(ctx):
    async with ctx.typing():
        dev_id = ID_HERE # it should be an int, for example: dev_id = 289106753277263872
        if dev_id == ctx.author.id:
            await client.logout()
            await client.close()
            await ctx.send("the bot has logged out")
        else:
            await ctx.send("you don't have permission to this command.")


# risinghub logo
rh_logo = "https://cdn.discordapp.com/attachments/710552597886664774/821345909883011082/rh_logo.png"

usage = '''
!top elo, !top score, !top level, !top vp,
!top deaths, !top capture, !top prestige,
!top time, !top kills, !top assists,
!top killstreak, !top deathstreak, 
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

        embed.set_thumbnail(url=rh_logo)
        
        embed.set_author(name="RisingHub leaderboards")

        embed.add_field(name="Usage", value=usage, inline=False)

        embed.add_field(name="Other", value="**!ping |** [RisingHub](https://risinghub.net/) **|** [RisingHub Leaderboard](https://risinghub.net/leaderboard/score)\n \n Developer: <@289106753277263872>", inline=False)

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

    values = {
        "elo", "Elo",
        "score", "Score",
        "level", "Level",
        "vp", "Vp", "VP",
        "time", "Time",
        "kills", "Kills",
        "assists", "Assists",
        "deaths", "Deaths",
        "capture", "Capture",
        "killstreak", "Killstreak",
        "deathstreak", "Deathstreak",
        "prestige", "Prestige"}

    if value[0] in values:

        ses = requests.Session()

        # get token
        url1 = "https://risinghub.net/"
        try:
            response1 = ses.get(url1)
        except Exception:
            print("Something went wrong")
        soup1 = BeautifulSoup(response1.text, "html.parser")
        token = soup1.find("input")['value']

        # login
        url2 = "https://risinghub.net/login"
        username, password = "USERNAME_HERE", "PASSWORD_HERE"
        data = f"_token={token}&username={username}&password={password}&submit="
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }
        try:
            response2 = ses.post(url2, data=data, headers=headers)
        except Exception:
            print("Something went wrong")

        # leaderboard
        if value[0] == ["elo", "Elo"]:
            url3 = "https://risinghub.net/leaderboard/elo"
        elif value[0] == ['score', 'Score']:
            url3 = "https://risinghub.net/leaderboard/score"
        elif value[0] == ['level', 'Level']:
            url3 = "https://risinghub.net/leaderboard/level"
        elif value[0] in ["vp","Vp", "VP"]:
            url3 = "https://risinghub.net/leaderboard/vp"
        elif value[0] == ['time', 'Time']:
            url3 = "https://risinghub.net/leaderboard/time"
        elif value[0] == ['kills', 'Kills']:
            url3 = "https://risinghub.net/leaderboard/kills"
        elif value[0] == ['assists', 'Assists']:
            url3 = "https://risinghub.net/leaderboard/assists"
        elif value[0] == ['deaths', 'Deaths']:
            url3 = "https://risinghub.net/leaderboard/deaths"
        elif value[0] == ['capture', 'Capture']:
            url3 = "https://risinghub.net/leaderboard/capture"
        elif value[0] == ['killstreak', 'Killstreak']:
            url3 = "https://risinghub.net/leaderboard/kill_streak"
        elif value[0] == ['deathstreak', 'Deathstreak']:
            url3 = "https://risinghub.net/leaderboard/death_streak"
        elif value[0] == ['prestige', 'Prestige']:
            url3 = "https://risinghub.net/leaderboard/prestige"
        try:
            response3 = ses.get(url3)
        except Exception:
            print("Something went wrong")
        soup2 = BeautifulSoup(response3.text, "html.parser")
        table_body = soup2.find('tbody')
        rows = table_body.find_all('tr')
        for index, row in enumerate(rows):
            td = row.find_all('td')
            idx, name, score = [ele.text.strip() for ele in td]
            if index == 10:
                break
            embed.set_thumbnail(url=rh_logo)
            embed.add_field(name=f"[{idx}] {name}", value=f"{score}", inline=False)
            embed.set_footer(text="Rising Hub Leaderboard active in 30 days.")
        await ctx.send(embed=embed)
    else:
        embed.add_field(name="Error", value="Value is not found, ``!help`` for usage info.", inline=False)
        await ctx.send(embed=embed)  


client.run(token)
