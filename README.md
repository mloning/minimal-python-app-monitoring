# Minimal Python app monitoring using Prometheus and Grafana

## Requirements

* [Docker](http://docker.com)
* [minikube](https://github.com/kubernetes/minikube) (or some other Kubernetes cluster)
* [kubectl](https://kubernetes.io/docs/tasks/tools/)
* [helm](http://helm.sh)

## Start minikube

```bash
minikube start
```

##  Install monitoring stack

For details, see [kube-prometheus-stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack) and
[loki-stack](https://github.com/grafana/helm-charts/tree/main/charts/loki-stack).

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace
helm upgrade loki-stack grafana/loki-stack --install --namespace=monitoring --set loki.isDefault=false
```

## Connect to Grafana dashboard

```bash
kubectl port-forward service/kube-prometheus-stack-grafana 3000:80 --namespace monitoring
```

where `80` is the [Grafana](https://grafana.com) service port. To look up port for the Grafana service, run: `kubectl get service -n monitoring | grep grafana`.

You can now log in to dashboard at [http://localhost:3000/](http://localhost:3000/).

The default credentials are:

* username: "admin"
* password: "prom-operator"

To look them up, run:

```bash
kubectl get secret kube-prometheus-stack-grafana -n monitoring -o json | jq -r '.data."admin-user"' | base64 --decode
kubectl get secret kube-prometheus-stack-grafana -n monitoring -o json | jq -r '.data."admin-password"' | base64 --decode
```

where `kube-prometheus-stack-grafana` is the name of the config map.

## Install minimal Python app

The application is based on an [example](https://github.com/JasonHaley/hello-python) from the [Kubernetes blog](https://kubernetes.io/blog/2019/07/23/get-started-with-kubernetes-using-python/).

### Build image

```bash
eval $(minikube docker-env)
docker build . --tag minimal-app:latest
```

The first line enables us to use local images in minicube when we set the image pull policy to "Never" in the k8s manifest files (see [docs](https://minikube.sigs.k8s.io/docs/commands/docker-env/)).

### Run app in Docker (optional)

```bash
docker run --rm -p 5001:5000 minimal-app:latest
```

To check the app in Docker, open [http://localhost:5001/](http://localhost:5001/).

### Run app in Kubernetes

```bash
kubectl apply -f ./k8s/
kubectl port-forward service/minimal-app-service 5001:6000 
```

To check the app in k8s, open [http://localhost:5001/](http://localhost:5001/) (or [http://localhost:5001/docs](http://localhost:5001/docs) for API docs).

## View logs

Logs should be visible on the Grafana dashboard, when selecting Loki as the data source (e.g. on the [Explore](https://grafana.com/docs/grafana/latest/explore/) page).

To filter out the application logs, run this [LogQL](https://grafana.com/docs/loki/latest/logql/) query:

```bash
{app="minimal-app"} |= `` 
```

##  Clean up

```bash
minikube stop
minikube delete
```
