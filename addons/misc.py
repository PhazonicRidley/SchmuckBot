#!/usr/bin/env python3.6

import datetime
import discord
from discord.ext import commands

class Misc:
    """
    Miscellaneous commands
    """

    def __init__(self, bot):
        self.bot = bot
        print("{} addon loaded.".format(self.__class__.__name__))

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """Pong!"""
        mtime = ctx.message.created_at
        currtime = datetime.datetime.now()
        latency = currtime - mtime
        ptime = str(latency.microseconds / 1000.0)
        return await ctx.send(":ping_pong:! Pong! Response time: {} ms".format(ptime))

    @commands.command(pass_context=True, aliases=['mc'])
    async def membercount(self, ctx):
        """Prints current member count"""
        return await ctx.send(str(self.bot.guild.name)+" currently has " + str(len(self.bot.guild.members)) + " members!")

    @commands.command()
    async def about(self, ctx):
        """About SchmuckBot."""
        return await ctx.send("https://github.com/PhazonicRidley/SchmuckBot")

    @commands.command(pass_context=True)
    async def sudo(self, ctx):
        """Gain temp mod powers, only need by Bot Developers to fix the bot/server"""

        user = ctx.message.author
        await ctx.message.delete()

        if self.bot.botdev_role in user.roles:
            await user.add_roles(self.bot.sudo_role)
            await ctx.send(":ambulance: **{} is now a HalfOP! Welcome to the twilight zone!**".format(user))
        else:
           return await ctx.send("You do not have permission to use this command!")

    @commands.command(pass_context=True)
    async def unsudo(self, ctx):
        """Remove temp mod powers, only needed by Bot Developers"""
        user = ctx.message.author
        await ctx.message.delete()

        if self.bot.botdev_role in user.roles:
            if self.bot.sudo_role in user.roles:
                await user.remove_roles(self.bot.sudo_role)
                await ctx.send("**Problem Solved! {} is no longer a HalfOP!**".format(user.name))
            else:
                ctx.send("You are not currently a HalfOP!")

        else:
            return await ctx.send("You do not have permission to use this command!")





    @commands.command(pass_context=True)
    async def togglechannel(self, ctx, channel):
        """Toggle access to some hidden channels"""

        user = ctx.message.author
        await ctx.message.delete()

        if channel == "nsfw":

            if self.bot.nsfw_role in user.roles:
                await user.remove_roles(self.bot.nsfw_role)
                await user.send("Access to NSFW channels revoked.")
            else:
                await user.add_roles(self.bot.nsfw_role)
                await user.send("Access to NSFW channels granted.")
        else:
            await user.send("{} is not a togglable channel.".format(channel))

    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def clear(self, ctx, amount):
        """Clears a given amount of messages. (Mods only)"""

        channel = ctx.message.channel
        try:
            n = int(amount) + 1
        except ValueError:
            return await ctx.send("Please mention a valid amount of messages!")

        try:
            await channel.purge(limit=n)
            await ctx.send("🗑️ Cleared {} messages in this channel!".format(amount))
        except discord.errors.Forbidden:
            await ctx.say("💢 I don't have permission to do this.")


def setup(bot):
    bot.add_cog(Misc(bot))
