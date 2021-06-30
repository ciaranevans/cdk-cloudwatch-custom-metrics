import json

from aws_cdk import (
    aws_cloudwatch,
    aws_events,
    aws_events_targets,
    aws_iam,
    aws_lambda,
    core,
)


class CdkStack(core.Stack):
    def __init__(
        self, scope: core.Construct, construct_id: str, identifier: str, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        metric_1 = aws_cloudwatch.Metric(
            metric_name="ciarans-metric-1", namespace="ciarans-metrics"
        )

        metric_2 = aws_cloudwatch.Metric(
            metric_name="ciarans-metric-2", namespace="ciarans-metrics"
        )

        metric_function = aws_lambda.Function(
            self,
            id=f"metric-function-{identifier}",
            code=aws_lambda.Code.from_inline(
                f"""
import boto3
import random

def handler(event, context):
    metric_data_1 = random.randint(0, 2000)
    metric_data_2 = random.randint(2000, 4000)
    metric_1 = {{
        "MetricName": "{metric_1.metric_name}",
        "Dimensions": [],
        "Unit": "None",
        "Value": metric_data_1
    }}
    metric_2 = {{
        "MetricName": "{metric_2.metric_name}",
        "Dimensions": [],
        "Unit": "None",
        "Value": metric_data_2
    }}
    print(f"Logging: {{metric_1}} {{metric_2}}")
    cloudwatch = boto3.client("cloudwatch")
    cloudwatch.put_metric_data(
        Namespace="{metric_1.namespace}",
        MetricData=[metric_1]
    )
    cloudwatch.put_metric_data(
        Namespace="{metric_2.namespace}",
        MetricData=[metric_2]
    )
"""
            ),
            handler="index.handler",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            timeout=core.Duration.seconds(10),
            retry_attempts=0,
        )

        metric_function.role.add_to_policy(
            aws_iam.PolicyStatement(
                effect=aws_iam.Effect.ALLOW,
                resources=["*"],
                actions=["cloudwatch:PutMetricData"],
            )
        )

        aws_events.Rule(
            self,
            id=f"metric-upload-rule-{identifier}",
            schedule=aws_events.Schedule.expression("cron(* * * * ? *)"),
        ).add_target(aws_events_targets.LambdaFunction(metric_function))

        widget = aws_cloudwatch.GraphWidget(
            left=[metric_1, metric_2],
            period=core.Duration.minutes(1),
            title="Ciarans Test Widget",
        )

        core.CfnOutput(self, "widget-json", value=json.dumps(self.resolve(widget)))
