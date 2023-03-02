from __future__ import annotations

import os
import sys
import subprocess
import configparser
from pathlib import Path, PurePath


DEBUG = os.getenv("AWSDEFAULT_DEBUG")
DISABLE = os.getenv("AWSDEFAULT_DISABLE")

# borrowed from https://github.com/asottile/awshelp
if sys.platform == 'win32':
    import subprocess

    def execvp(cmd: str, args: list[str]) -> int:
        return subprocess.call(args)
else: 
    from os import execvp


def assemble_default_config(path) -> dict:
	defaults = {}
	_path = PurePath()

	for part in path.parts:
		_path = _path.joinpath(part)

		if ".awsconfig" in (p.name for p in Path(_path).iterdir()):
			if Path(_path.joinpath(".awsconfig")).is_file():
				awsconfig = configparser.ConfigParser()
				awsconfig.read(Path(_path.joinpath(".awsconfig")))
				defaults = {**defaults, **dict(awsconfig.items("default"))}

	return defaults


def main() -> int:
	cmd = sys.argv
	cmd[0] = "aws"

	if not DISABLE:
		# default_args, config_file  = get_most_local_config(Path(os.getcwd()))
		default_args = assemble_default_config(Path(os.getcwd()))

		if DEBUG:
			print(f"using default args from {config_file!r}", file=sys.stderr)

		for arg, val in default_args.items():
			arg = "--"+arg
			if arg not in cmd:
				cmd.extend([arg, val])
				if DEBUG:
					print(f"adding {arg} {val}", file=sys.stderr)

	return execvp(cmd[0], cmd)


if __name__ == "__main__":
	raise SystemExit(main())
