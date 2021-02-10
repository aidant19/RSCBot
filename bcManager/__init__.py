from .bcManager import BCManager
from .config import config

def setup(bot):
    bot.add_cog(BCManager(bot))