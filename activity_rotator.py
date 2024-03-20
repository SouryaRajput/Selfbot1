import discord
from discord.ext import commands, tasks
import asyncio
import random

class StatusRotator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.activities = []  
        self.change_activity.start()

    def cog_unload(self):
        self.change_activity.stop()

    @tasks.loop(seconds=3)
    async def change_activity(self):
        if self.activities:
            activity = random.choice(self.activities)
            await self._change_activity(activity)
            await asyncio.sleep(5)

    async def _change_activity(self, activity):
        if activity.startswith("stream"):
            _, message = activity.split(" ", 1)
            await self.bot.change_presence(
                activity=discord.Streaming(name="Lucifer", url="https://www.twitch.tv/Lucifer", details=message, platform="Twitch")
            )
        elif activity.startswith("play"):
            custom_image_url = "https://media.discordapp.net/attachments/1176041182204268586/1189433664048730112/Untitled_Project_6.jpg?ex=659e256c&is=658bb06c&hm=9828e49fd3fd0215efac2b4aa934415b75d5fa30eb577a9d01cb99628e9d21b9&=&format=webp&width=448&height=448"
            await self.bot.change_presence(activity=discord.Game(name=activity[5:], image=custom_image_url))
        elif activity.startswith("listen"):
            await self.bot.change_presence(activity=discord.Game(name="Listening to " + activity[7:]))
        elif activity.startswith("watch"):
            await self.bot.change_presence(activity=discord.Game(name="Watching " + activity[6:]))
        else:
            await self.bot.change_presence(activity=discord.Game(name=activity))

    @commands.command()
    async def activityrotator(self, ctx, *, activities):
        # Split activities by commas
        self.activities = [activity.strip() for activity in activities.split(',')]
        await ctx.send("`-` **ACTIVITY ROTATION HAS BEEN SET**")

    @commands.command()
    async def activityrotator_stop(self, ctx):
        self.change_activity.stop()
        await ctx.send("`-` **ACTIVITY ROTATION STOPPED**")

def setup(bot):
    bot.add_cog(StatusRotator(bot))
