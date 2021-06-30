#!/usr/bin/env python3
import os

from aws_cdk import core
from cdk_stack import CdkStack

identifier = os.environ["IDENTIFIER"]

app = core.App()

CdkStack(
    app,
    construct_id=f"cdk-cloudwatch-custom-metrics-{identifier}",
    identifier=identifier,
)

for k, v in {
    "Project": "cdk-cloudwatch-custom-metrics",
    "Stack": identifier,
    "Client": "Development Seed",
    "Owner": os.environ["OWNER"],
}.items():
    core.Tags.of(app).add(k, v, apply_to_launched_instances=True)

app.synth()
