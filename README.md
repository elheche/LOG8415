# LOG8415
Advanced Concepts of Cloud Computing

# Assignment 1

<p>Program that creates two clusters of virtual machines and deploys a flask app to them.It first looks for credentials and configuration files provided by your AWS CLI (You can configure your AWS CLI using this command: <em><strong>aws configure</strong></em>). If not found, it offers you the option to manually enter their values using the arguments below:</p>

## Run the program with default credentials

    usage: python3.9 main.py [-h] [-r] [-d] {aws} ...

### optional arguments:
    -h, --help    show this help message and exit
    -r, --reset   reset user's aws account.
    -d, --docker  enable test scenarios through docker.
    
## Run the program with manually entered credentials
    
### aws arguments:
    {aws}
    
    usage: python3.9 main.py aws [-h] -g AWS_REGION_NAME -i AWS_ACCESS_KEY_ID -s AWS_SECRET_ACCESS_KEY -t AWS_SESSION_TOKEN

### optional arguments:
    -h,                         --help                              show this help message and exit
    -g AWS_REGION_NAME,         --region    AWS_REGION_NAME         region name for your AWS account.
    -i AWS_ACCESS_KEY_ID,       --id        AWS_ACCESS_KEY_ID       access key for your AWS account.
    -s AWS_SECRET_ACCESS_KEY,   --secret    AWS_SECRET_ACCESS_KEY   secret key for your AWS account.
    -t AWS_SESSION_TOKEN,       --token     AWS_SESSION_TOKEN       session key for your AWS account.
    
## Note:
<p>If you want to run queries using Docker [-d/--docker], you need to have Docker installed and running on your machine.</p>
