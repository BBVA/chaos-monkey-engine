# Deploy to DockerHub
VERSION=$(cat VERSION)
docker build -t bbvalabs/chaos-monkey-engine:$VERSION -t bbvalabs/chaos-monkey-engine:latest .
docker login -e $DOCKER_EMAIL -u $DOCKER_USER -p $DOCKER_PASS
docker push bbvalabs/chaos-monkey-engine:$VERSION
docker push bbvalabs/chaos-monkey-engine:latest
