# imports
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
import asyncio
import math


# bot prefix
client = commands.Bot(command_prefix="!")

# to remove builtin help command
client.remove_command("help")

# bot token
token = "<TOKEN_HERE>"


# on ready event & presence activity
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("battlefield heroes"))
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
@commands.cooldown(1, 5, commands.BucketType.user) # cooldown: 1 is the number of tries and 5 is the time in seconds
async def ping(ctx):
    async with ctx.typing():
        await ctx.send(f"**{round(client.latency *1000)}** milliseconds!")

# logout the bot
@client.command(hidden=False, aliases=['Kill', 'logout', 'Logout'])
@commands.cooldown(1, 60, commands.BucketType.user)
async def kill(ctx):
    async with ctx.typing():
        dev_id = 289106753277263872 # it should be an int, for example: dev_id = 289106753277263872
        if dev_id == ctx.author.id:
            await ctx.send("The bot has logged out!")
            await client.logout()
            await client.close()
        else:
            await ctx.send("You don't have permission to this command.")


# risinghub logo
rh_logo = "https://cdn.discordapp.com/attachments/710552597886664774/821345909883011082/rh_logo.png"

leaderboards = '''
!top elo, !top score, !top level, !top vp,
!top deaths, !top capture, !top prestige,
!top time, !top kills, !top assists,
!top killstreak, !top deathstreak
'''
player = '''
!hero <playername> <heroname>
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
        embed.set_author(name="RisingHub Bot")
        embed.add_field(name="Player statistics", value=player, inline=False)
        embed.add_field(name="Leaderboards", value=leaderboards, inline=False)
        embed.add_field(name="Other", value="**!team, !ping | [RisingHub](https://risinghub.net/)** \n \n Developer: <@289106753277263872>", inline=False)
        await ctx.send(embed=embed)


lead = '''
[DarkVenom](https://risinghub.net/profile/DarkVenom)
[Potskard](https://risinghub.net/profile/Potskard)
[MHx489](https://risinghub.net/profile/MHx489)
'''
staff = '''
[Estoniangirl](https://risinghub.net/profile/Estoniangirl)
[Freakin](https://risinghub.net/profile/Freakin)
[Superpaul2](https://risinghub.net/profile/Superpaul2)
'''
dev = '''
[Maybeads](https://risinghub.net/profile/Maybeads)
'''

# rising hub team
@client.command(aliases=['Team'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def team(ctx):
    async with ctx.typing():
        embed = discord.Embed(
            discription = "discription",
            color = discord.Color.green()
        )

        embed.set_thumbnail(url=rh_logo)
        embed.add_field(name="Rising Lead", value=lead, inline=False)
        embed.add_field(name="Rising Staff", value=staff, inline=False)
        embed.add_field(name="Rising Dev", value=dev, inline=False)
        embed.set_footer(text="RisingHub Team")
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
        embed.add_field(name="Error", value="Value is not supplied, **!help** command for usage info.", inline=False)
        await ctx.send(embed=embed)
        return

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
        # leaderboard
        if value[0] in ["elo", "Elo"]:
            url3 = "https://risinghub.net/leaderboard/elo"
        elif value[0] in ['score', 'Score']:
            url3 = "https://risinghub.net/leaderboard/score"
        elif value[0] in ['level', 'Level']:
            url3 = "https://risinghub.net/leaderboard/level"
        elif value[0] in ["vp", "Vp", "VP"]:
            url3 = "https://risinghub.net/leaderboard/vp"
        elif value[0] in ['time', 'Time']:
            url3 = "https://risinghub.net/leaderboard/time"
        elif value[0] in ['kills', 'Kills']:
            url3 = "https://risinghub.net/leaderboard/kills"
        elif value[0] in ['assists', 'Assists']:
            url3 = "https://risinghub.net/leaderboard/assists"
        elif value[0] in ['deaths', 'Deaths']:
            url3 = "https://risinghub.net/leaderboard/deaths"
        elif value[0] in ['capture', 'Capture']:
            url3 = "https://risinghub.net/leaderboard/capture"
        elif value[0] in ['killstreak', 'Killstreak']:
            url3 = "https://risinghub.net/leaderboard/kill_streak"
        elif value[0] in ['deathstreak', 'Deathstreak']:
            url3 = "https://risinghub.net/leaderboard/death_streak"
        elif value[0] in ['prestige', 'Prestige']:
            url3 = "https://risinghub.net/leaderboard/prestige"
        else:
            pass

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
        embed.add_field(name="Error", value="Value is not found, **!help** command for usage info.", inline=False)
        await ctx.send(embed=embed)


# hero info
@client.command(aliases=['Hero'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def hero(ctx,*value):
    async with ctx.typing():
        embed = discord.Embed(
            discription = "discription",
            color = discord.Color.green()
        )
    if not value:
        embed.add_field(name="Error", value="Value is not supplied, **!help** command for usage info.", inline=False)
        await ctx.send(embed=embed)
        return

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

    if len(value) == 2:
        # hero info
        playername, heroname = f"{value[0]}", f"{value[1]}"
        url5 = f"https://risinghub.net/profile/{playername}/{heroname}"
        try:
            response5 = ses.get(url5)
        except Exception:
            print("Something went wrong")
        if "https://risinghub.net/images/404_slider.png" in response5.text:
            embed.add_field(name="Error", value="Player not found, **!help** command for usage info.", inline=False)
            await ctx.send(embed=embed)
        else:
            soup5 = BeautifulSoup(response5.text, "lxml")
            h6 = soup5.find_all('h6')
            for roww in h6:
                dt = roww.find_all('dt')
                dd = roww.find_all('dd')
                ono = [e.text.strip() for e in dt]
                due = [c.text.strip().replace(" ", "") for c in dd]
                embed.set_thumbnail(url=rh_logo)
                try:
                    embed.add_field(name=f"{ono[0]}", value=f"{due[0]}", inline=True)
                except:
                    pass
                embed.set_footer(text=f"Hero statistics for {value[1]}")
            await ctx.send(embed=embed)
    else:
        embed.add_field(name="Error", value="Player not found, **!help** command for usage info.", inline=False)
        await ctx.send(embed=embed)

client.run(token)
