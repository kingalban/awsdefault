import pytest
import awsdefault


@pytest.mark.parametrize(
	('aws_command', 'config_pattern', 'result'),
	(
		("logs", 	"logs",		True),
		("logs x", 	"logs",		True),
		("logs x", 	"logs x",	True),
		("ecs", 	"logs",		False),
		("ecs x", 	"logs",		False),
		("logs y", 	"logs x",	False),
	)
)
def test_belongs_to_heirachy(aws_command, config_pattern, result):
	aws_command = aws_command.split()
	config_pattern = config_pattern.split()

	assert awsdefault.belongs_to_heirachy(aws_command, config_pattern) is result
 
