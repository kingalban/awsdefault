# awsdefault

Automatically add arguments to the aws cli from config files if they were not specified
All `.awsdefault` files on the path to the current working directory are evaluated, with closer configs overwriting earlier.

For example, running awsdefault in the directory `first_project`, the options in `.awsdefault (A)`, `.awsdefault (B)` and `.awsdefault (C)` will be added.
Running awsdefault in `my_project` will collect the defaults from `.awsdefault (A)` and `.awsdefault (B)`.
~~~
/
├── .awsdefault (A)
└── my_projects
		├── .awsdefault (B)
		├── first_project
		│		└── .awsdefault (C)
		└── second_project
				└── .awsdefault (D)
~~~

`.awsdefault` must have a section called `default`. From there, keys are interpreted as keyword arguments, adding `--` to the start of them and appending them to the final `aws` command.

Example `.awsdefault` file:
~~~
cat .awsdefault

[default]
profile=my-fave-profile
region=eu-central-1
cluser=cluster-name
~~~

If an argument is literally specified when calling `awsdefault` it will not be replaced by any default.
If a default argument is specified in two `.awsdefault` files, the value on the deeper path will be used.

## motivation
For some project / directory I want to always add `--profile <xyz>` ect. to aws cli.
This allows for default arguments to be set at any project level.

## installation + setup
~~~ 
pip install awsdefault
alias aws=awsdefault
~~~


## inspiration
the wonderful [asotilie's](https://github.com/asottile) similar tool [awshelp](https://github.com/asottile/awshelp).
ironically, these two tools can't be used together
