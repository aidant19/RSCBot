import discord
import os.path
import os
import re

from .utils.dataIO import dataIO
from discord.ext import commands
from cogs.utils import checks

class Transactions:
    """Used to set franchise and role prefixes and give to members in those franchises or with those roles"""

    DATA_FOLDER = "data/transactionConfiguration"
    CONFIG_FILE_PATH = DATA_FOLDER + "/config.json"

    CONFIG_DEFAULT = {}

    def __init__(self, bot):
        self.bot = bot
        self.check_configs()
        self.load_data()

    @commands.command(pass_context=True)
    async def sign(self, ctx, user : discord.Member, teamRole : discord.Role):
        """Assigns the team role, franchise role and prefix to a user when they are signed and posts to the assigned channel"""
        if teamRole in user.roles:
            await self.bot.say(":x: {0} is already on the {1}".format(user.mention, teamRole.mention))
            return
        
        server = ctx.message.server
        self.load_data()
        server_dict = self.config.setdefault(server.id, {})
        franchise_dict = server_dict.setdefault("Franchise roles", {})
        prefix_dict = server_dict.setdefault("Prefixes", {})

        gmName = re.findall(r'(?<=\()\w*\b', teamRole.name)[0]
        try:
            franchiseRole = self.find_role(server.roles, franchise_dict[gmName])
        except KeyError:
            await self.bot.say(":x: No role found in dictionary for {0}".format(gmName))
            return
        except LookupError:
            await self.bot.say(":x: Could not find franchise role for {0}".format(gmName))
            return

        try:
            prefix = prefix_dict[gmName]
        except KeyError:
            await self.bot.say(":x: No prefix found in dictionary for {0}".format(gmName))
            return
        
        try:
            channelId = server_dict['Transaction Channel']
            try:
                leagueRoleId = server_dict['League Role']
                try:
                    leagueRole = self.find_role(server.roles, leagueRoleId)
                    channel = server.get_channel(channelId)
                    message = "{0} was signed by the {1}.".format(user.mention, teamRole.mention)
                    await self.bot.add_roles(user, teamRole, leagueRole, franchiseRole)
                    await self.bot.change_nickname(user, "{0} | {1}".format(prefix, user.name))
                    await self.bot.send_message(channel, message)
                except LookupError:
                    await self.bot.say(":x: Could not find league role with id of {0}".format(leagueRoleId))
            except KeyError:
                await self.bot.say(":x: League role not currently set")
        except KeyError:
            await self.bot.say(":x: Transaction log channel not set")

    @commands.command(pass_context=True)
    async def cut(self, ctx, user : discord.Member, teamRole : discord.Role):
        """Removes the team role and franchise role, and adds the free agent prefix to a user and posts to the assigned channel"""
        if teamRole not in user.roles:
            await self.bot.say(":x: {0} is not on the {1}".format(user.mention, teamRole.mention))
            return

        server = ctx.message.server
        self.load_data()
        server_dict = self.config.setdefault(server.id, {})
        franchise_dict = server_dict.setdefault("Franchise roles", {})

        gmName = re.findall(r'(?<=\()\w*\b', teamRole.name)[0]
        try:
            franchiseRole = self.find_role(server.roles, franchise_dict[gmName])
            await self.bot.remove_roles(user, teamRole, franchiseRole)
            await self.bot.change_nickname(user, "FA | {1}".format(user.name))
            freeAgentRole = self.find_role(server.roles, server_dict['Free Agent'])
            await self.bot.add_roles(user, freeAgentRole)
        except KeyError:
            await self.bot.say(":x: No role found in dictionary for {0}".format(gmName))
            return
        except LookupError:
            await self.bot.say(":x: Could not find franchise role for {0}".format(gmName))
            return
        
        try:
            channelId = server_dict['Transaction Channel']
            channel = server.get_channel(channelId)
            message = "{0} was cut by the {1}. He will now be on waivers.".format(user.mention, teamRole.mention)
            await self.bot.send_message(channel, message)
        except KeyError:
            await self.bot.say(":x: Transaction log channel not set")

    # @commands.command(pass_context=True)
    # async def trade(self, ctx, user : discord.Member, newTeamRole : discord.Role, 
    #     user2 : discord.Member, newTeamRole2 : discord.Role):

    # @commands.command(pass_context=True)
    # async def sub(self, ctx, user : discord.Member, teamRole : discord.Role):

    def find_role(self, roles, roleId):
        for role in roles:
            if role.id == roleId:
                return role
        raise LookupError('roleId not found in server roles')

    # Config
    def check_configs(self):
        self.check_folders()
        self.check_files()

    def check_folders(self):
        if not os.path.exists(self.DATA_FOLDER):
            os.makedirs(self.DATA_FOLDER, exist_ok=True)

    def check_files(self):
        self.check_file(self.CONFIG_FILE_PATH, self.CONFIG_DEFAULT)

    def check_file(self, file, default):
        if not dataIO.is_valid_json(file):
            dataIO.save_json(file, default)

    def load_data(self):
        self.config = dataIO.load_json(self.CONFIG_FILE_PATH)

    def save_data(self):
        dataIO.save_json(self.CONFIG_FILE_PATH, self.config)

def setup(bot):
    bot.add_cog(Transactions(bot))