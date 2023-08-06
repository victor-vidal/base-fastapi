docker_cmd:
    docker-compose -f development.yml $(cmd)

dinfra:
    docker-compose -f development.yml up --build -d db minio redis

infra:
    docker-compose -f development.yml up --build db minio redis

dall:
    docker-compose -f development.yml up --build -d

all:
    docker-compose -f development.yml up --build

dback:
    docker-compose -f development.yml up --build -d worker server

back:
    docker-compose -f development.yml up --build worker server

dserver:
    docker-compose -f development.yml up --build -d server

server:
    docker-compose -f development.yml up --build server

dworker:
    docker-compose -f development.yml up --build -d server

worker:
    docker-compose -f development.yml up --build server

exec:
    docker-compose -f development.yml exec server $(cmd)
