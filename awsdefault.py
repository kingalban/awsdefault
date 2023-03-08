from __future__ import annotations

import os
import sys
import configparser
from itertools import zip_longest
from pathlib import Path, PurePath
from typing import Generator


DEBUG = os.getenv("AWSDEFAULT_DEBUG")
DISABLE = os.getenv("AWSDEFAULT_DISABLE")


def log(*arg, **kwargs):
	if DEBUG: 
		print(*arg, **kwargs, file=sys.stderr)


# borrowed from https://github.com/asottile/awshelp
if sys.platform == 'win32':
    import subprocess

    def execvp(cmd: str, args: list[str]) -> int:
        return subprocess.call(args)
else: 
    from os import execvp


def read_config(path: Path | str) -> Generator[tuple[tuple, dict], None, None]:
	awsdefault = configparser.ConfigParser()
	awsdefault.read(path)
	for section in awsdefault.sections():
		yield tuple(section.strip().split()), dict(awsdefault.items(section)) 


def assemble_default_config(path) -> tuple[dict, list[str]]:
	defaults: dict[tuple, dict[str, str]] = {}
	config_files = []
	_path = PurePath()

	for part in path.parts:
		_path = _path.joinpath(part)
		if ".awsdefault" in (p.name for p in Path(_path).iterdir()):
			if Path(_path.joinpath(".awsdefault")).is_file():
				config_files.append(str(Path(_path.joinpath(".awsdefault"))))
				for section, _defaults in read_config(Path(_path.joinpath(".awsdefault"))):
					defaults[section] = {**defaults.get(section, {}), **_defaults}

	return defaults, config_files


def belongs_to_heirachy(command, pattern) -> bool:
	all_match = all(c == p for c, p in zip_longest(command, pattern))
	pattern_is_parent = all(c == p for c, p in zip(command, pattern))
	return all_match or pattern_is_parent


def create_cmd(argv) -> list[str]:
	cmd = argv
	cmd[0] = "aws"

	if not DISABLE:
		default_args, config_files = assemble_default_config(Path(os.getcwd()))

		log(f"using default args from files: {', '.join(config_files)}")

		subcommand = tuple(arg for arg in cmd[1:3] if not arg.startswith("-"))

		for section, arguments in default_args.items():
			if section == ("default",) or belongs_to_heirachy(subcommand, section):
				for key, val in arguments.items():
					key = f"--{key}"
					if key not in cmd:
						cmd.extend([key, val])
						if DEBUG:
							print(f"adding '{key} {val}'", file=sys.stderr)

	log(f"executing: {' '.join(cmd)}")

	return cmd


def main() -> int:
	cmd = create_cmd(sys.argv)
	return execvp(cmd[0], cmd)


if __name__ == "__main__":
	raise SystemExit(main())
