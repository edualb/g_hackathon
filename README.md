# gHackathon
gHackathon is a PoC for the Google Hackathon.

# Video:

# How to start the application:

Pre-requisites:
    - Go
    - Docker

1. (Optional) You can use the current `data` folder, however if you want to update the `data` folder with latest information run:
```
$ go run ./cmd/main.go
```
    - It is important to note this script can be broken if the application has new information and the translation is not ready. You need to include new information.

2. Start all Docker Containers:
```
$ docker compose up . -d
```