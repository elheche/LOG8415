# LOG8415
Advanced Concepts of Cloud Computing

# Assignment 1

usage: main.py [-h] [-r] [-d] {aws} ...

Program that creates two clusters of virtual machines and deploys a flask app to them.It first looks for credentials and configuration files provided by your AWS CLI (You
can configure your AWS CLI using this command: <aws configure>). If not found, it offers you the option to manually enter their values using the arguments below:

optional arguments:
  -h, --help    show this help message and exit
  -r, --reset   reset user's aws account.
  -d, --docker  enable test scenarios through docker.

aws arguments:
  {aws}

usage: main.py aws [-h] -g AWS_REGION_NAME -i AWS_ACCESS_KEY_ID -s AWS_SECRET_ACCESS_KEY -t AWS_SESSION_TOKEN

optional arguments:
  -h, --help            show this help message and exit
  -g AWS_REGION_NAME, --region AWS_REGION_NAME
                        region name for your AWS account.
  -i AWS_ACCESS_KEY_ID, --id AWS_ACCESS_KEY_ID
                        access key for your AWS account.
  -s AWS_SECRET_ACCESS_KEY, --secret AWS_SECRET_ACCESS_KEY
                        secret key for your AWS account.
  -t AWS_SESSION_TOKEN, --token AWS_SESSION_TOKEN
                        session key for your AWS account.
