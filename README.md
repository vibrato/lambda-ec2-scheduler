# EC2 Start/Stop Scheduler

Starts/Stops EC2 instances based on their tags:

	Scheduler:Start   H:7 M:00 DOW:01234
	Scheduler:Stop    H:19 M:00 DOW:01234

Tags are parsed as:

* H - hour to start
* M - minute to start (not currently implemented)
* DOW - Days of Week to start (Monday is 0 and Sunday is 6)

Tags can be customised inside `lambda_function.py`. Also can be restricted to a set `FILTER` for damage mitigation (see filters in `aws ec2 describe-instances help` for available filters).

# Build
To create a deployment package (code+dependencies):

	./build.sh

# Permissions
Required role permissions:

	{
		"Version": "2012-10-17",
		"Statement": [
			{
				"Effect": "Allow",
				"Action": [
					"ec2:DescribeInstances",
					"ec2:StartInstances",
					"ec2:StopInstances"
				],
				"Resource": [
					"*"
				]
			}
		]
	}
