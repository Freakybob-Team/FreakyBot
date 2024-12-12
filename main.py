# I should get a cookie cause I'm the main person who cooked on this... - 5quirre1
from discord.utils import get
import discord
from discord.ext import commands
from datetime import timedelta
from collections import defaultdict
import time


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
warnings = defaultdict(int)
SPAM_THRESHOLD = 5
SPAM_INTERVAL = 6
spam_tracker = defaultdict(list)
lmao = 'lmao'

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():

    await bot.tree.sync()
    print(f"I have logged in as {bot.user}")
    game = discord.Game("Protecting President Squirtward 👅 (FreakyBot 1.2)")
    print("Changed status to: " + str(game))
    await bot.change_presence(status=discord.Status.online, activity=game)


@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return None

    designated_channel_id = 1311447896805347348

    if message.channel.id != designated_channel_id:
        user_messages = spam_tracker[message.author.id]
        current_time = message.created_at.timestamp()

        user_messages.append(current_time)
        spam_tracker[message.author.id] = [
            msg_time for msg_time in user_messages if current_time - msg_time <= SPAM_INTERVAL
        ]

        if len(spam_tracker[message.author.id]) > SPAM_THRESHOLD:
            try:
                await message.channel.purge(
                    limit=SPAM_THRESHOLD + 1,
                    check=lambda msg: msg.author == message.author
                )
            except discord.errors.Forbidden:
                pass

            spam_tracker[message.author.id].clear()


    responses = {
        'piplup': 'nerd',
        'are you freaky': 'yes 👅',
        'greg' : '[Greg](https://www.greg.com/images/resized_and_crop/250/200/eyJpZCI6IjgzYWU3NjQ2YjljYWZkYjBiYjAzY2MwY2U2Y2E3NmVmIiwic3RvcmFnZSI6InN0b3JlIn0?signature=87f4495c39748e4459b4f3ad69f5843a9acc005e7b3baa33ccad7d6e47f198dd) Heffley is peak!\nntyler the creator ',
        'chair': '[chair](https://theamishhouse.com/cdn/shop/products/theodore-side-chair-260327_847ac408-9f9f-4ba3-8dbc-10a9fc08257d.jpg?crop=center&height=1200&v=1611462911&width=1200)',
        'car': '[car](https://media.discordapp.net/attachments/1296598626537312300/1316646229513338931/IMG_1305.jpg?ex=675bcddb&is=675a7c5b&hm=0c497865de724aea018e846b8e5da0376b30782977bdb11f8e6c5ea7f4ee323c&=&format=webp&width=375&height=375)',
        'Car': '[car](https://media.discordapp.net/attachments/1296598626537312300/1316646229513338931/IMG_1305.jpg?ex=675bcddb&is=675a7c5b&hm=0c497865de724aea018e846b8e5da0376b30782977bdb11f8e6c5ea7f4ee323c&=&format=webp&width=375&height=375)',
        'Greg': ('[Greg](https://www.greg.com/images/resized_and_crop/250/200/eyJpZCI6IjgzYWU3NjQ2YjljYWZkYjBiYjAzY2MwY2U2Y2E3NmVmIiwic3RvcmFnZSI6InN0b3JlIn0?signature=87f4495c39748e4459b4f3ad69f5843a9acc005e7b3baa33ccad7d6e47f198dd) Heffley is peak!\nntyler the creator '),
        'Chair': '[chair](https://theamishhouse.com/cdn/shop/products/theodore-side-chair-260327_847ac408-9f9f-4ba3-8dbc-10a9fc08257d.jpg?crop=center&height=1200&v=1611462911&width=1200)',
        'Are you freaky': 'yes 👅',
        'Piplup': 'nerd',
        'freakybob': 'peak https://freakybob.site',
        'gay': 'https://cdn.discordapp.com/attachments/1296598626537312300/1316874630576738324/ec60a7a5-ca73-4194-8b2b-f2647cf394b4.jpg?ex=675ca292&is=675b5112&hm=a2653313a02d101273c5d3e2dbd20ab43dd9f7828616ed4b83f61e27ec6a0ecf&'
    }

    if message.content in responses:
        await message.channel.send(responses[message.content])

    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1298869716261146664)
    if channel:
        await channel.send(f"Welcome, {member.mention} to Freakcord! I hope you enjoy your stay!")
        
@bot.command(name='fire', help='Now this is fire :fire:')
async def fire(ctx):
    await ctx.send('[Fire](https://media.discordapp.net/attachments/1270914607661322261/1316649597984051201/caption.gif)')
@bot.command(name='ban', help='Ban a member from the server')
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


@bot.command(name='kick', help='Kick a member from the server')
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



@bot.command(name='info', help='Get information about a member')
async def info(ctx, member: discord.Member):
    member = await ctx.guild.fetch_member(member.id)
    await ctx.send(f'{member.mention} is a member of {ctx.guild.name} since {member.joined_at}.')
    await ctx.send("Warning: If you use this for being a creep, you will be warned.")

@bot.command(name='timeout', help='Timeout a member for a specified duration')
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, duration: int, *, reason=None):
    try:
        await member.timeout(timedelta(minutes=duration), reason=reason)
        await ctx.send(f'{member.mention} has been timed out for {duration} minutes. Reason: {reason or "No reason provided."}')
        try:
            await member.send(f'You have been timed out in {ctx.guild.name} for {duration} minutes. Reason: {reason or "No reason provided."}')
        except discord.Forbidden:
            await ctx.send(f'Could not DM {member.mention} about their timeout.')

    except Exception as e:
        await ctx.send(f'Failed to timeout {member.mention}: {e}')

@bot.command(name='untimeout', help='Remove timeout from a member')
@commands.has_permissions(moderate_members=True)
async def untimeout(ctx, member: discord.Member, *, reason=None):
    try:
        await member.timeout(None, reason=reason)
        await ctx.send(f'{member.mention} is no longer in timeout.')
    except Exception as e:
        await ctx.send(f'Failed to remove timeout for {member.mention}: {e}')

@bot.command(name='warn', help='Warn a member for a specified reason')
@commands.has_permissions(moderate_members=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    warnings[member.id] += 1
    warn_count = warnings[member.id]
    await ctx.send(f'{member.mention} has been warned for: \'{reason}\'. This is warning #{warn_count}.')
    try:
        await member.send(f'You have been warned in {ctx.guild.name} for: \'{reason}\'. You now have {warn_count} warnings.')
    except discord.Forbidden:
        await ctx.send(f'Could not DM {member.mention} about their warning.')

@bot.command(name='unwarn', help='Remove a warning from a member')
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
@bot.command(name='clear', help='Clear a specified number of messages')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'{amount} messages have been cleared!')

@bot.command(name='warning_clear', help='Clear all warnings from a member')
@commands.has_permissions(moderate_members=True)
async def warning_clear(ctx, member: discord.Member):
    warnings[member.id] = 0
    await ctx.send(f'All warnings have been cleared for {member.mention}.')
    try:
        await member.send(f'All warnings have been cleared in {ctx.guild.name}.')
    except discord.Forbidden:
        await ctx.send(f'Could not DM {member.mention} about their warning clear.')

@bot.command(name='warns', help='Check how many warnings a member has')
async def warns(ctx, member: discord.Member):
    warn_count = warnings[member.id]
    await ctx.send(f'{member.mention} has {warn_count} warnings.')
@bot.command(name='not_fire', help='this is not fire')
async def not_fire(ctx):
    await ctx.send('[Not Fire](https://media.discordapp.net/attachments/1251937089440845844/1288338569014018109/caption.gif?ex=675ba74b&is=675a55cb&hm=e158804de82881c469ecb515c0a1fe0aaace069e71d57a2a016e083c5e359d15&=&width=622&height=548)')
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


@bot.command(name="socials", help="Social networks Freakybob Team is on")
async def the_socials(ctx):
    await ctx.send("PikiDiary: https://pikidiary.lol/@freakybob" + "\n Bluesky: https://bsky.app/profile/freakybob.site")

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

bot.run('THE_TOKEN') # the token is not here cause safety 