# I should get a cookie cause I'm the main person who cooked on this... - 5quirre1
from discord.utils import get
import discord
from discord.ext import commands
from datetime import timedelta
from collections import defaultdict
import time
import random
import requests

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
warnings = defaultdict(int)
timeout_tracker = defaultdict(int)
sob_cooldowns = {}
fire_cooldowns = {}
SPAM_THRESHOLD = 5
SPAM_INTERVAL = 6
TIMEOUT_DURATION = 5 
spam_tracker = defaultdict(list)

PEXELS_API_KEY = "PIX_TOKEN" # again, no showing api grge
PEXELS_URL = "https://api.pexels.com/v1/search"

bot = commands.Bot(command_prefix='!', intents=intents)
trigger_words = ['Retard', 'test2', 'test3']

def start():
    bot.tree.sync()
    print(f"I have logged in as {bot.user}")
    game = discord.Game("Protecting President Squirtward 👅 (FreakyBot 1.2)")
    print("Changed status to: " + str(game))
    bot.change_presence(status=discord.Status.online, activity=game)
    bot.run('TOKEN') #no showing api grge

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return

    designated_channel_id = 1277352185302220921

    if message.channel.id != designated_channel_id:
        user_messages = spam_tracker.setdefault(message.author.id, [])
        current_time = message.created_at.timestamp()

        user_messages.append(current_time)
        spam_tracker[message.author.id] = [
            msg_time for msg_time in user_messages if current_time - msg_time <= SPAM_INTERVAL
        ]

        if len(spam_tracker[message.author.id]) > SPAM_THRESHOLD:
            if message.author.id not in timeout_tracker:
                timeout_tracker[message.author.id] = 1
            else:
                timeout_tracker[message.author.id] += 1

            try:
                await message.channel.purge(
                    limit=SPAM_THRESHOLD + 1,
                    check=lambda msg: msg.author == message.author
                )
            except discord.errors.Forbidden:
                pass

            spam_tracker[message.author.id].clear()

            if timeout_tracker[message.author.id] < 2:
                await message.channel.send(
                    f"{message.author.mention}, make sure to not spam in any other channel except for [Spam Channel](https://discord.com/channels/1277349483633705042/1277352185302220921) plzz ^^"
                )
            elif timeout_tracker[message.author.id] == 2:
                try:
                    await message.author.timeout(timedelta(minutes=TIMEOUT_DURATION), reason="Repeated spamming")
                    await message.channel.send(
                        f"{message.author.mention} has been timed out for {TIMEOUT_DURATION} minutes due to repeated spamming."
                    )
                except discord.errors.Forbidden:
                    await message.channel.send(
                        f"Could not timeout {message.author.mention}, but please stop spamming."
                    )

    responses = {
        'piplup': 'nerd',
        'are you freaky': 'yes 👅',
        'greg': '[Greg](https://www.greg.com/images/resized_and_crop/250/200/eyJpZCI6IjgzYWU3NjQ2YjljYWZkYjBiYjAzY2MwY2U2Y2E3NmVmIiwic3RvcmFnZSI6InN0b3JlIn0?signature=87f4495c39748e4459b4f3ad69f5843a9acc005e7b3baa33ccad7d6e47f198dd) Heffley is peak!\nntyler the creator',
        'chair': '[chair](https://theamishhouse.com/cdn/shop/products/theodore-side-chair-260327_847ac408-9f9f-4ba3-8dbc-10a9fc08257d.jpg?crop=center&height=1200&v=1611462911&width=1200)',
        'car': '[car](https://media.discordapp.net/attachments/1296598626537312300/1316646229513338931/IMG_1305.jpg?ex=675bcddb&is=675a7c5b&hm=0c497865de724aea018e846b8e5da0376b30782977bdb11f8e6c5ea7f4ee323c&=&format=webp&width=375&height=375)',
        'Car': '[car](https://media.discordapp.net/attachments/1296598626537312300/1316646229513338931/IMG_1305.jpg?ex=675bcddb&is=675a7c5b&hm=0c497865de724aea018e846b8e5da0376b30782977bdb11f8e6c5ea7f4ee323c&=&format=webp&width=375&height=375)',
        'Greg': '[Greg](https://www.greg.com/images/resized_and_crop/250/200/eyJpZCI6IjgzYWU3NjQ2YjljYWZkYjBiYjAzY2MwY2U2Y2E3NmVmIiwic3RvcmFnZSI6InN0b3JlIn0?signature=87f4495c39748e4459b4f3ad69f5843a9acc005e7b3baa33ccad7d6e47f198dd) Heffley is peak!\nntyler the creator',
        'Chair': '[chair](https://theamishhouse.com/cdn/shop/products/theodore-side-chair-260327_847ac408-9f9f-4ba3-8dbc-10a9fc08257d.jpg?crop=center&height=1200&v=1611462911&width=1200)',
        'Are you freaky': 'yes 👅',
        'Piplup': 'nerd',
        'freakybob': 'peak https://freakybob.site',
        'gay': 'https://cdn.discordapp.com/attachments/1296598626537312300/1316874630576738324/ec60a7a5-ca73-4194-8b2b-f2647cf394b4.jpg?ex=675ca292&is=675b5112&hm=a2653313a02d101273c5d3e2dbd20ab43dd9f7828616ed4b83f61e27ec6a0ecf&',
        'ay': 'lmao' + message.content,
        'balls': 'https://cdn.discordapp.com/attachments/1277349485155975261/1316929388436263042/RDT_20241210_1537575581555789560519844.jpg?ex=675cd591&is=675b8411&hm=ecf5388ec71c084159e128544025cffdd99328541bcb4f4b013737f68bcae8eb&',
    }

    if message.content in responses and message.channel.id != designated_channel_id:
        await message.channel.send(responses[message.content])

    await bot.process_commands(message)
# Mod commands :3
@bot.command(name='ban', help='MOD ONLY: Ban a member from the server', category='mod')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    try:
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} has been banned! Reason: {reason or "No reason provided."}')
        try:
            await member.send(f'You have been banned from {ctx.guild.name}. Reason: {reason or "No reason provided."}')
        except discord.Forbidden:
            await ctx.send(f'Could not DM {member.mention} about their ban')
    except Exception as e:
        await ctx.send(f'Failed to ban {member.mention}: {e}')


@bot.command(name='kick', help='MOD ONLY: Kick a member from the server', category='mod')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    try:
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} has been kicked! Reason: {reason or "No reason provided."}')
        try:
            await member.send(f'You have been kicked from {ctx.guild.name}. Reason: {reason or "No reason provided."}')
        except discord.Forbidden:
            await ctx.send(f'Could not DM {member.mention} about their kick :sob:')
    except Exception as e:
        await ctx.send(f'Failed to kick {member.mention}: {e}')
@bot.command(name='timeout', help='MOD ONLY: Timeout a member for a specified duration', category='mod')
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, duration: int, *, reason=None):
    try:
        await member.timeout(timedelta(minutes=duration), reason=reason)
        await ctx.send(f'They have been timed out for {duration} minutes. Reason: {reason or "No reason provided."}')
        try:
            await member.send(f'You have been timed out in {ctx.guild.name} for {duration} minutes. Reason: {reason or "No reason provided."}')
        except discord.Forbidden:
            await ctx.send(f'Could not DM {member.mention} about their timeout.')

    except Exception as e:
        await ctx.send(f'Failed to timeout {member.mention}: {e}')

@bot.command(name='untimeout', help='MOD ONLY: Remove timeout from a member', category='mod')
@commands.has_permissions(moderate_members=True)
async def untimeout(ctx, member: discord.Member, *, reason=None):
    try:
        await member.timeout(None, reason=reason)
        await ctx.send(f'{member.mention} is no longer in timeout.')
    except Exception as e:
        await ctx.send(f'Failed to remove timeout for {member.mention}: {e}')

@bot.command(name='warn', help='MOD ONLY: Warn a member for a specified reason', category='mod')
@commands.has_permissions(moderate_members=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    warnings[member.id] += 1
    warn_count = warnings[member.id]
    await ctx.send(f'{member.mention} has been warned for: \'{reason}\'. This is warning #{warn_count}.')
    try:
        await member.send(f'You have been warned in {ctx.guild.name} for: \'{reason}\'. You now have {warn_count} warnings.')
    except discord.Forbidden:
        await ctx.send(f'Could not DM {member.mention} about their warning.')

@bot.command(name='unwarn', help='MOD ONLY: Remove a warning from a member', category='mod')
@commands.has_permissions(moderate_members=True)
async def unwarn(ctx, member: discord.Member):
    if warnings[member.id] > 0:
        warnings[member.id] -= 1
        await ctx.send(f'One warning has been removed from {member.mention}. They now have {warnings[member.id]} warnings.')
        try:
            await member.send(f'One of your warnings has been removed in {ctx.guild.name}. You now have {warnings[member.id]} warnings.')
        except discord.Forbidden:
            await ctx.send(f'Could not DM {member.mention} about their unwarning.')
    else:
        await ctx.send(f'{member.mention} has no warnings to remove.')
@bot.command(name='clear', help='MOD ONLY: Clear a specified number of messages', category='mod')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'{amount} messages have been cleared!')

@bot.command(name='warning_clear', help='MOD ONLY: Clear all warnings from a member', category='mod')
@commands.has_permissions(moderate_members=True)
async def warning_clear(ctx, member: discord.Member):
    warnings[member.id] = 0
    await ctx.send(f'All warnings have been cleared for {member.mention}.')
    try:
        await member.send(f'All warnings have been cleared in {ctx.guild.name}.')
    except discord.Forbidden:
        await ctx.send(f'Could not DM {member.mention} about their warning clear.')


#useful stuff I think
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1298869716261146664)
    if channel:
        await channel.send(f"Welcome, {member.mention} to Freakcord! I hope you enjoy your stay!")
@bot.command(name='info', help='Get information about a member')
async def info(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author


    member = await ctx.guild.fetch_member(member.id)

    roles = [role.name for role in member.roles if role.name != "@everyone"]
    roles = ", ".join(roles) if roles else "No roles assigned"

    embed = discord.Embed(title=f"Information about {member.display_name}", color=discord.Color.blue())
    embed.set_thumbnail(url=member.display_avatar.url)

    embed.add_field(name="Username", value=member.name, inline=True)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime('%b %d, %Y'), inline=False)
    embed.add_field(name="Roles", value=roles, inline=False)
    embed.add_field(name="Account Created", value=member.created_at.strftime('%b %d, %Y'), inline=False)

    await ctx.send(embed=embed)

    await ctx.send("⚠️ **Warning:** Please refrain from using this command inappropriately, such as spam pinging. Just plz be good ^^")

@bot.command(name="socials", help="Social networks Freakybob Team is on")
async def the_socials(ctx):
    await ctx.send("PikiDiary: https://pikidiary.lol/@freakybob" + "\nBluesky: https://bsky.app/profile/freakybob.site")


@bot.command(name='warns', help='Check how many warnings a member has')
async def warns(ctx, member: discord.Member):
    warn_count = warnings[member.id]
    await ctx.send(f'{member.mention} has {warn_count} warnings.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    for word in trigger_words:
        if word in message.content.lower():
            warnings[message.author] += 1
            await message.delete()
            if warnings[message.author] == 3:
                TIMEOUT_DURATION = 9
                try:
                    await message.author.timeout(timedelta(minutes=TIMEOUT_DURATION), reason="Repeated spamming of a blocked word")
                    await message.channel.send(f"{message.author.mention} has been timed out for using the blocked words too many times, what a loser.")
                except discord.errors.Forbidden:
                    await message.channel.send(f"I can't timeout {message.author.mention} because they have higher permissions than me... You're supposed to be better than this.")
                    admin = await bot.fetch_user(1127731486485921813)
                    await admin.send(f"One of the devs, mods, or admins broke the rules by saying a blocked word 3 times, triggering the dm: {message.author.mention}")
                except Exception as e:
                    await message.channel.send(f"An error occurred while trying to timeout {message.author.mention}...: {e}")
            else:
                await message.channel.send(f"{message.author.mention}, do not say that plz. Warning {warnings[message.author]}/3. At 3 warnings, you will be timed out for 9 minute ^^")
            return

    await bot.process_commands(message)

@bot.command(name='slowmode', help='Set slowmode for the channel.')
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Slowmode has been set to {seconds} seconds.")

@bot.command(name='announce', help='MOD ONLY: Send an announcement to a channel!')
@commands.has_permissions(administrator=True)
async def announce(ctx, channel_id: int, *, message: str):
    channel = bot.get_channel(channel_id)
    if channel:
        embed = discord.Embed(
            title="**Announcement**",
            description=message,
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Announced by {ctx.author}")
        await channel.send(embed=embed)
        await ctx.send(f"Announcement sent to {channel.name}!")
    else:
        await ctx.send("Channel not found.")

#fun ones
@bot.command(name='peak', help='Now this is fire :fire:')
async def fire(ctx):
    await ctx.send('[Fire](https://media.discordapp.net/attachments/1270914607661322261/1316649597984051201/caption.gif)')

@bot.command(name='not_fire', help='this is not fire')
async def not_fire(ctx):
    await ctx.send('[Not Fire](https://media.discordapp.net/attachments/1251937089440845844/1288338569014018109/caption.gif?ex=675ba74b&is=675a55cb&hm=e158804de82881c469ecb515c0a1fe0aaace069e71d57a2a016e083c5e359d15&=&width=622&height=548)')
@bot.command(name='sfx', help='stupid cube')
async def sfx(ctx):
    await ctx.send('[dummy](https://cdn.discordapp.com/attachments/1290356175287881905/1302061996002246696/attachment.gif?ex=675cccba&is=675b7b3a&hm=318009a5179fd00a398323099e88d41bdfd068004eb94c60f691150223638293&)')
@bot.command(name="hello", help="Says hello")
async def hello(ctx):
    await ctx.send('Hello, {0.author.mention}!!'.format(ctx))
    
@bot.command(name="hello_everyone", help="Says hello to everyone")
async def hello_everyone(ctx):
    await ctx.send('Hello everyone!!! I\'m FreakyBot! I\'m Freakcord\'s **new** moderation bot!!!')
    
@bot.command(name="about", help="about freakybot")
async def about(ctx):
    await ctx.send("FreakyBot is Freakcord's **new** moderation bot.")
    time.sleep(1)
    await ctx.send('FreakyBot was originally made in C++ but the bot now uses Python and <https://railway.app> to deploy.')
    time.sleep(1)
    await ctx.send('FreakyBot was made by: 5quirre1, Wish13yt, and Nomaakip! (GitHub usernames)')
    time.sleep(1)
    await ctx.send('5quirre1 was the one that cooked tho, not self glazing trust >:3')

@bot.command(name='kill', help='sends luigi to someone\'ns house', category='fun')
async def kill(ctx, member: discord.Member):
    await ctx.send(f'sending luigi to {member.mention}\'s house...')


@bot.command(name='sob', help='reacts with a sob emoji', category='fun')
async def sob(ctx):
    user_id = ctx.author.id
    current_time = time.time()
    
    if user_id in sob_cooldowns:
        cooldown_time = sob_cooldowns[user_id]
        if current_time - cooldown_time < 8:
            if sob_cooldowns[user_id] + 8 < current_time:
                sob_cooldowns[user_id] = current_time
            else:
                await ctx.send("This command is on cooldown! Please try again in like 8 seconds :3")
                return
    
    sob_cooldowns[user_id] = current_time
    await ctx.message.add_reaction('😭')

@bot.command(name='fire', help='reacts with a fire emoji', category='fun')
async def fire(ctx):
    user_id = ctx.author.id
    current_time = time.time()
    
    if user_id in fire_cooldowns:
        cooldown_time = fire_cooldowns[user_id]
        if current_time - cooldown_time < 8:
            if fire_cooldowns[user_id] + 8 < current_time:
                fire_cooldowns[user_id] = current_time
            else:
                await ctx.send("This command is on cooldown! Please try again in like 8 seconds :3")
                return
    
    fire_cooldowns[user_id] = current_time
    await ctx.message.add_reaction('🔥')


@bot.command(name='8ball', help='Ask the magic 8 ball a question and get an answer!')
async def eight_ball(ctx, *, question: str):
    responses = [
        "Yes.",
        "No.",
        "Maybe.",
        "Definitely not.",
        "Absolutely!",
        "I don't know, try again later.",
        "Ask again in a bit.",
        "I have no clue.",
        "Most likely.",
        "Very doubtful.",
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Outlook not so good.",
        "Very doubtful.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful.",
        "I'm gay",
        "You're gay"
    ]
    
    answer = random.choice(responses)
    await ctx.send(f'🎱 {answer}')
    
@bot.command(name='flipcoin', help='Flip a coin.')
async def flipcoin(ctx):
    result = random.choice(['Heads', 'Tails'])
    await ctx.send(f'🪙 {result}')
@bot.command(name='fortune', help='Receive a random fortune from a fortune cookie.')
async def fortune(ctx):
    fortunes = [
        "You will find great success in your future!",
        "A friend is someone who knows all about you and still loves you :33",
        "Your talents will be recognized and suitably rewarded!",
        "A fresh start will put you on your way",
        "A new adventure awaits you.",
        "Freakybob will give you a hug."
    ]
    await ctx.send(random.choice(fortunes))
@bot.command(name='joke', help='Get a random joke.')
async def joke(ctx):
    response = requests.get('https://v2.jokeapi.dev/joke/Any?type=single')
    
    if response.status_code == 200:
        data = response.json()
        joke_text = data['joke']
        await ctx.send(joke_text)
    else:
        await ctx.send("Sorry, I couldn't fetch a joke at the moment :sob:")

empty_board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

def display_board(board, current_player):
    return f"""
    {board[0]} | {board[1]} | {board[2]}
    ----------- 
    {board[3]} | {board[4]} | {board[5]}
    ----------- 
    {board[6]} | {board[7]} | {board[8]}
    
    It's {current_player}'s turn!
    """

def check_win(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

def is_board_full(board):
    return all(cell in ['X', 'O'] for cell in board)

@bot.command(name="tictactoe", help="Start a Tic-Tac-Toe game.")
async def tictactoe(ctx):
    board = empty_board.copy()
    current_player = "X"
    embed = discord.Embed(title="Tic-Tac-Toe", description=display_board(board, current_player), color=discord.Color.blue())
    message = await ctx.send(embed=embed)
    emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

    for emoji in emojis:
        await message.add_reaction(emoji)

    def check(reaction, user):
        return user != bot.user and str(reaction.emoji) in emojis

    while True:
        reaction, user = await bot.wait_for("reaction_add", check=check)
        index = emojis.index(str(reaction.emoji))

        if board[index] in ['X', 'O']:
            continue

        board[index] = current_player
        embed = discord.Embed(title="Tic-Tac-Toe", description=display_board(board, current_player), color=discord.Color.blue())
        await message.edit(embed=embed)

        if check_win(board, current_player):
            await ctx.send(f"Player {current_player} wins!")
            break
        elif is_board_full(board):
            await ctx.send("It's a draw!")
            break

        current_player = 'O' if current_player == 'X' else 'X'

        await message.remove_reaction(reaction.emoji, user)

def get_squirrel_image():
    headers = {
        "Authorization": PEXELS_API_KEY
    }
    params = {
        "query": "squirrel",
        "per_page": 10,
        "orientation": "landscape"
    }
    response = requests.get(PEXELS_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data["photos"]:
            random_image = random.choice(data["photos"])
            return random_image["src"]["original"]
        else:
            return None
    else:
        return None

@bot.command(name="squirrel", help="get a random picture of a squirrel, idk")
async def squirrel(ctx):
    image_url = get_squirrel_image()
    
    if image_url:
        embed = discord.Embed(title="Squirrel be like")
        embed.set_image(url=image_url)
        embed.color = discord.Color.pink()
        await ctx.send(embed=embed)
    else:
        await ctx.send("There were no squirrel images found... :(")

# Idk why I'm like sorting these out but error handling ig :sob:
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Command not found! Error: ' + str(error))
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please provide all required arguments! Error: ' + str(error))
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have the required permissions to use this command! Error: ' + str(error))
    else:
        await ctx.send(f'An error occurred: ' + str(error))
        raise error

        


start()
