## README

This guide contains the setup steps to build out arbitrary demos.

__Install Environment__

```bash
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install python python-pip python-dev

sudo add-apt-repository ppa:gophers/archive
sudo apt-get update
sudo apt-get install golang-1.9-go

mkdir /home/davidgee/go
mkdir /home/davidgee/go/{src,pkg,bin}

go get github.com/ryanuber/readme-server
```

Add in the export entries to the profile:

```bash
export GOPATH=$HOME/go
export PATH=$PATH:/home/davidgee/go/bin
export PATH=$PATH:/usr/lib/go-1.9/bin
```

When you're ready, you can launch any of the READMEs via a browser.
Pages are presented on port 5678:

```bash
go build -o ./readme github.com/ryanuber/readme-server
./readme -dont-open
```
