# imports
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
import asyncio
import math


# bot settings
client = commands.Bot(command_prefix="!")
client.remove_command("help")
token = "TOKEN_HERE"

# bot events
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("Battlefield Heroes"))
    print('{0.user} bot is ready'.format(client))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = await ctx.send("Cooldown soldier!! please retry in **{}s**.".format(math.ceil(error.retry_after)))
        await asyncio.sleep(5)
        await msg.delete()
        await asyncio.sleep(6)
    else:
        print(error, on_command_error)

# ping command
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


rh_logo = "https://cdn.discordapp.com/attachments/710552597886664774/821345909883011082/rh_logo.png"

leaderboards = '''
!top elo, !top score, !top level, !top vp,
!top deaths, !top capture, !top prestige,
!top time, !top kills, !top assists,
!top killstreak, !top deathstreak
'''
player = '''
!hero <playername> <heroname>
!player <playername>
'''
lead = '''
[DarkVenom](https://risinghub.net/profile/DarkVenom)
[Potskard](https://risinghub.net/profile/Potskard)
[MHx489](https://risinghub.net/profile/MHx489)
'''
staff = '''
[Estoniangirl](https://risinghub.net/profile/Estoniangirl)
[Freakin](https://risinghub.net/profile/Freakin)
'''
dev = '''
[Maybeads](https://risinghub.net/profile/Maybeads)
'''
invite_link = 'https://discord.com/api/oauth2/authorize?client_id=821129463462625300&permissions=318528&scope=bot'


# help
@client.command(pass_context=True, aliases=['Help'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def help(ctx):
    async with ctx.typing():
        embed = discord.Embed(
            color = discord.Color.green()
        )

        embed.set_thumbnail(url=rh_logo)
        embed.add_field(name="Commands", value="!top, !hero, !stats, !team, !ping", inline=False)
        embed.add_field(name="Links", value=f"[INVITE TO YOUR SERVER]({invite_link}) **|** [Rising Hub](https://risinghub.net/)\n\n**Developer**: <@289106753277263872>", inline=False)
        await ctx.send(embed=embed)

# login &  token
def login():
    ses = requests.Session()
    # get token
    url1 = "https://risinghub.net/"
    try:
        response1 = ses.get(url1)
    except Exception:
        print("Something went wrong")
    soup1 = BeautifulSoup(response1.text, "html.parser")
    token = soup1.find("input")['value']

    # # login
    url2 = "https://risinghub.net/login"
    username, password = "freefire", "omar1230"
    data = f"_token={token}&username={username}&password={password}&submit="
    headers = {
    "content-type": "application/x-www-form-urlencoded",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    try:
        response2 = ses.post(url2, data=data, headers=headers)
    except Exception:
        print("Something went wrong")
    return ses

# stats
@client.command(aliases=['Stats'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def stats(ctx,*value):
    async with ctx.typing():
        embed = discord.Embed(
            color = discord.Color.green()
        )

    url6 = "https://risinghub.net/stats"
    try:
        response6 = login().get(url6)
    except Exception:
        print("Something went wrong")
    soup6 = BeautifulSoup(response6.text, "lxml")
    h6 = soup6.find_all('h5')
    h3 = soup6.find('h3').text
    embed.add_field(name="Stats", value=h3, inline=False)
    for roww in h6:
        dt = roww.find_all('dt')
        dd = roww.find_all('dd')
        ono = [e.text for e in dt]
        due = [c.text for c in dd]
        embed.set_thumbnail(url=rh_logo)
        embed.add_field(name=f"{ono[0]}", value=f"{due[0]}", inline=True)
        embed.set_footer(text=f"Rising Hub Stats")
    await ctx.send(embed=embed)

# rising hub team
@client.command(aliases=['Team'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def team(ctx):
    async with ctx.typing():
        embed = discord.Embed(
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
            color = discord.Color.green()
        )
    if not value:
        embed.add_field(name="Usage", value=leaderboards, inline=False)
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
        if value[0] in ["elo", "Elo"]:
            url3 = "https://risinghub.net/leaderboard/elo/any/any"
        elif value[0] in ['score', 'Score']:
            url3 = "https://risinghub.net/leaderboard/score/any/any"
        elif value[0] in ['level', 'Level']:
            url3 = "https://risinghub.net/leaderboard/level/any/any"
        elif value[0] in ["vp", "Vp", "VP"]:
            url3 = "https://risinghub.net/leaderboard/vp/any/any"
        elif value[0] in ['time', 'Time']:
            url3 = "https://risinghub.net/leaderboard/time/any/any"
        elif value[0] in ['kills', 'Kills']:
            url3 = "https://risinghub.net/leaderboard/kills/any/any"
        elif value[0] in ['assists', 'Assists']:
            url3 = "https://risinghub.net/leaderboard/assists/any/any"
        elif value[0] in ['deaths', 'Deaths']:
            url3 = "https://risinghub.net/leaderboard/deaths/any/any"
        elif value[0] in ['capture', 'Capture']:
            url3 = "https://risinghub.net/leaderboard/capture/any/any"
        elif value[0] in ['killstreak', 'Killstreak']:
            url3 = "https://risinghub.net/leaderboard/kill_streak/any/any"
        elif value[0] in ['deathstreak', 'Deathstreak']:
            url3 = "https://risinghub.net/leaderboard/death_streak/any/any"
        elif value[0] in ['prestige', 'Prestige']:
            url3 = "https://risinghub.net/leaderboard/prestige/any/any"
        else:
            pass

        try:
            response3 = login().get(url3)
        except Exception:
            print("Something went wrong")
        soup2 = BeautifulSoup(response3.text, "html.parser")
        table_body = soup2.find('tbody')
        rows = table_body.find_all('tr')
        for index, row in enumerate(rows):
            td = row.find_all('td')
            idx, lvl, name, score = [ele.text.strip() for ele in td]
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
@client.command(aliases=['Hero', 'Player', 'player'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def hero(ctx,*value):
    async with ctx.typing():
        embed = discord.Embed(
            color = discord.Color.green()
        )
    if not value:
        embed.add_field(name="Usage", value=player, inline=False)
        await ctx.send(embed=embed)
        return

    if len(value) == 1:
        url4 = f"https://risinghub.net/profile/{value[0]}"
        try:
            response4 = login().get(url4)
        except Exception:
            print("Something went wrong")
        if "https://risinghub.net/images/404_slider.png" in response4.text:
            embed.add_field(name="Error", value="Player not found, **!help** command for usage info.", inline=False)
            await ctx.send(embed=embed)
        else:
            soup4 = BeautifulSoup(response4.text, "lxml")
            try:
                info = soup4.find('h4').text
            except:
                pass
            status = soup4.find('td').text
            if status == 'OFFLINE':
                emoji = ":red_circle:"
            else:
                emoji = ":green_circle:"
            embed.set_thumbnail(url=rh_logo)
            embed.add_field(name="Status", value=f"{status} {emoji}", inline=True)
            try:
                embed.add_field(name="Info", value=f"{info}", inline=True)
            except:
                pass
            await ctx.send(embed=embed)
            return
    else:
        playername, heroname = f"{value[0]}", f"{value[1]}"
        url5 = f"https://risinghub.net/profile/{playername}/{heroname}"
        try:
            response5 = login().get(url5)
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
                ono = [e.text for e in dt]
                due = [c.text for c in dd]
                embed.set_thumbnail(url=rh_logo)
                try:
                    embed.add_field(name=f"{ono[0]}", value=f"{due[0]}", inline=True)
                except:
                    pass
                embed.set_footer(text=f"Hero statistics for {value[1]}")
            await ctx.send(embed=embed)


client.run(token)
