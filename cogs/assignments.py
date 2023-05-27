import sys
from datetime import datetime
from typing import Callable, List, Optional

import discord
from discord.components import SelectOption
from discord.ext import commands

sys.path.append("..")
from pathlib import Path

from utils import constants, database
from utils.base import LEBBase


class AssignmentsVoteButton(discord.ui.View):
    def __init__(self, ctx: commands.Context, assignment: database.Assignment) -> None:
        super().__init__()
        self.ctx = ctx
        self.assignment = assignment

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green)
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if interaction.permissions.administrator:
            await interaction.message.add_reaction("✅")
            await interaction.response.send_message("Approved!", ephemeral=False)
            database.add_assignments(self.assignment)
            self.stop()
        else:
            await interaction.response.send_message("You are not an administrator!", ephemeral=True)


class AssigmentsSelect:
    @staticmethod
    def get_options() -> List[SelectOption]:
        assignments = database.get_list_of_assignments()
        options = [
            SelectOption(
                label=assignment.name,
                description=f"`{assignment.id}` {assignment.description}",
                value=assignment.unique_id,
            )
            for assignment in assignments
        ]
        return options


class AssigmentsDeleteView(discord.ui.View):
    def __init__(self, *, timeout: float = 180) -> None:
        super().__init__(timeout=timeout)
        self.select_menu = discord.ui.Select(
            placeholder="Select an assignment to delete",
            options=AssigmentsSelect.get_options(),
            min_values=1,
            max_values=1,
        )

        # Callback for when the select menu receives a selection.
        async def callback(interaction: discord.Interaction) -> None:
            unique_id = int(self.select_menu.values[0])
            assignment = database.get_assignment(unique_id)
            database.remove_assignments(unique_id)

            await interaction.response.send_message(f"{assignment.name} has been deleted!", ephemeral=False)

        self.add_item(self.select_menu)
        self.select_menu.callback = callback


class Assignments(commands.Cog, LEBBase):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def assignments_to_embed(self, assignments: list[database.Assignment]) -> discord.Embed:
        # Create the embed.
        embed = discord.Embed(
            title="List of assignments",
            description=f"Here is a list of assignments!",
            color=discord.Color.red(),
        )

        # Add the fields to the embed.
        for assignment in assignments:
            embed.add_field(
                name=assignment.name,
                value=f"ID: {assignment.id}\nDue: {assignment.due}\nDescription: {assignment.description}",
                inline=False,
            )

        # Return the embed.
        return embed

    @LEBBase.parent_command.group(name="assignments")
    async def assignments(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send("Hello, you invoked the child command!")

    @assignments.command(name="list")
    async def assignments_list(self, ctx: commands.Context) -> None:
        assignments = database.get_list_of_assignments()
        if not len(assignments):
            await ctx.send("There are no assignments!")
        else:
            embed = self.assignments_to_embed(assignments)
            await ctx.send(embed=embed)

    @assignments.command(name="add")
    async def assigments_add(
        self,
        ctx: commands.Context,
        id: str,
        name: str = "Untitled",
        due: str = "",
        description: str = "This assignment has no description.",
    ) -> None:
        if not len(due):
            # The due date was not provided, we will set it to next week.
            due = (datetime.now() + datetime.timedelta(weeks=1)).strftime("%Y-%m-%d")

        # Create the assignment object.
        assignments = database.get_list_of_assignments()
        assignment = database.Assignment(unique_id=len(assignments), id=id, name=name, due=due, description=description)

        if ctx.interaction.permissions.administrator:
            # The user is an admin all assignments will be added to the database directly.
            await ctx.send(f"Added Assignment by {ctx.author.mention}! {id} {name} {due}", ephemeral=False)
            database.add_assignments(assignment)
        else:
            # The user is not an admin, we need to vote on the assignment with another user.

            thumbnail_path = constants.THUMBNAIL_ASSIGNMENTS_ADD_PATH
            thumbnail = discord.File(thumbnail_path, filename=Path(thumbnail_path).name)

            # Vote buttons.
            view = AssignmentsVoteButton(ctx=ctx, assignment=assignment)

            # Create the embed.
            embed = discord.Embed(
                title="Voting for adding new assignments",
                description=f"due on `{due}` from user {ctx.author.mention}",
                color=discord.Color.red(),
            )

            # Add the thumbnail to the embed and add the fields.
            embed.set_thumbnail(url=f"attachment://{thumbnail.filename}")
            embed.add_field(name="Name", value=name, inline=True)
            embed.add_field(name="ID", value=id, inline=True)
            await ctx.send(embed=embed, file=thumbnail, view=view, ephemeral=False)

    @assignments.command(name="del")
    async def assigments_delete(self, ctx: commands.Context) -> None:
        # Delete an assignment.
        delete_view = AssigmentsDeleteView()

        # Display the selected item.
        await ctx.send("select an assignment to delete", view=delete_view)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Assignments(bot))
