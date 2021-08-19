import requests
import json
import locale
import discord, asyncio
import itertools
import random
from datetime import datetime, timezone
from dateutil import parser
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
from discord.ext.commands import CommandNotFound

dev = "nekooooooooo#0120"
coinGeckoImageURL = "https://cdn.discordapp.com/attachments/872026951810973706/875624142379048980/CoinGecko_Logo.png"
coinGeckoURL = "https://www.coingecko.com/en/coins/"

prefix = 'sg!'

locale.setlocale(locale.LC_ALL, '')

def getCoinsJson():
    URL = "https://api.coingecko.com/api/v3/coins/list"
    r = requests.get(url=URL)
    data = r.json()
    coins = []

    print("Getting Coins...")

    for i in range(len(data)):
        coins.append(data[i]['id'])

        # progress = (i + 1) / len(data)
        # print(format(progress * 100, '.2f'), f'{i+1}/{len(data)}')

    print("Done...")

    return coins

def getCurrenciesJson():
    URL = "https://api.coingecko.com/api/v3/simple/supported_vs_currencies"
    r = requests.get(url=URL)
    data = r.json()
    currencies = []

    print("Getting Currencies...")

    for i in range(len(data)):
        currencies.append(data[i])

        # progress = (i + 1) / len(data)
        # print(format(progress * 100, '.2f'), f'{i+1}/{len(data)}')

    currencies.append('all')

    print("Done...")
    return currencies

coinsList = getCoinsJson()
currenciesList = getCurrenciesJson()

def isCoinSupported(crypto):
    if crypto in coinsList:
        return True
    else: 
        return False

def coinNotSupportedEmbed(ctx, crypto):
    embed = discord.Embed(
        title = f"❌ Coin '{crypto}' is not supported",
        color = discord.Color.red()
    )
    embed.add_field(
        name = "You can try using the full name and substitute space with hyphen.",
        value = f"`ex. smooth love potion 👉 smooth-love-potion`",
        inline = False
    )
    embed.set_author(
        name = ctx.author.display_name,
        icon_url = ctx.author.avatar_url
    )
    embed.set_footer(
        text = "Message nekooooooooo#0120 if you want a coin supported",
        icon_url = "https://cdn.discordapp.com/avatars/299747390888345600/84613a7996f2886517ae2c2e164e0eab.png?size=256"
    )
    embed.set_image(
        url = "https://cdn.discordapp.com/attachments/875348794634563596/876783597992960020/YQ50cOf5WIAAAAASUVORK5CYII.png"
    )
    return embed

def isCurrencySupported(currency):
    if currency in currenciesList:
        return True
    else: 
        return False
   
def currencyNotSupportedEmbed(ctx, currency):
    embed = discord.Embed(
        title = f"❌ Currency '{currency}' is not supported",
        color = discord.Color.red()
    )
    embed.set_author(
        name = ctx.author.display_name,
        icon_url = ctx.author.avatar_url
    )
    embed.set_footer(
        text = "Message nekooooooooo#0120 if you want a coin supported",
        icon_url = "https://cdn.discordapp.com/avatars/299747390888345600/84613a7996f2886517ae2c2e164e0eab.png?size=256"
    )
    formatCurrencies = ''

    for i in currenciesList:
        currency = i
        formatCurrencies += f"`{currency}` "

    embed.description = f"List of Supported Currencies\n{formatCurrencies}"
    return embed

def getCoinJson(crypto):
    URL = f'https://api.coingecko.com/api/v3/coins/{crypto}'
    r = requests.get(url=URL)
    data = r.json()
    return data

# def getCryptoPrice(crypto, currency):
#     data = getCoinsJson(crypto)
#     return data['market_data']['current_price'][currency]

# def getAllCryptoPrices(crypto):
#     data = getCoinsJson(crypto)
#     return data['market_data']['current_price']

def cryptoDictionary(crypto):
    return {
        'slp': 'smooth-love-potion',
        'zoon': 'cryptozoon',
        'eth': 'ethereum',
        'btc': 'bitcoin',
        'dnd': 'dungeonswap',
        'axs': 'axie-infinity',
        'tlm': 'alien-worlds',
        'doge': 'dogecoin',
        'dpet': 'my-defi-pet',
        'usdt': 'tether',
        'ada': 'cardano',
        'xrp': 'xrp',
        'usdc': 'usd-coin',
        'busd': 'binance-usd',
        'rune': 'thorchain',
        'ftt': 'ftx-token'
    }.get(crypto, crypto)

def currencyDictionary(currency):
    return {
        'php': '🇵🇭 PHP',
        'usd': '🇺🇸 USD',
        'aud': '🇦🇺 AUD',
        'eur': '🇪🇺 EUR',
        'btc': '<:bitcoin:875781933722894366> BTC',
        'eth': '<:binance:875781786687393872> ETH',
        'bnb': '<:ethereum:875781746287845386> BNB'
    }.get(currency, currency)

# print(getCryptoPrice('smooth-love-potion', 'php'))

def getPrefix(bot, msg):
    return [f"{prefix} ", f"{prefix}"]

activity = discord.Game(name="Use sg!help | neko")

client = commands.Bot(
    command_prefix = getPrefix,
    activity = activity,
    status = discord.Status.online,
    case_insensitive = True,
    help_command = None
)

def splitDict(d):
    n = len(d) // 2          # length of smaller half
    i = iter(d.items())      # alternatively, i = d.iteritems() works in Python 2

    d1 = dict(itertools.islice(i, n))   # grab first n items
    d2 = dict(i)                        # grab the rest

    return d1, d2

embedOne = discord.Embed(
    title = "Page #1", #Any title will do
)

embedTwo = discord.Embed(
    title = "Page #2",
)
embedThree = discord.Embed(
    title = "Page #3",
)

paginationList = [embedOne, embedTwo, embedThree]

DiscordComponents(client)

cryptoCommandList = ['price', 'convert']
infoCommandList = ['help', 'info', 'todo']

@client.event
async def on_ready():
    print(f'SaltyG is running...')

@client.event
async def on_message(msg):
    pfx = getPrefix(client, msg)[1]
    if msg.content.lower().startswith(pfx):
        msg.content = msg.content[:len(pfx)].lower() + msg.content[len(pfx):]
    await client.process_commands(msg)

@client.command(aliases=['p'])
async def price(ctx, crypto, currency = 'all'):

    crypto = crypto.lower()
    currency = currency.lower()

    crypto = cryptoDictionary(crypto)

    if not isCoinSupported(crypto):
        await ctx.send(embed = coinNotSupportedEmbed(ctx, crypto))
        return

    if not isCurrencySupported(currency):
        await ctx.send(embed = currencyNotSupportedEmbed(ctx, currency))
        return

    cryptoData = getCoinJson(crypto)

    dateNow = datetime.now(timezone.utc)

    cryptoId = cryptoData['id']
    cryptoName = cryptoData['name']
    cryptoSymbol = cryptoData['symbol']
    cryptoAddress = cryptoData['contract_address'] if 'contract_address' in cryptoData else "None"
    cryptoDesc = cryptoData['description']['en']
    cryptoImageURL = cryptoData['image']['large']
    cryptoPriceChange24h = cryptoData['market_data']['price_change_percentage_24h']
    cryptoPriceChange = cryptoData['market_data']['price_change_percentage_24h_in_currency']
    cryptoLastUpdated = parser.parse(cryptoData['last_updated'])

    subtractedDate = dateNow - cryptoLastUpdated

    m, s = divmod(subtractedDate.total_seconds(), 60)
    h, m = divmod(m, 60)

    if h > 0:
        fromNow = f"{h} hour/s {m} minute/s {s} second/s ago"
    elif h < 0 and m > 0:
        fromNow = f"{m} minute/s {s} second/s ago"
    elif s > 1:
        fromNow = f"{format(s, '.0f')} seconds ago"
    else: 
        fromNow = f"{format(s, '.0f')} second ago"

    embed = discord.Embed()

    # SMALL ICON
    
    # embed.set_author(
    #     name = cryptoName,
    #     icon_url = cryptoImageURL
    # )

    embed.set_author(
        name = f"{cryptoName} ({cryptoSymbol.upper()})"
    )

    embed.set_thumbnail(
        url = cryptoImageURL
    )

    embed.set_footer(
        text = "Powered by CoinGecko | sg!info for invite",
        icon_url = coinGeckoImageURL
    )

    if currency.lower() in ['a', 'all']:

        prices = cryptoData['market_data']['current_price']
        if cryptoPriceChange24h > 0:
            embed.color = discord.Color.green()
        else:
            embed.color = discord.Color.red()

        # pricesJson = json.dumps(prices, indent=4, sort_keys=True)
        # print(pricesJson)
        # await ctx.send(pricesJson)
        # await ctx.send(embed = embed)
        # await ctx.send(f'%s'%prices)
        # await ctx.send(prices)

        for x in prices:
            # print(prices[x], x)  
            currencies = x 

            if currencies in ['usd', 'php', 'aud', 'eur', 'btc', 'eth', 'bnb']:

                priceChange = cryptoPriceChange[currencies]
                currencies = currencyDictionary(currencies) 

                if priceChange > 0:
                    sign = '+'
                else:
                    sign = ''

                if prices[x] >= 1:
                    prices[x] = '{:,.2f}'.format(prices[x])
                else:
                    prices[x] = '{:,.8f}'.format(prices[x])

                embed.add_field(
                    name = currencies,
                    value = f"**```{prices[x]} ({sign}{format(priceChange, '.2f')}%)```**"
                )

        embed.add_field(
            name = "Last Updated",
            value = f'{fromNow}',
            # value = f'{cryptoLastUpdated.strftime("%I:%M:%S %p %Z")} ({fromNow})',
            inline = False
        )

        embed.add_field(
            name = "Links",
            value = f'[CoinGecko]({coinGeckoURL}{cryptoId})',
            inline = True
        )  

    else:
        price = float(cryptoData['market_data']['current_price'][currency])
        priceChange = cryptoPriceChange[currency]

        if price >= 1:
            price = '{:,.2f}'.format(price)
        else:
            price = '{:,.8f}'.format(price)

        if priceChange > 0:
            sign = '+'
            embed.color = discord.Color.green()
        else:
            sign = ''
            embed.color = discord.Color.red()

        currency = currencyDictionary(currency)
        # await ctx.send(f'Price: %s %s'%(currency.upper(), price))
        embed.add_field(
            name = currency.upper(),
            value = f"**```{price} ({sign}{format(priceChange, '.2f')}%)```**",
            inline = False
        )

        embed.add_field(
            name = "Last Updated",
            value = f'{fromNow}',
            # value = f'{cryptoLastUpdated.strftime("%I:%M:%S %p %Z")} ({fromNow})',
            inline = True
        )

        embed.add_field(
            name = "Links",
            value = f'[CoinGecko]({coinGeckoURL}{cryptoId})',
            inline = True
        )

    # embed.add_field(
    #     name = "Address",
    #     value = cryptoAddress,
    #     inline = False
    # )

    await ctx.send(embed = embed)

@price.error
async def price_error(ctx, error):

    print(error)

    embed = discord.Embed(
        color = discord.Color.red()
    )

    embed.set_author(
        name = ctx.author.display_name,
        icon_url = ctx.author.avatar_url
    )

    if isinstance(error, commands.MissingRequiredArgument):
        embed.description = "❌ Invalid <crypto> <currency | all> argument given. \n\nUsage:\n```price <crypto> <currency>```"
        await ctx.send(embed = embed)
        # await ctx.send('Invalid <crypto> <currency> argument given')
        # await ctx.send('Usage: price <crypto> <currency>')
        return

@client.command(
    aliases = ['cv']
)
async def convert(ctx, amount: int, crypto, currency):
    crypto = cryptoDictionary(crypto)

    crypto = crypto.lower()
    currency = currency.lower()

    amount = float(amount)

    if amount < 0:
        embed = discord.Embed(
            title = "❌ Invalid Amount",
            description = "Amount must be more than 0!",
            color = discord.Color.red()
        )
        embed.set_author(
            name = ctx.author.display_name,
            icon_url = ctx.author.avatar_url
        )
        await ctx.send(embed = embed)
        return

    if amount < 0:
        embed = discord.Embed(
            title = "❌ Invalid Amount",
            description = "Amount must be more than 0!",
            color = discord.Color.red()
        )
        embed.set_author(
            name = ctx.author.display_name,
            icon_url = ctx.author.avatar_url
        )
        await ctx.send(embed = embed)
        return

    if not isCoinSupported(crypto):
        await ctx.send(embed = coinNotSupportedEmbed(ctx, crypto))
        return

    if not isCurrencySupported(currency):
        await ctx.send(embed = currencyNotSupportedEmbed(ctx, currency))
        return

    cryptoData = getCoinJson(crypto)
    cryptoId = cryptoData['id']
    cryptoName = cryptoData['name']
    cryptoSymbol = cryptoData['symbol']
    cryptoAddress = cryptoData['contract_address'] if 'contract_address' in cryptoData else "None"
    cryptoDesc = cryptoData['description']['en']
    cryptoImageURL = cryptoData['image']['large']

    embed = discord.Embed(
        description = f"Converted {cryptoSymbol.upper()} {amount} to {currency.upper()}",
        color = discord.Color.gold()
    )

    embed.set_author(
        name = f"{cryptoName} ({cryptoSymbol.upper()})"
    )

    embed.set_thumbnail(
        url = cryptoImageURL
    )

    embed.set_footer(
        text = "Powered by CoinGecko | sg!info for invite",
        icon_url = coinGeckoImageURL
    )

    price = float(cryptoData['market_data']['current_price'][currency])

    total = float(amount) * price

    if price >= 1:
        price = '{:,.2f}'.format(price)
    else:
        price = '{:,.8f}'.format(price)

    if total >= 1:
        total = '{:,.2f}'.format(total)
    else:
        total = '{:,.8f}'.format(total)

    currency = currencyDictionary(currency)
    # await ctx.send(f'Price: %s %s'%(currency.upper(), price))
    embed.add_field(
        name = cryptoSymbol.upper(),
        value = '**```{:.2f}```**'.format(amount),
        inline = True
    )

    embed.add_field(
        name = currency.upper(),
        value = f'**```{price}```**',
        inline = True
    )

    embed.add_field(
        name = f"Total in {currency.upper()}",
        value = f'**```{total}```**',
        inline = False
    )
    
    embed.add_field(
        name = "Links",
        value = f'[CoinGecko]({coinGeckoURL}{cryptoId})',
        inline = False
    )

    # embed.add_field(
    #     name = "Address",
    #     value = cryptoAddress,
    #     inline = False
    # )

    await ctx.send(embed = embed)

@convert.error
async def convert_error(ctx, error):
    print(error)

    embed = discord.Embed(
        color = discord.Color.red()
    )

    embed.set_author(
        name = ctx.author.display_name,
        icon_url = ctx.author.avatar_url
    )

    if isinstance(error, commands.BadArgument):
        embed.title = "❌ Invalid <amount> argument given."
        embed.description =  "<amount> must be a number.\n\nUsage:\n```convert <amount> <crypto> <currency>```"
        await ctx.send(embed = embed)
        # await ctx.send('Invalid <crypto> <currency> argument given')
        # await ctx.send('Usage: price <crypto> <currency>')
        return

    if isinstance(error, commands.MissingRequiredArgument):
        embed.description = "❌ Invalid <amount> <crypto> <currency> argument given. \n\nUsage:\n```convert <amount> <crypto> <currency>```"
        await ctx.send(embed = embed)
        # await ctx.send('Invalid <crypto> <currency> argument given')
        # await ctx.send('Usage: price <crypto> <currency>')
        return

@client.command(
    name = "info",
    alias = ["i"]
)
async def info(ctx):
    embed = discord.Embed(
        color = discord.Color.from_hsv(random.randint(0,255), random.randint(200,255), random.randint(200,255))
    )

    embed.add_field(
        name = "Version",
        value = "0.0.1",
        inline = True
    )

    embed.add_field(
        name = "Library",
        value = "[Discord.py](https://discordpy.readthedocs.io/en/stable/#)",
        inline = True
    )

    embed.add_field(
        name = "Prefix",
        value = f"{prefix}",
        inline = True
    )

    embed.add_field(
        name = "Servers",
        value = len(client.guilds),
        inline = True
    )

    embed.add_field(
        name = "Users",
        value = len(client.users),
        inline = True
    )

    embed.add_field(
        name = "Developer",
        value = "nekooooooooo#0120",
        inline = False
    )

    embed.add_field(
        name = "Invite",
        value = "Bot is currently private.\nIf you want the bot added to your server\n contact me nekooooooooo#0120",
        inline = False
    )

    embed.set_author(
        name = client.user.name,
        icon_url = client.user.avatar_url
    )

    embed.set_footer(
        text = f"Prefix {prefix} | This bot is still under construction"
    )

    await ctx.send(embed = embed)

@client.command(
    name = "todo"
)
async def todo(ctx):
    embed = discord.Embed(
        title = "📝 TODO LIST",
        color = discord.Color.gold()
    )

    embed.description = f"""
    • Price Alerts
    • Market Chart (Candles)
    • Price Chart
    """

    embed.set_footer(
        text = f"Prefix {prefix} | This bot is still under construction"
    )

    await ctx.send(embed = embed)

@client.command(
    name = "pagination",
    aliases = ["pages"]
)
async def pagination(ctx):
    #Sets a default embed
    current = 0
    #Sending first message
    #I used ctx.reply, you can use simply send as well
    mainMessage = await ctx.send(
        "**Pagination!**",
        embed = paginationList[current],
        components = [ #Use any button style you wish to :)
            [
                Button(
                    label = "Prev",
                    id = "back",
                    style = ButtonStyle.red
                ),
                Button(
                    label = f"Page {int(paginationList.index(paginationList[current])) + 1}/{len(paginationList)}",
                    id = "cur",
                    style = ButtonStyle.grey,
                    disabled = True
                ),
                Button(
                    label = "Next",
                    id = "front",
                    style = ButtonStyle.red
                )
            ]
        ]
    )
    #Infinite loop
    while True:
        #Try and except blocks to catch timeout and break
        try:
            interaction = await client.wait_for(
                "button_click",
                check = lambda i: i.component.id in ["back", "front"], #You can add more
                timeout = 10.0 #10 seconds of inactivity
            )
            #Getting the right list index
            if interaction.component.id == "back":
                current -= 1
            elif interaction.component.id == "front":
                current += 1
            #If its out of index, go back to start / end
            if current == len(paginationList):
                current = 0
            elif current < 0:
                current = len(paginationList) - 1

            #Edit to new page + the center counter changes
            await interaction.respond(
                type = InteractionType.UpdateMessage,
                embed = paginationList[current],
                components = [ #Use any button style you wish to :)
                    [
                        Button(
                            label = "Prev",
                            id = "back",
                            style = ButtonStyle.red
                        ),
                        Button(
                            label = f"Page {int(paginationList.index(paginationList[current])) + 1}/{len(paginationList)}",
                            id = "cur",
                            style = ButtonStyle.grey,
                            disabled = True
                        ),
                        Button(
                            label = "Next",
                            id = "front",
                            style = ButtonStyle.red
                        )
                    ]
                ]
            )
        except asyncio.TimeoutError:
            #Disable and get outta here
            await mainMessage.edit(
                components = [
                    [
                        Button(
                            label = "Prev",
                            id = "back",
                            style = ButtonStyle.red,
                            disabled = True
                        ),
                        Button(
                            label = f"Page {int(paginationList.index(paginationList[current])) + 1}/{len(paginationList)}",
                            id = "cur",
                            style = ButtonStyle.grey,
                            disabled = True
                        ),
                        Button(
                            label = "Next",
                            id = "front",
                            style = ButtonStyle.red,
                            disabled = True
                        )
                    ]
                ]
            )
            break

@client.command()
async def help(ctx, command = None):

    embed = discord.Embed(
        color = discord.Color.blurple()
    )
    embed.title = "Nekooooooooo's Help Desk"

    if command == 'price':
        embed.description = f"""
        **{prefix}price**
        ```Get the price/s of a coin/crypto```
        """

        embed.add_field(
            name = f"***Examples***",
            value = f"""`{prefix}price slp`
            shows all the supported prices of SLP.
            `{prefix}price eth usd`
            shows the price of ETH in USD.
            `{prefix}price btc all`
            shows all the supported prices of BTC.
            """,
            inline = True
        )

        embed.add_field(
            name = f"***Usages***",
            value = f"`{prefix}price <crypto> [ <currency> | all ]`",
            inline = True
        )

        embed.add_field(
            name = f"***Aliases***",
            value = f"*__p__*",
            inline = False
        )

    elif command == 'convert':
        embed.description = f"""
        **{prefix}convert**
        ```convert the amount of selected crypto to selected currency```
        """

        embed.add_field(
            name = f"***Examples***",
            value = f"""`{prefix}convert 2500 slp php`
            converts 2500 SLP to PHP.
            `{prefix}convert 1 eth usd`
            converts 1 ETH to USD.
            """,
            inline = True
        )

        embed.add_field(
            name = f"***Usages***",
            value = f"`{prefix}convert <amount> <crypto> <currency>`",
            inline = True
        )

        embed.add_field(
            name = f"***Aliases***",
            value = f"*__cv__*",
            inline = False
        )
    elif command == 'help':
        embed.description = f"""
        **{prefix}help**
        ```Shows list of commands```
        """

        embed.add_field(
            name = f"***Examples***",
            value = f"""`{prefix}help`
            shows all commands.
            `{prefix}help price`
            shows how to use the `price` command.
            """,
            inline = True
        )

        embed.add_field(
            name = f"***Usages***",
            value = f"`{prefix}help [command]`",
            inline = True
        )
    elif command == 'info':
        embed.description = f"""
        **{prefix}info**
        ```Shows info about the bot.```
        """

        embed.add_field(
            name = f"***Example***",
            value = f"""`{prefix}info`
            shows info about the bot.
            """,
            inline = True
        )

        embed.add_field(
            name = f"***Usages***",
            value = f"`{prefix}info`",
            inline = True
        )
    elif command == 'todo':
        embed.description = f"""
        **{prefix}todo**
        ```Shows my to-do list of upcoming changes and additions to the bot.```
        """

        embed.add_field(
            name = f"***Example***",
            value = f"""`{prefix}todo`
            Shows bot to-do list.
            """,
            inline = True
        )

        embed.add_field(
            name = f"***Usages***",
            value = f"`{prefix}todo`",
            inline = True
        )
    else:

        cryptoCommands = ''
        infoCommands = ''

        embed.title = "⚙ Standard Commands"

        embed.set_thumbnail(
            url = "https://bolderadvocacy.org/wp-content/uploads/2018/08/blue-icon-question-mark-image.png"
        )

        embed.description = f"Type {prefix}help [command] for more help eg. t!help price"

        for i in cryptoCommandList:
            cryptoCommands += f"`{i}` "

        embed.add_field(
            name = "<:ethereum:875781746287845386> Crypto",
            value = cryptoCommands
        )

        for j in infoCommandList:

            infoCommands += f"`{j}` "

        embed.add_field(
            name = "📝 Info",
            value = infoCommands
        )

    await ctx.send(embed = embed)

@client.event
async def on_command_error(ctx, error):
    embed = discord.Embed(
        color = discord.Color.red()
    )

    embed.set_author(
        name = ctx.author.display_name,
        icon_url = ctx.author.avatar_url
    )
    if isinstance(error, CommandNotFound):
        embed.description = f"❌ Invalid command \n\n**Help**\n`{prefix}help`\nShows list of commands."
        await ctx.send(embed = embed)
        # await ctx.send('Invalid <crypto> <currency> argument given')
        # await ctx.send('Usage: price <crypto> <currency>')
        return
    raise error

cedId = "454964469752266762"

@client.command()
async def raine(ctx):
    await ctx.send(f'<@!{cedId}> pango')

@client.command()
async def pango(ctx):
    await ctx.send(f'ni <@!{cedId}>')

BOT_TOKEN = "token here"
client.run(BOT_TOKEN)
