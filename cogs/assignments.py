import sys

from discord.ext import commands

sys.path.append("..")
from utils.base import LEBBase


class Assignments(commands.Cog, LEBBase):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @LEBBase.parent_command.group(name="assignments")
    async def assignments(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send("Hello, you invoked the child command!")

    @assignments.command(name="list")
    async def assignments_list(self, ctx: commands.Context) -> None:
        await ctx.send(f"Here is a list of assignments!")

    @assignments.command(name="add")
    async def assigments_add(self, ctx: commands.Context) -> None:
        await ctx.send(f"Added Assignment!")

    @assignments.command(name="del")
    async def assigments_delete(self, ctx: commands.Context) -> None:
        await ctx.send(f"Assignment deleted!")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Assignments(bot))
