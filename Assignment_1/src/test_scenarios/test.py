import docker


def create_file():
    alb_dns_name = "log8415-lab1-elb-1394081442.us-east-1.elb.amazonaws.com"
    f = open("Dockerfile", "w")
    f.write("FROM python:3 \n")
    f.write("ADD send_get_requests.py / \n")
    f.write("RUN pip install requests \n")
    f.write(f'CMD [ "python", "./send_get_requests.py", "--dns",  "{alb_dns_name}"] \n')
    f.close()


def main():
    create_file()
    client = docker.from_env()
    client.images.build(path="./", tag="log8415-test-scenarios")
    output = client.containers.run("log8415-test-scenarios")
    print()


if __name__ == '__main__':
    main()
