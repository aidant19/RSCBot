from .replayManager import ReplayerManager

def setup(bot):
    bot.add_cog(ReplayManager(bot))