from header_files import *

@brewmeister.event
async def on_ready():
    for guild in brewmeister.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{brewmeister.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@brewmeister.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the Discord Server!'
    )


@brewmeister.command(
	help="Pass the user id into the command and it will ping that user in the server",
	brief="Pings the user id passed"
)
async def ping(ctx, user_id):
    await ctx.send("<@" + user_id + ">")

@brewmeister.command(
	help="Uses some crazy logic to determine who I am.",
	brief="Returns back who I am."
)
async def info(ctx):
	await ctx.channel.send("Hello, my name is Brewmeister and I was developed by Shashanka to help automate away responsibilities humans face on a daily basis.")

@brewmeister.command(
    help='!crypto BTC ---> returns BTC information',
    brief='Returns back a JSON formatted data of the latest trade metrics of the specified crypto ticker'
)
async def crypto(ctx, arg):
    SYMBOL = arg
    url = f'{COIN_URL}/v2/cryptocurrency/quotes/latest?symbol={SYMBOL}'
    parameters = {
    }

    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': COIN_API,
    }
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        apiResponse = json.loads(response.text)

        price = apiResponse['data'][SYMBOL][0]['quote']['USD']['price']

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    await ctx.channel.send(f'This is the current price of {SYMBOL}: ${str(round(float(price), 2))}')

@brewmeister.command(
    help='',
    brief=''
)
async def tilted(ctx):
    await ctx.channel.send("Shashanka is tilted right now, do not disturb. :(")

@brewmeister.event
async def on_message(message):
	if message.content == "hello":
		await message.channel.send("pies are better than cakes. change my mind.")

	await brewmeister.process_commands(message)


brewmeister.run(TOKEN)