from discord.ext import commands
from bs4 import BeautifulSoup
import discord
import asyncio
import httpx
import math
import json
import re
import os


# session
def login():
    session = httpx.Client()
    headers = {
    "content-type": "application/x-www-form-urlencoded",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29",
    "x-requested-with": "XMLHttpRequest"
    }
    # Get token
    try:
        response1 = session.get("https://pte.risinghub.net/", headers=headers)
    except Exception as error:
        print(f"Logging: {error}")

    soup = BeautifulSoup(response1.text, "html.parser")
    token = soup.find("input")['value']

    # Login
    username, password = "asdfasdf", "asdfasdf"
    payload = f"_token={token}&username={username}&password={password}&submit="
    try:
        response2 = session.post("https://pte.risinghub.net/login", data=payload, headers=headers)
    except Exception as error:
        print(f"Logging: {error}")

    return session


# bot settings
rh_logo = "https://risinghub.net/images/rh_logo.png"
bot = commands.Bot(command_prefix="!")
bot.remove_command("help")
token = "Token"


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("Battlefield Heroes"))
    print('bot is online.')


# error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = await ctx.send("Cooldown soldier!! please retry in **{}s**.".format(math.ceil(error.retry_after)))
        await asyncio.sleep(5)
        await msg.delete()
        await asyncio.sleep(6)
    else:
        print(f"Logging: {error} --> {on_command_error}")


# logout the bot
@bot.command(hidden=False, aliases=['Kill', 'logout', 'Logout'])
@commands.cooldown(1, 60, commands.BucketType.user)
async def kill(ctx):
    async with ctx.typing():
        if 289106753277263872 == ctx.author.id:
            await ctx.send("The bot has logged out!")
            await bot.logout()
            await bot.close()
        else:
            await ctx.send("You don't have permission to this command.")

          
# restart the bot
@bot.command()
async def restart(ctx):
    if 289106753277263872 == ctx.author.id:
      await ctx.send("Restarting...")
      await ctx.bot.logout()
      os.system('python bot.py')
    else:
      await ctx.send("You don't have permission to this command.")


# ping command
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user) # cooldown: 1 is the number of tries and 5 is the time in seconds
async def ping(ctx):
    async with ctx.typing():
        embed = discord.Embed(color = discord.Color.green(), description=f"**{round(bot.latency *1000)}** ms")
        await ctx.send(embed=embed)

      
# help
@bot.command(pass_context=True, aliases=['Help'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def help(ctx):
    async with ctx.typing():
        embed = discord.Embed(
          title="Commands",
          description="!top, !profile, !hero, !stats, !name, !ping\n\n[INVITE TO YOUR SERVER](https://discord.com/api/oauth2/authorize?client_id=821129463462625300&permissions=318528&scope=bot)\n**Developer**: <@289106753277263872>",
          color=discord.Color.green())
        embed.set_thumbnail(url=rh_logo)
        await ctx.send(embed=embed)


# stats
@bot.command(aliases=['Stats'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def stats(ctx,*value):
    async with ctx.typing():
        embed = discord.Embed(title = "RisingHub Stats", url="https://risinghub.net/stats", color = discord.Color.green())

        session = login()
        headers = {
          "content-type": "application/x-www-form-urlencoded",
          "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29",
          "x-requested-with": "XMLHttpRequest"
        }
        try:
            response = session.get("https://pte.risinghub.net/stats", headers=headers)
        except Exception as error:
            print(f"Logging: {error}")
            return

        soup = BeautifulSoup(response.text, "lxml")
        h6 = soup.find_all('h5')
        h3 = soup.find('h3').text
        embed.add_field(name="Stats", value=h3, inline=True)
        for roww in h6:
            dt = roww.find_all('dt')
            dd = roww.find_all('dd')
            ono = [e.text for e in dt]
            due = [c.text for c in dd]
            embed.set_thumbnail(url=rh_logo)
            embed.add_field(name=f"{ono[0]}", value=f"{due[0]}", inline=True)
        await ctx.send(embed=embed)


# leaderboards
@bot.command(aliases=['Top', 'TOP'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def top(ctx,*value):
    async with ctx.typing():
        if not value:
            embed = discord.Embed(color = discord.Color.green(), title="Usage", description=("""!top elo, !top score, !top level, !top vp,\n!top deaths, !top capture, !top prestige,\n!top time, !top wins, !top kills, !top assists,\n!top losses !top killstreak, !top deathstreak"""))
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(title = f"Top {value[0]} leaderboard", url=f"https://risinghub.net/leaderboard/{value[0]}/any/any", color = discord.Color.green())

        values = {
        "elo",
        "score",
        "level",
        "vp",
        "time",
        "kills",
        "assists",
        "deaths",
        "capture",
        "killstreak",
        "deathstreak",
        "wins",
        "losses",
        "prestige"
        }
        if value[0] in values:
            url = f"https://pte.risinghub.net/leaderboard/{value[0]}/any/any"
            session = login()
            headers = {
              "content-type": "application/x-www-form-urlencoded",
              "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29",
              "x-requested-with": "XMLHttpRequest"
            }
            try:
                response = session.get(url, headers=headers)
            except Exception as error:
                print(f"Logging: {error}")
                return
            
            soup = BeautifulSoup(response.text, "lxml")
            table_body = soup.find('tbody')
            rows = table_body.find_all('tr')
            for index, row in enumerate(rows):
                td = row.find_all('td')
                idx, lvl, name, score = [ele.text.strip() for ele in td]
                if index == 10:
                    break
                embed.set_thumbnail(url=rh_logo)
                embed.add_field(name=f"[{idx}] {name}", value=f"{score}", inline=False)
                embed.set_footer(text="Rising Hub Leaderboard active in 30 days")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Value was not found, `!top` for usage")


# user profile
@bot.command(aliases=['Profile', 'p', 'P'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def profile(ctx,*value):
    async with ctx.typing():
        if not value:
            embed = discord.Embed(color = discord.Color.green(), title="Usage", description="!profile [username]")
            await ctx.send(embed=embed)
            return

        session = login()
        headers = {
          "content-type": "application/x-www-form-urlencoded",
          "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29",
          "x-requested-with": "XMLHttpRequest"
        }
        try:
            response = session.get(f"https://pte.risinghub.net/profile/{value[0]}", headers=headers)
        except Exception as error:
            print(f"Logging: {error}")
            return

        if response.status_code == 404:
            await ctx.send("Player was not found!")
        else:
            soup = BeautifulSoup(response.text, "lxml")
            status = soup.find('td').text
          
            if status == 'OFFLINE':
                emoji = ":red_circle:"
            elif status == 'ONLINE':
                emoji = ":green_circle:"

            if 'Donator' in response.text:
                info = "Donator :star:"
            else:
                info = ""

            level_text = soup.find_all("h6")[1].text ; total_level = re.search(r"\d+", level_text).group()
            created_text = soup.find_all("h6")[2].text.lstrip(" ") ; days = re.search(r"\d+", created_text).group() ; years = int(days) // 365
            total_heros = soup.find_all(class_="hero-content shadow-2")

            embed = discord.Embed(title = f"{value[0]}'s profile", url=f"https://risinghub.net/profile/{value[0]}", description=info, color = discord.Color.green())
            embed.set_thumbnail(url=rh_logo)
            embed.add_field(name="Status", value=f"{status} {emoji}", inline=False)
            embed.add_field(name="Total Hero level", value=f"{total_level}", inline=False)
            embed.add_field(name="Total Heros", value=f"{len(total_heros)}", inline=False)
            embed.add_field(name="Creation Time", value=f"{days} days, `{years} years ago`", inline=False)
            await ctx.send(embed=embed)


# hero info
@bot.command(aliases=['Hero', 'h', 'H'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def hero(ctx, *value):
    async with ctx.typing():
        if not value:
            embed = discord.Embed(color = discord.Color.green(), title="Usage", description="!hero [heroname]")
            await ctx.send(embed=embed)
            return

        session = login()
        headers = {
          "content-type": "application/x-www-form-urlencoded",
          "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29",
          "x-requested-with": "XMLHttpRequest"
        }
        try:
            response = session.get(f"https://pte.risinghub.net/hero/{value[0]}", headers=headers)
        except Exception as error:
            print(f"Logging: {error}")
            return
            
        if response.status_code == 404:
            await ctx.send("Hero was not found!")
        else:
            soup = BeautifulSoup(response.text, "lxml")
            h6 = soup.find_all('h6')
            prestige = soup.find('h4').text.strip()
            embed = discord.Embed(title = f"{value[0]}'s hero", url=f"https://risinghub.net/hero/{value[0]}", description = f"**{prestige}**", color = discord.Color.green())
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
            await ctx.send(embed=embed)


# name availability
@bot.command(aliases=['Name', 'n', 'N'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def name(ctx, *value):
    async with ctx.typing():
        if not value:
            embed = discord.Embed(color = discord.Color.green(), title="Usage", description="!name [name]")
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(color = discord.Color.green())

        session = login()
        headers = {
          "content-type": "application/x-www-form-urlencoded",
          "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29",
          "x-requested-with": "XMLHttpRequest"
        }
        payload = f"heroName={value[0]}"
        try:
            response = session.post("https://pte.risinghub.net/profile/create/hero/availability", data=payload, headers=headers)
        except Exception as error:
            print(f"Logging: {error}")
            return

    if response.status_code == 500:
        name = "Taken!"
    elif response.status_code == 200:
        name = "Availabil!"

    embed = discord.Embed(title = "Hero Name Availability", description  = f"**{value[0]}** name is `{name}`",  color = discord.Color.green())
    embed.set_thumbnail(url=rh_logo)
    await ctx.send(embed=embed)


bot.run(token)
