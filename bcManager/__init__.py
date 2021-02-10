from .bcManager import BCManager
from . import config

def setup(bot):
    bot.add_cog(BCManager(bot))