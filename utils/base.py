from discord.ext import commands

from .decorators import LEB


class LEBBase:
    @LEB
    async def parent_command(self, ctx: commands.Context) -> None:
        """
        We even have the use of parents. This will work as usual for ext.commands but will be un-invokable for app commands.
        This is a discord limitation as groups are un-invokable.
        """
        if ctx.invoked_subcommand is None:
            await ctx.send("Hello, you invoked the parent command!")
