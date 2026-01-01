from aws_cdk import (
    Stack,
    Duration,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    RemovalPolicy,
)
from constructs import Construct

class NexusCrmStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. Database
        table = dynamodb.Table(
            self, "NexusLeadsTable",
            partition_key=dynamodb.Attribute(name="lead_id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )

        # 2. Compute (Strictly Typed Architecture)
        ingest_function = _lambda.DockerImageFunction(
            self, "IngestLeadHandler",
            code=_lambda.DockerImageCode.from_image_asset("lambda_container"),
            environment={
                "TABLE_NAME": table.table_name,
                "MPLCONFIGDIR": "/tmp" 
            },
            memory_size=2048,
            timeout=Duration.seconds(30),
            # This ensures AWS runs it on Intel chips (matching your Dockerfile)
            architecture=_lambda.Architecture.X86_64
        )
        table.grant_write_data(ingest_function)

        # 3. API
        apigw.LambdaRestApi(
            self, "NexusApi",
            handler=ingest_function,
            proxy=True
        )