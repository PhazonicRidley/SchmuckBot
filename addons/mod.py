#!/usr/bin/env python3

import discord
from discord.ext import commands

class Moderation(commands.Cog):
    """
    Moderation commands
    """

    def __init__(self, bot):
        self.bot = bot
        print("{} addon loaded.".format(self.__class__.__name__))

    async def dm(self, member, message):
        """DM the user and catch an eventual exception."""
        try:
            await member.send(message)
        except:
            pass

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def kick(self, ctx, member, *, reason=""):
        """Kick a member. (Staff Only)"""
        try:
            try:
                member = ctx.message.mentions[0]
            except IndexError:
                await ctx.send("Please mention a user.")
                return
            if reason == "":
                dm_msg="You have been kicked from {}.".format(ctx.guild.name)
            else:
                dm_msg = "You have been kicked from {} for the following reason:\n{}".format(ctx.guild.name, reason)
            await self.dm(member, dm_msg)
            await member.kick()
            await ctx.send("I've kicked {}.".format(member))
            emb = discord.Embed(title="Member Kicked", colour=discord.Colour.red())
            emb.add_field(name="Member:", value=member, inline=True)
            emb.add_field(name="Mod:", value=ctx.message.author, inline=True)
            if reason == "":
                reason = "No reason specified."
            emb.add_field(name="Reason:", value=reason, inline=True)
            logchannel = self.bot.logs_channel
            await logchannel.send("", embed=emb)
        except discord.errors.Forbidden:
            await ctx.send("💢 I dont have permission to do this.")

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def multikick(self, ctx, *, members):
        """Kick multiple members. (Staff Only)"""
        try:
            member = ctx.message.mentions[0]
        except IndexError:
            await ctx.send("Please mention at least one user.")
            return
        for member in ctx.message.mentions:
            try:
                await member.kick()
                await ctx.send("Kicked {}.".format(member))
            except discord.errors.Forbidden:
                await ctx.send("💢 Couldn't kick {}".format(member))

    @commands.has_permissions(ban_members=True)
    @commands.command(aliases=['002-0102'])
    async def ban(self, ctx, user="", *, reason=""):
        """Ban a member. (Staff Only)"""
        try:
            member = ctx.message.mentions[0]
        except IndexError:
                await ctx.send("Please mention a user.")
                return
        if self.bot.admin_role in member.roles and (self.bot.owner_role not in ctx.message.author.roles):
                await ctx.send("You may not ban another staffer")
        else:
            try:
                if reason == "":
                    dm_msg = "You have been banned from {}.".format(ctx.guild.name)
                else:
                    dm_msg = "You have been banned from {} for the following reason:\n{}".format(ctx.guild.name, reason)
                if member == ctx.message.author:
                    await ctx.send("You cannot ban yourself!")
                    return
                else:
                    await self.dm(member, dm_msg)
                    await member.ban(delete_message_days=0)
                    await ctx.send("I've banned {}.".format(member))
                    emb = discord.Embed(title="Member Banned", colour=discord.Colour.red())
                    emb.add_field(name="Member:", value=member.name, inline=True)
                    emb.add_field(name="Mod:", value=ctx.message.author.name, inline=True)
                    if reason == "":
                        reason = "No reason specified."
                    emb.add_field(name="Reason:", value=reason, inline=True)
                    logchannel = self.bot.logs_channel
                    await logchannel.send("", embed=emb)
            except discord.errors.Forbidden:
                await ctx.send("💢 I dont have permission to do this.")

    @commands.has_permissions(manage_messages=True)
    @commands.command()

    async def lockdown(self, ctx, *, reason=""):
        """
        Lock down a channel
        """
        channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        if reason == "":
            await channel.send(":lock: Channel locked.")
        else:
            await channel.send(":lock: Channel locked. The given reason is: {}".format(reason))
        emb = discord.Embed(title="Lockdown", colour=discord.Colour.gold())
        ch = "{} ({})".format(ctx.channel.mention, ctx.channel.name)
        emb.add_field(name="Channel:", value=ch, inline=True)
        emb.add_field(name="Mod:", value=ctx.message.author, inline=True)
        if reason == "":
            reason = "No reason specified."
        emb.add_field(name="Reason:", value=reason, inline=True)
        logchannel = self.bot.logs_channel
        await logchannel.send("", embed=emb)

    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def unlock(self, ctx):
        """
        Unlock a channel
        """
        channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await channel.send(":unlock: Channel Unlocked")
        emb = discord.Embed(title="Unlock", colour=discord.Colour.gold())
        ch = "{} ({})".format(ctx.channel.mention, ctx.channel.name)
        emb.add_field(name="Channel:", value=ch, inline=True)
        emb.add_field(name="Mod:", value=ctx.message.author.name, inline=True)
        logchannel = self.bot.logs_channel
        await logchannel.send("", embed=emb)

    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def mute(self, ctx, member, *, reason=""):
        """Mutes a user. (Staff Only)"""
        try:
            member = ctx.message.mentions[0]
        except IndexError:
            return await ctx.send("Please mention a user.")

        if self.bot.muted_role in member.roles:
            return await ctx.send("{} is already muted!".format(member))

        try:
            await member.add_roles(self.bot.muted_role)
            await ctx.send("{} can no longer speak!".format(member))
            if reason == "":
                msg = "You have been muted in {} by {}. You will be DM'ed when a mod unmutes you.\n**Do not ask mods to unmute you, as doing so might extend the duration of the mute**".format(ctx.guild.name, ctx.message.author)
            else:
                msg = "You have been muted in {} by {}. The given reason is {}. You will be DM'ed when a mod unmutes you.\n**Do not ask mods to unmute you, as doing so might extend the duration of the mute**".format(ctx.guild.name, ctx.message.author, reason)
            await self.dm(member, msg)
            emb = discord.Embed(title="Member Muted", colour=discord.Colour.purple())
            emb.add_field(name="Member:", value=member, inline=True)
            emb.add_field(name="Mod:", value=ctx.message.author, inline=True)
            if reason == "":
                emb.add_field(name="Reason:", value="No reason specified.", inline=True)
            else:
                emb.add_field(name="Reason:", value=reason, inline=True)
            logchannel = self.bot.logs_channel
            await logchannel.send("", embed=emb)
        except discord.errors.Forbidden:
            await ctx.send("💢 I dont have permission to do this.")

    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def unmute(self, ctx, member):
        """Unmutes a user. (Staff Only)"""
        try:
            member = ctx.message.mentions[0]
        except IndexError:
            return await ctx.send("Please mention a user.")

        if self.bot.muted_role not in member.roles:
            return await ctx.send("{} is not muted!".format(member))

        try:
            await member.remove_roles(self.bot.muted_role)
            await ctx.send("{} is no longer muted!".format(member))
            msg = "You have been unmuted in {}.".format(ctx.guild.name)
            await self.dm(member, msg)
            emb = discord.Embed(title="Member Unmuted", colour=discord.Colour.purple())
            emb.add_field(name="Member:", value=member, inline=True)
            emb.add_field(name="Mod:", value=ctx.message.author, inline=True)
            logchannel = self.bot.logs_channel
            await logchannel.send("", embed=emb)
        except discord.errors.Forbidden:
            await ctx.send("💢 I dont have permission to do this.")


def setup(bot):
    bot.add_cog(Moderation(bot))
