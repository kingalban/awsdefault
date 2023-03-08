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

`.awsdefault` should have sections named with aws sub commands, with the exception of `[default]` which will be added to all commands.
 From there, keys are interpreted as keyword arguments, adding `--` to the start of them and appending them to the final `aws` command.

Example `.awsdefault` file:
~~~
$ cat .awsdefault

[default]
profile=my-fave-profile
region=eu-central-1
cluser=cluster-name

# applies to all subcommands of 'log' (including 'describe-log-streams')
[logs]
log-group-name=my-log-group
log-stream-name=random-log-stream-123

# only applies to sub-subcommand
[logs describe-log-streams]
order-by=updated_at
~~~

~~~
$ AWSDEFAULT_DEBUG=1 awsdefault logs get-log-events
using default args from files: /media/alban/Shared/Shared_Documents/Zervant/Projects/awsdefault/.awsdefault
adding '--profile example_profile'
adding '--log-stream-name random-log-stream-123'
adding '--log-group-name my-log-group'
executing: aws logs get-log-events --profile example_profile --log-stream-name random-log-stream-123 --log-group-name my-log-group

...

$ AWSDEFAULT_DEBUG=1 awsdefault help               
using default args from files: /media/alban/Shared/Shared_Documents/Zervant/Projects/awsdefault/.awsdefault
adding '--profile example_profile'
executing: aws help --profile example_profile

...
~~~


If an argument is literally specified when calling `awsdefault` it will not be replaced by any default.
If a default argument is specified in two `.awsdefault` files, the value on the deeper path will be used.

## motivation
For some project / directory I want to always add `--profile <xyz>` ect. to aws cli.
This allows for default arguments to be set at any project level.

## installation + setup
~~~ 
$ pip install awsdefault
$ alias aws=awsdefault
~~~


## inspiration
the wonderful [asotilie's](https://github.com/asottile) similar tool [awshelp](https://github.com/asottile/awshelp).
ironically, these two tools can't be used together
