
.PHONY: serve
serve:
	@docker-compose run --rm -p 80:80 -e BASE_PROXY_URL='https://arduino-wifi-config.netlify.app' -e PYTHONPATH='.' -v `pwd`:/app backend  uvicorn main:app --host 0.0.0.0 --port 80 --reload

.PHONY: container
container:
	@docker buildx build --platform=linux/amd64 -t http-proxy/backend:local -f Dockerfile .

.PHONY: dependencies
dependencies:
	@docker run --rm -e PYTHONPATH='.' -v `pwd`:/app http-proxy/backend:local pip-compile requirements.in
	@docker build --no-cache -t http-proxy/backend:local  -f Dockerfile .
