#!/usr/bin/env python3.6

from discord.ext import commands


class Rules:
    """
    vs code is ungood
    """
    def __init__(self, bot):
        self.bot = bot
        print("{} addon loaded.".format(self.__class__.__name__))

        @commands.command()
        async def r1(self, ctx):
            """Shows Rule 1"""
            emb = discord.Embed(title="Rule 1", description="Don't be an asshole to others for no reason.", colour=discord.Colour.purple())
            await ctx.send("", embed=emb)

        @commands.command()
        async def r2(self, ctx):
            """Shows Rule 2"""
            emb = discord.Embed(title="Rule 2", description="No NSFW content unless in NSFW.", colour=discord.Colour.purple())
            await ctx.send("", embed=emb)

        @commands.command()
        async def r3(self, ctx):
            """Shows Rule 3"""
            emb = discord.Embed(title="Rule 3", description="Don't Spam", colour=discord.Colour.purple())
            await ctx.send("", embed=emb)

        @commands.command()
        async def r4(self, ctx):
            """Shows Rule 4"""
            emb = discord.Embed(title="Rule 4", description="No alts with out staff approval", colour=discord.Colour.purple())
            await ctx.send("", embed=emb)

        @commands.command()
        async def r5(self, ctx):
            """Shows Rule 5"""
            emb = discord.Embed(title="Rule 5", description=" Implied rules are also rules.", colour=discord.Colour.purple())
            await ctx.send("", embed=emb)


def setup(bot):
    bot.add_cog(Rules(bot))
