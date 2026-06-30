from .config import ScoreFeedConfig
from .linking import ScoreFeedLinking
from .listener import ScoreFeedListener
from .viewer import ScoreFeedViewer

def setup(bot):
    bot.add_cog(ScoreFeedConfig(bot))
    bot.add_cog(ScoreFeedLinking(bot))
    bot.add_cog(ScoreFeedListener(bot))
    bot.add_cog(ScoreFeedViewer(bot))