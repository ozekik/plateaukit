from __future__ import annotations

import click

from plateaukit.logger import set_log_level


# https://alexdelorenzo.dev/notes/click.html
class OrderCommands(click.Group):
    def list_commands(self, ctx):
        return list(self.commands)


# https://stackoverflow.com/a/76624494/10954858
class AliasCliGroup(click.Group):
    def command(self, *args, **kwargs):
        """Adds the ability to add `aliases` to commands."""

        def decorator(f):
            aliases = kwargs.pop("aliases", None)
            if aliases and isinstance(aliases, list):
                name = kwargs.pop("name", None)
                if not name:
                    raise click.UsageError(
                        "`name` command argument is required when using aliases."
                    )

                base_command = super(AliasCliGroup, self).command(
                    name, *args, **kwargs
                )(f)

                for alias in aliases:
                    cmd = super(AliasCliGroup, self).command(alias, *args, **kwargs)(f)
                    cmd.help = f"Alias for '{name}'.\n\n{cmd.help}"
                    cmd.params = base_command.params

            else:
                cmd = super(AliasCliGroup, self).command(*args, **kwargs)(f)

            return cmd

        return decorator


class CustomCliGroup(AliasCliGroup, OrderCommands):
    pass


@click.group(
    cls=CustomCliGroup,
    context_settings=dict(help_option_names=["-h", "--help"], show_default=True),
    no_args_is_help=True,
)
@click.option(
    "-v", "--verbose", is_flag=True, default=False, help="Enable verbose mode."
)
def cli(verbose):
    if verbose:
        set_log_level("DEBUG")
