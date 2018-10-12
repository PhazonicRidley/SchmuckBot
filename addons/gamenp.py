# Credit to Hydraxis#7824 for making this for glados.

from json import load, dump

from discord import Embed, Colour
from discord.ext import commands
from discord.utils import get


class Toggle:

    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def addgamenp(self, ctx, keyword, emoji, role, *, description):
        """
        Add a new non-pingable role to the bot's database, or replace one.
        If you don't need to link the role to a specific emoji,
        replace the "emoji" argument by "none".
        Role name is caps sensitive and must be between quotes.
        """

        try:
            with open("database/rolesnp.json") as f:
                js = load(f)
        except FileNotFoundError:
            js = {}

        if emoji.lower() == "none":
            emoji = ""
        keyword = keyword.lower()

        js[keyword] = {}

        js[keyword]["emoji"] = emoji
        js[keyword]["role"] = role
        js[keyword]["description"] = description

        await ctx.send("Added role `{}` to the database.".format(keyword))

        with open("database/rolesnp.json", "w") as f:
            dump(js, f, sort_keys=True, indent=4, separators=(',', ': '))

    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def delgamenp(self, ctx, keyword):
        """
        Delete a role from the bot's database
        """

        try:
            with open("database/rolesnp.json") as f:
                js = load(f)
        except FileNotFoundError:
            js = {}

        try:
            del js[keyword]
        except KeyError:
            await ctx.send("This role is not in the database!")
            return

        with open("database/rolesnp.json", "w") as f:
            dump(js, f, sort_keys=True, indent=4, separators=(',', ': '))

    @commands.command()
    async def gamenp(self, ctx, keyword=""):
        """
        Toggle some opt-in roles
        """

        user = ctx.message.author
        keyword = keyword.lower()

        try:
            with open("database/rolesnp.json") as f:
                js = load(f)
        except FileNotFoundError:
            js = {}

        try:
            rolename = js[keyword]["role"]
            role = get(ctx.message.guild.roles, name=rolename)
            if role in user.roles:
                await user.remove_roles(role)
                await ctx.send("Left {}".format(rolename))
                return
            await user.add_roles(role)
            await ctx.send("Joined {}".format(rolename))

        except KeyError:
            if keyword == "":
                embed = Embed(title="Game List:",
                              colour=Colour.dark_purple())
                embed.description = ""
                for k in js:
                    embed.description += "- {} {}: `{}`\n".format(
                        js[k]["emoji"],
                        js[k]["description"],
                        k
                    )
                await ctx.send("", embed=embed)
                return

            await ctx.send("This role is not in the database!")


def setup(bot):
    bot.add_cog(Toggle(bot))
