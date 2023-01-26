# Requirements:
# pip install httpx bs4 configparser py-cord lxml
# Python version: 3.9.7

import httpx, discord, math, re, json, os
from configparser import ConfigParser
from discord.ext import commands
from bs4 import BeautifulSoup
from discord import Option

bot = discord.Bot()

config = ConfigParser()
config.read('config.ini')

token = config['settings']['token']
username = config['settings']['username']
password = config['settings']['password']
author = int(config['settings']['author_id'])

logo = config['preferences']['logo']
nat_emoji = config['preferences']['nat_emoji']
roy_emoji = config['preferences']['roy_emoji']
soldier_emoji = config['preferences']['soldier_emoji']
gunner_emoji = config['preferences']['gunner_emoji']
commando_emoji = config['preferences']['commando_emoji']

class links:
    main = config['links']['main']
    login = config['links']['login']
    stats = config['links']['stats']
    servers = config['links']['servers']
    servers_api = config['links']['servers_api']
    profiles = config['links']['profiles']
    heroes = config['links']['heroes']
    name_availability = config['links']['name_availability']

headers = {
    "content-type": "application/x-www-form-urlencoded",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29",
    "x-requested-with": "XMLHttpRequest"
}

def login():
    session = httpx.Client()
    try:
        response1 = session.get(links.main, headers=headers)
    except Exception as error:
        print(f"Logging: {error}")

    soup = BeautifulSoup(response1.text, "lxml")
    crsf = soup.find("input")['value']

    payload = f"_token={crsf}&username={username}&password={password}&submit="
    try:
        response2 = session.post(links.login, data=payload, headers=headers)
    except Exception as error:
        print(f"Logging: {error}")

    return session

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("Battlefield Heroes"))
    print('bot is up.')

@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond("Cooldown soldier! please retry in **{}s**.".format(math.ceil(error.retry_after)), delete_after=5.0)
    else:
        print(error)

@bot.slash_command(hidden=True, description="Logout the bot.")
async def logout(ctx):
    if author == ctx.author.id:
        await ctx.respond("The bot has logged out!")
        await bot.close()
    else:
        await ctx.respond("You don't have permission to this command.")

@bot.slash_command(hidden=True, description="Restart the bot.")
async def restart(ctx):
    if author == ctx.author.id:
        await ctx.respond("Restarting...")
        await ctx.bot.logout()
        os.system('python bot.py')
    else:
        await ctx.respond("You don't have permission to this command.")

@bot.slash_command(description="Bot latency.")
@commands.cooldown(1, 5, commands.BucketType.user) # cooldown: 1 is the number of tries and 5 is the time in seconds
async def ping(ctx):
    embed = discord.Embed(color=discord.Color.green(),description=f"**{round(bot.latency *1000)}** ms")
    await ctx.respond(embed=embed)

@bot.slash_command(description="RisingHub stats.")
@commands.cooldown(1, 3, commands.BucketType.user)
async def stats(ctx):
    try:
        response = httpx.get(links.stats,headers=headers)
    except Exception as error:
        print(f"Logging: {error}")
        return

    soup = BeautifulSoup(response.text, "lxml")
    h6 = soup.find_all('h5')
    h3 = soup.find('h3').text

    embed = discord.Embed(title="RisingHub Stats", url=links.stats, color=discord.Color.green())
    embed.add_field(name="Stats", value=h3, inline=True)

    for roww in h6:
        dt = roww.find_all('dt')
        dd = roww.find_all('dd')
        ono = [e.text for e in dt]
        due = [c.text for c in dd]
        embed.set_thumbnail(url=logo)
        embed.add_field(name=f"{ono[0]}", value=f"{due[0]}", inline=True)
    await ctx.respond(embed=embed)

@bot.slash_command(description="Online servers list.")
@commands.cooldown(1, 3, commands.BucketType.user)
async def servers(ctx):
    try:
        response = httpx.get(links.servers, headers=headers)
    except Exception as error:
        print(f"Logging: {error}")
        return
    try:
        response2 = httpx.get(links.servers_api, headers=headers).json()
    except Exception as error:
        print(f"Logging: {error}")
        return

    soup = BeautifulSoup(response.text, "lxml")
    status = soup.find_all(class_="small-4 columns")
    players_online = status[4].text.strip()
    master_server = status[3].text.strip()
    active_servers = status[5].text.strip()

    embed = discord.Embed(title="RisingHub Servers", url=links.servers, description=f"Active Servers: **{active_servers}** | Players Online: **{players_online}**", color=discord.Color.green())

    for servers in response2['servers']:
        region = servers['region'].split(" ")[0]
        if region == "DE":
            flag = ":flag_de:"
        elif region == "FR":
            flag = ":flag_fr:"
        elif region == "PL":
            flag = ":flag_pl:"
        elif region == "NL":
            flag = ":flag_nl:"
        elif region == "FI":
            flag = ":flag_fi:"
        elif region == "EE":
            flag = ":flag_ee:"
        elif region == "BR":
            flag = ":flag_br:"
        elif region == "US":
            flag = ":flag_us:"
        elif region == "AU":
            flag = ":flag_au:"
        elif region == "RU":
            flag = ":flag_ru:"
        elif region == "SE":
            flag = ":flag_se:"
        else:
            flag = ":grey_question:"
        name = servers['name']
        map_ = servers['map']
        nats = servers['nats'][0]
        nmandos = servers['nats'][1]
        nsoldiers = servers['nats'][2]
        ngunners = servers['nats'][3]
        roys = servers['roys'][0]
        rmandos = servers['roys'][1]
        rsoldiers = servers['roys'][2]
        rgunners = servers['roys'][3]
        if servers['avg_lvl'] == 0:
            break
        embed.set_thumbnail(url=logo)
        embed.add_field(
            name=f"{flag} | {name} | {map_}",
            value=f"**{nats}** {nat_emoji} | {nmandos} {commando_emoji} | {nsoldiers} {soldier_emoji} | {ngunners} {gunner_emoji}\n**{roys}** {roy_emoji} | {rmandos} {commando_emoji} | {rsoldiers} {soldier_emoji} | {rgunners} {gunner_emoji}",
            inline=False)
    await ctx.respond(embed=embed)

@bot.slash_command(description="Top 10 leaderboards.")
@commands.cooldown(1, 3, commands.BucketType.user)
async def top(ctx, option: Option(description="Choose one from the list.", choices=["elo", "score", "level", "vp", "deaths", "capture", "prestige", "time", "wins", "kills", "assists", "losses", "killstreak", "deathstreak"])):
    try:
        response = httpx.get(f"https://risinghub.net/leaderboard/{option}/any/any", headers=headers)
    except Exception as error:
        print(f"Logging: {error}")
        return

    soup = BeautifulSoup(response.text, "lxml")
    table_body = soup.find('tbody')
    rows = table_body.find_all('tr')

    embed = discord.Embed(title=f"Top {option} leaderboard", url=f"https://risinghub.net/leaderboard/{option}/any/any", color=discord.Color.green())

    for index, row in enumerate(rows):
        td = row.find_all('td')
        idx, lvl, name, score = [ele.text.strip() for ele in td]
        if index == 10:
            break
        embed.set_thumbnail(url=logo)
        embed.add_field(name=f"[{idx}] {name}",value=f"{score}",inline=False)
        embed.set_footer(text="Rising Hub Leaderboard active in 30 days")
    await ctx.respond(embed=embed)

@bot.slash_command(description="Get user profile.")
@commands.cooldown(1, 3, commands.BucketType.user)
async def profile(ctx, username: Option(description="Enter a username.")):
    try:
        response = login().get(f"{links.profiles}{username}", headers=headers)
    except Exception as error:
        print(f"Logging: {error}")
        return

    if response.status_code == 404:
        await ctx.respond("Player was not found!")
    else:
        soup = BeautifulSoup(response.text, "lxml")
        name_and_status = soup.find(class_="pull-left")
        Username = name_and_status.text.split(" ")[0]
        status = name_and_status.text.split(" ")[2]

        if status == 'OFFLINE':
            emoji = ":red_circle:"
        elif status == 'ONLINE':
            emoji = ":green_circle:"

        if 'Donator' in response.text:
            info = "Donator :star:"
        else:
            info = ""

        heroes = ""
        names = soup.find_all(class_="hero-content shadow-2")
        for index, name in enumerate(names, start=1):
            all_heroes = name.a.text
            heroes += f"[{index}] {all_heroes}\n"

        level_text = soup.find_all("h6")[1].text
        total_level = re.search(r"\d+", level_text).group()
        created_text = soup.find_all("h6")[2].text.lstrip(" ")
        days = re.search(r"\d+", created_text).group()
        years = int(days) // 365

        embed = discord.Embed(title=f"{Username}'s profile {emoji}", url=f"{links.profiles}{username}", description=info, color=discord.Color.green())
        embed.set_thumbnail(url=logo)
        embed.add_field(name="Heros", value=f"{heroes}**Total heroes level**: {total_level}", inline=False)
        embed.add_field(name="Creation Time", value=f"{days} days, `{years} years ago`", inline=False)
        await ctx.respond(embed=embed)

@bot.slash_command(description="Get hero information.")
@commands.cooldown(1, 3, commands.BucketType.user)
async def hero(ctx, hero: Option(description="Enter a hero name.")):
    try:
        response = login().get(f"{links.heroes}{hero}", headers=headers)
    except Exception as error:
        print(f"Logging: {error}")
        return

    if response.status_code == 404:
        await ctx.respond("Hero was not found!")
    else:
        soup = BeautifulSoup(response.text, "lxml")
        h6 = soup.find_all('h6')
        prestige = soup.find('h4').text.strip()

        embed = discord.Embed(title=f"{hero}'s hero", url=f"{links.heroes}{hero}", description=f"**{prestige}**", color=discord.Color.green())
        for roww in h6:
            dt = roww.find_all('dt')
            dd = roww.find_all('dd')
            ono = [e.text for e in dt]
            due = [c.text for c in dd]
            embed.set_thumbnail(url=logo)
            try:
                embed.add_field(name=f"{ono[0]}", value=f"{due[0]}", inline=True)
            except:
                pass
        await ctx.respond(embed=embed)

@bot.slash_command(description="Check name availability.")
@commands.cooldown(1, 3, commands.BucketType.user)
async def name(ctx, name: Option(description="Enter a name.")):
    payload = f"heroName={name}"
    try:
        response = login().post(links.name_availability, data=payload, headers=headers)
    except Exception as error:
        print(f"Logging: {error}")
        return

    if response.status_code == 500:
        availability = "Taken!"
    elif response.status_code == 200:
        availability = "Availabil!"

    embed = discord.Embed(title="Hero Name Availability", description=f"**{name}** name is `{availability}`", color=discord.Color.green())
    embed.set_thumbnail(url=logo)
    await ctx.respond(embed=embed)

bot.run(token)
