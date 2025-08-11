import os

import dotenv


def setup():
    # Reload the variables in your '.env' file (override the existing variables)
    dotenv.load_dotenv(".env", override=True)


def main():
    setup()

    WRKBNCH_TGGL_ENGINE_VERSION = os.getenv("WRKBNCH_TGGL_ENGINE_VERSION", "stable")

    print(f"Using Prompting Workbench Engine Version: {WRKBNCH_TGGL_ENGINE_VERSION}")

    from prompting_workbench.cli_engine import CliEngine

    cli_engine = CliEngine()
    cli_engine.start()


if __name__ == "__main__":
    main()
