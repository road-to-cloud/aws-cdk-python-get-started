from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_events as events,
    aws_events_targets as targets,
    aws_s3_notifications as s3_notifications,
)
from constructs import Construct

class AppStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Create an S3 bucket
        bucket = s3.Bucket(self, "MyBucket")

        # Create the first Lambda function
        scheduled_lambda = _lambda.Function(
            self, "ScheduledLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="scheduled_lambda.handler",
            code=_lambda.Code.from_asset("app/lambda"),
            environment={
                'BUCKET_NAME': bucket.bucket_name
            }
        )

        # Schedule the first Lambda function
        rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.rate(Duration.minutes(5)),
        )
        rule.add_target(targets.LambdaFunction(scheduled_lambda))

        # Create the second Lambda function
        s3_listen_lambda = _lambda.Function(
            self, "S3ListenLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="s3_listen_lambda.handler",
            code=_lambda.Code.from_asset("app/lambda"),
        )

        # Grant the first Lambda permissions to write to the S3 bucket
        bucket.grant_write(scheduled_lambda)

        # Trigger the second Lambda on S3 object creation
        notification = s3_notifications.LambdaDestination(s3_listen_lambda)
        bucket.add_event_notification(s3.EventType.OBJECT_CREATED, notification)

        # Grant the second Lambda permissions to read from the S3 bucket
        bucket.grant_read(s3_listen_lambda)
