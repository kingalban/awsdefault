# awsdefault

Automatically add arguments to the aws cli from config files if they were not specified
All `.awsconfig` files on the path to the current working directory are evaluated, with closer configs overwriting earlier.

For example, running awsdefault in the directory `first_project`, the options in `.awsconfig (A)` and `.awsconfig (B)` will be added, with `(B)` taking taking precedence.
~~~ 
/
├── .awsconfig (A)
└── my_projects
		├── .awsconfig
		├── first_project
		│		└── .awsconfig (B)
		└── second_project
				└── .awsconfig (C)
~~~ 

`.awsconfig` must have a section called `default`. From there, keys are interpreted as keyword arguments, adding `--` to the start of them and appending them to the final `aws` command.

Example `.awsconfig` file:
~~~
cat .awsconfig

[default]
profile=my-fave-profile
region=eu-central-1
cluser=cluster-name
~~~

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