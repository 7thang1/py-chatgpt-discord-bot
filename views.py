import discord


def get_buttons(
    bot,
    process_command,
    command_name: str,
    prompt: str,
    history: int = 0,
    max_tokens: int = 1000,
    origin_data=None,
):
    class RegenerateView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=3 * 60)

        async def on_timeout(self):
            for child in self.children:
                child.disabled = True
            await self.message.edit(view=None)

        async def handle(self, interaction, temperature: float):
            await interaction.response.send_message("🔄 /*regenerate*")
            if temperature == -1:
                temperature = origin_data["temperature"]
            await process_command(
                bot=bot,
                command_name=command_name,
                ctx=interaction.channel,
                prompt=prompt,
                temperature=temperature,
                history=history,
                max_tokens=max_tokens,
                author=str(interaction.user),
                is_regenerate=True,
                origin_data=origin_data,
            )

        # @discord.ui.button(label="0.0 (Precise 🧠)")
        @discord.ui.button(label="0.0")
        async def regenerate_button_callback_00(self, button, interaction):
            await self.handle(interaction=interaction, temperature=0.0)

        @discord.ui.button(label="0.2")
        async def regenerate_button_callback_02(self, button, interaction):
            await self.handle(interaction=interaction, temperature=0.2)

        # @discord.ui.button(label="0.5 (Balanced ⚖️)")
        @discord.ui.button(label="0.5")
        async def regenerate_button_callback_05(self, button, interaction):
            await self.handle(interaction=interaction, temperature=0.5)

        @discord.ui.button(label="0.7")
        async def regenerate_button_callback_07(self, button, interaction):
            await self.handle(interaction=interaction, temperature=0.7)

        # @discord.ui.button(label="1.0 (Creative 🌟)")
        @discord.ui.button(label="1.0")
        async def regenerate_button_callback_10(self, button, interaction):
            await self.handle(interaction=interaction, temperature=1.0)

    return RegenerateView()
