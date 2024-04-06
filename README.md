# Github Parser

## Installation Guide
#### 1. Create compute cloud vm via ubuntu [link](https://console.yandex.cloud/folders/b1gb31l87647n7l0ha0g/compute/create-instance)
#### 2. Connect to it through ssh like
    ssh @{username}{vm_ip}
#### 3. Install docker
    snap install docker
#### 4. Clone that repository
    git clone https://github.com/ramazanix/github-parser.git && cd github_parser
#### 5. Define env variables. DB_HOSTNAME _must be_ ip of vm
    cat .env.example > .env; nano .env
#### 6. Run docker compose
    sudo docker compose up -d
#### 7. Wait one-two minutes
