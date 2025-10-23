from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from commands.create import CreateTableCommand
from commands.insert import InsertCommand
from commands.select import SelectCommand
from commands.update import UpdateCommand
from commands.delete import DeleteCommand
from database import Database


class PyDBCLI:
    def __init__(self):
        self.db = Database()
        self.session = PromptSession()
        self.running = True

        # Use a dictionary for commands: easy to retrieve by key
        self.commands = {
            "create": CreateTableCommand(self.db),
            "insert": InsertCommand(self.db),
            "select": SelectCommand(self.db),
            "update": UpdateCommand(self.db),
            "delete": DeleteCommand(self.db)
        }

        # Command completion
        self.sql_completer = WordCompleter(
            ["create table", "insert into", "select", "update", "delete from", "help", "exit"],
            ignore_case=True
        )

        # CLI theme
        self.style = Style.from_dict({
            "prompt": "bold #00ffff",
            "error": "bold #ff5555",
            "info": "#ffffff",
        })

    # ---------------------- MAIN LOOP ----------------------
    def run(self):
        print("🚀 Welcome to pydb CLI (modular version)")
        print("💡 Type 'help' for commands, 'exit' to quit.\n")

        while self.running:
            try:
                user_input = self.session.prompt(
                    [("class:prompt", "pydb> ")],
                    completer=self.sql_completer,
                    style=self.style
                ).strip()

                if not user_input:
                    continue

                if user_input.lower() in {"exit", "quit"}:
                    print("👋 Exiting pydb...")
                    break

                self.execute(user_input)

            except KeyboardInterrupt:
                print("\n🛑 Press Ctrl+D or type 'exit' to quit.")
            except EOFError:
                break
            except Exception as e:
                print(f"⚠️  {e}")

    # ---------------------- COMMAND ROUTER ----------------------
    def execute(self, user_input: str):
        """Route SQL-like input to the appropriate Command class."""
        tokens = user_input.split()
        base_cmd = tokens[0].lower()

        # Map "delete from" and "create table"
        if base_cmd == "delete" and len(tokens) > 1 and tokens[1].lower() == "from":
            base_cmd = "delete"
        elif base_cmd == "create" and len(tokens) > 1 and tokens[1].lower() == "table":
            base_cmd = "create"

        command_obj = self.commands.get(base_cmd)
        if not command_obj:
            print("❓ Unknown command. Type 'help' for available commands.")
            return

        result = command_obj.execute(user_input)
        if result:
            print(result)


if __name__ == "__main__":
    PyDBCLI().run()
