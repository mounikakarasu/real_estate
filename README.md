AWS CDK Infrastructure Project
This is written in Python. It allows cloud infrastructure to be defined using code and deployed to AWS through CloudFormation. The project includes a basic CDK application and the configuration required to synthesize and deploy infrastructure stacks.

Stack:
Infrastructure as Code- AWS Cloud Development Kit (CDK)
Deployment- AWS CloudFormation
Language- Python
Environment- Python Virtual Environment (.venv)

Tools:
AWS CDK CLI
Python
CloudFormation
Virtual Environment (venv)

to see it working:
-Create and activate a Python virtual environment
python -m venv .venv

-Activate the environment
Windows
.venv\Scripts\activate
macOS / Linux
source .venv/bin/activate

-Install dependencies
pip install -r requirements.txt

-List available stacks
cdk ls

-Generate the CloudFormation template
cdk synth

-Deploy the stack to AWS
cdk deploy

-Compare deployed infrastructure with local changes
cdk diff

-Open CDK documentation
cdk docs
