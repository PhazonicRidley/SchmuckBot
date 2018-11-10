#!/usr/bin/env python3.6

from discord.ext import commands


class Rules:
    """
    Read this bitch
    """

        def __init__(self, bot):
                self.bot = bot
                print("{} addon loaded.".format(self.__class__.__name__))


        @commands.command(aliases=['r01'])
        async def r1(self, ctx):
                """Displays rule 1."""
                await ctx.send("Don't be an asshole to others for no reasons.")


        @commands.command(aliases=['r02'])
        async def r2(self, ctx):
                """Displays rule 2."""
                await ctx.send("No NSFW content unless it's in the NSFW chats.")


        @commands.command(aliases=['r03'])
        async def r3(self, ctx):
                """Displays rule 3."""
                await ctx.send("Don't spam.")


        @commands.command(aliases=['r04'])
        async def r4(self, ctx):
                """Displays rule 4."""
                await ctx.send("No alts unless allowed .")


        @commands.command(aliases=['r05'])
        async def r5(self, ctx):
                """Displays rule 5."""
                await ctx.send("Implied rules are also rules.")
