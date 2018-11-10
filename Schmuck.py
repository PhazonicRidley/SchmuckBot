from asyncio import sleep
from traceback import format_exception
from json import load, dump
from subprocess import run
from os import chdir, makedirs
from os.path import isfile, dirname, realpath
from sys import executable, exit as sysexit

from discord import errors, Embed, Color
from discord.utils import get
from discord.ext import commands

from addons.utils import checks

# Change to script's directory
path = dirname(realpath(__file__))
chdir(path)

# Create database
makedirs("database", exist_ok=True)

if not isfile("database/config.json"):
    with open("database/config.json", "w") as f:
        dump({'prefix': [".", "sudo "], 'token': ''}, f,
             sort_keys=True, indent=4, separators=(',', ': '))

config = load(open("database/config.json", "r"))

bot = commands.Bot(command_prefix=config['prefix'], description="GLaDOS, a general purpose discord bot.",
                   max_messages=10000, pm_help=True)


@bot.event
async def on_ready():

    for guild in bot.guilds:
        bot.guild = guild

        # Moderation Roles
        bot.owner_role = get(guild.roles, name="BlackGuy")
        bot.admin_role = get(guild.roles, name="Minions")
        bot.mod_role = get(guild.roles, name="Mods")
        bot.staff_role = get(guild.roles, name="staff")
        bot.botdev_role = get(guild.roles, name="SchmuckBotAllow")
        bot.nsfw_role = get(guild.roles, name="mcspankies")
        bot.muted_role = get(guild.roles, name="Muted")

        # Misc Roles
        bot.sudo_role = get(guild.roles, name="sudo")

        # Channels
        bot.announcements_channel = get(guild.channels, name="announcements")
        bot.botdev_channel = get(guild.channels, name="botwork")
        bot.botdms_channel = get(guild.channels, name="bot-dm")
        bot.logs_channel = get(guild.channels, name="server-log")
        bot.memberlogs_channel = get(guild.channels, name="join-leave-log")

    # Load addons
    addons = [
        'emojif',
        'events',
        'game',
        'memes',
        'speak',
        'warn',
        'misc',
        'mod',
        'rules',
    ]

    # Notify if an addon fails to load.
    fail = 0
    for addon in addons:
        try:
            bot.load_extension("addons." + addon)
            print("{} addon loaded.".format(addon))
        except Exception as e:
            if not fail:
                emb = Embed(
                    title="Startup", description="Failed to load Addons", colour=Color.blue())
            fail += 1
            emb.add_field(name=addon, value="{} : {}".format(
                type(e).__name__, e), inline=True)
            print("Failed to load {} :\n{} : {}".format(
                addon, type(e).__name__, e))
    if fail:
        try:
            logchannel = bot.logs_channel
            await logchannel.send("", embed=emb)
        except errors.Forbidden:
            pass

    bot.all_ready = True

    print("Client logged in as {}, in the following guild : {}"
          "".format(bot.user.name, bot.guild.name))



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, (commands.errors.CommandNotFound, commands.errors.CheckFailure)):
        return
    elif isinstance(error, (commands.MissingRequiredArgument, commands.BadArgument)):
        helpm = await bot.formatter.format_help_for(ctx, ctx.command)
        for m in helpm:
            await ctx.send(m)
    elif isinstance(error, commands.errors.CommandOnCooldown):
        try:
            await ctx.message.delete()
        except errors.NotFound:
            pass
        message = await ctx.message.channel.send("{} This command was used {:.2f}s ago and is on "
                                                 "cooldown. Try again in {:.2f}s."
                                                 "".format(ctx.message.author.mention,
                                                           error.cooldown.per - error.retry_after,
                                                           error.retry_after))
        await sleep(10)
        await message.delete()
    else:
        await ctx.send("An error occured while processing the `{}` command."
                       "".format(ctx.command.name))
        print(
            'Ignoring exception in command {0.command} in {0.message.channel}'.format(ctx))
        botdev_msg = "Exception occured in `{0.command}` in {0.message.channel.mention}".format(
            ctx)
        tb = format_exception(type(error), error, error.__traceback__)
        print(''.join(tb))
        botdev_channel = bot.botdev_channel
        await botdev_channel.send(botdev_msg + '\n```' + ''.join(tb) + '\n```')

# Core commands


@bot.command()
@checks.is_botdev()
async def unload(ctx, addon: str):
    """Unloads an addon."""
    try:
        addon = "addons." + addon
        bot.unload_extension(addon)
        await ctx.send('✅ Addon unloaded.')
    except Exception as e:
        await ctx.send('💢 Error trying to unload the addon:\n```\n{}: {}\n```'
                       ''.format(type(e).__name__, e))


@bot.command(name='reload', aliases=['load'])
@checks.is_botdev()
async def reload(ctx, addon: str):
    """(Re)loads an addon."""
    try:
        addon = "addons." + addon
        bot.unload_extension(addon)
        bot.load_extension(addon)
        await ctx.send('✅ Addon reloaded.')
    except Exception as e:
        await ctx.send('💢 Failed!\n```\n{}: {}\n```'.format(type(e).__name__, e))

        # Will add back later


@bot.command(name="pull", aliases=["pacman"])
@checks.is_botdev()
async def pull(ctx, pip=None):
    """Pull new changes from Git and restart.
    Append -p or --pip to this command to also update python modules from requirements.txt."""

    await ctx.send("`Pulling changes...`")
    run(["git", "stash", "save"])
    run(["git", "pull"])
    run(["git", "stash", "clear"])
    pip_text = ""
    if pip in ("-p", "--pip", "-Syu"):
        await ctx.send("`Updating python dependencies...`")
        run([executable, "-m", "pip", "install", "--user",
             "--upgrade", "-r", "requirements.txt"])
        pip_text = " and updated python dependencies"
    await ctx.send("Pulled changes{}! Restarting...".format(pip_text))
    run([executable, "Schmuck.py"])


@commands.has_permissions(administrator=True)
@bot.command()
async def restart(ctx):
    """Restart the bot (Staff Only)"""
    await ctx.send("`Restarting, please wait...`")
    run([executable, "Schmuck.py"])
    sysexit()


@commands.has_permissions(administrator=True)
@bot.command()
async def stop(ctx):
    """Stop the bot (Staff Only)"""
    await ctx.send("`Exiting...`")
    await bot.logout()
    sysexit()

# Run the bot
if __name__ == "__main__":
    bot.run(config['token'])
