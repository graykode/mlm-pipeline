# install terraform and ansible
sudo apt update

sudo apt-get install python3 python-dev python3-dev \
     build-essential libssl-dev libffi-dev \
     libxml2-dev libxslt1-dev zlib1g-dev \
     python-pip -y

wget https://releases.hashicorp.com/terraform/0.11.13/terraform_0.11.13_linux_amd64.zip && \
    unzip terraform_0.11.13_linux_amd64.zip && \
    rm terraform_0.11.13_linux_amd64.zip && \
    sudo mv terraform /usr/bin && sudo chmod +x /usr/bin/terraform

wget https://raw.githubusercontent.com/alicek106/aws-terraform-kubernetes/4c1e79e9ee6299afb846fee1e763d8ff9b9d88b0/ansible/requirements.txt && \
    pip3 install -r requirements.txt
