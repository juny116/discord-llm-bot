"""Select a Discord LLM bot version."""

import argparse
import runpy
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", choices=["v1", "v2", "moderation"])
    parser.add_argument("options", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    module = (
        "discord_llm.moderation_bot"
        if args.version == "moderation"
        else f"discord_llm.{args.version}.bot"
    )
    sys.argv = [module, *args.options]
    runpy.run_module(module, run_name="__main__")


if __name__ == "__main__":
    main()
