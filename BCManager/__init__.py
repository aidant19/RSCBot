from .bcManager import BCManager
from .bcManager import config

def setup(bot):
    bot.add_cog(BCManager(bot))