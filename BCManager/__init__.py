from .BCManager import BCManager
from .BCManager import config

def setup(bot):
    bot.add_cog(BCManager(bot))
    
