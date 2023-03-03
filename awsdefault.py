from __future__ import annotations

import os
import sys
import subprocess
import configparser
from pathlib import Path, PurePath
from typing import Generator


DEBUG = os.getenv("AWSDEFAULT_DEBUG")
DISABLE = os.getenv("AWSDEFAULT_DISABLE")

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


def main() -> int:
	cmd = sys.argv
	cmd[0] = "aws"

	if not DISABLE:
		default_args, config_files = assemble_default_config(Path(os.getcwd()))

		if DEBUG:
			print(f"using default args from files: {', '.join(config_files)}", file=sys.stderr)

		subcommand = tuple(arg for arg in cmd[1:3] if not arg.startswith("-"))

		for section, arguments in default_args.items():
			if section == ("default",) or section == subcommand:
				for key, val in arguments.items():
					key = f"--{key}"
					if key not in cmd:
						cmd.extend([key, val])
						if DEBUG:
							print(f"adding '{key} {val}'", file=sys.stderr)

	if DEBUG:
		print(f"executing: {' '.join(cmd)}", file=sys.stderr)

	return execvp(cmd[0], cmd)


if __name__ == "__main__":
	raise SystemExit(main())
