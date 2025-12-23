import aws_cdk as core
import aws_cdk.assertions as assertions

from nexus_crm.nexus_crm_stack import NexusCrmStack

# example tests. To run these tests, uncomment this file along with the example
# resource in nexus_crm/nexus_crm_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = NexusCrmStack(app, "nexus-crm")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
