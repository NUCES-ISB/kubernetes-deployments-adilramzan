# 1. Install Python dependencies
install:
	@echo "Installing Python dependencies..."
	pip install --upgrade pip
	pip install -r app/requirements.txt
	pip install pytest pylint kubernetes

# 2. Lint code using pylint (disabling C and R messages)
lint:
	@echo "Linting code..."
	pylint --disable=CR app/app.py

# 3. Run tests
test:
	@echo "Running tests..."
	python -m pytest test.py -v

# 4. Run the Flask app locally (Flask runs on port 5000)
run:
	@echo "Running Flask app..."
	cd app && python app.py

# 5. Build Docker image for the Flask app
docker-build:
	@echo "Building Docker image..."
	cd app && docker build -t flask-app:latest .

# 6. Kubernetes commands

# Start Minikube if not already running
minikube-start:
	@echo "Starting Minikube..."
	minikube start

# Stop Minikube
minikube-stop:
	@echo "Stopping Minikube..."
	minikube stop

# Set Docker env to use Minikube's Docker daemon
minikube-docker-env:
	@echo "Setting Docker environment to Minikube..."
	eval $$(minikube docker-env)

# Deploy all Kubernetes resources
k8s-deploy: minikube-start minikube-docker-env docker-build
	@echo "Deploying to Kubernetes..."
	kubectl apply -f manifests/configmap/postgres-configmap.yaml
	kubectl apply -f manifests/secret/postgres-secret.yaml
	kubectl apply -f manifests/deployment/postgres-deployment.yaml
	kubectl apply -f manifests/service/postgres-service.yaml
	kubectl apply -f manifests/deployment/flask-deployment.yaml
	kubectl apply -f manifests/service/flask-service.yaml

# Get the URL to access the Flask app
get-url:
	@echo "Getting URL for Flask app..."
	minikube service flask-app --url

# Show all Kubernetes resources
k8s-status:
	@echo "Showing Kubernetes status..."
	kubectl get all

# Scale Flask deployment
scale-flask:
	@echo "Scaling Flask deployment..."
	kubectl scale deployment flask-app --replicas=$(REPLICAS)

# Create submission artifacts
create-snapshots:
	@echo "Creating submission snapshots..."
	mkdir -p submission/screenshots
	kubectl get pods -o wide > submission/screenshots/pods.txt
	kubectl get all > submission/screenshots/all-resources.txt
