# Minimal Python app monitoring using Prometheus and Grafana

## Requirements

* [Docker](http://docker.com)
* [minikube](https://github.com/kubernetes/minikube) (or some other Kubernetes cluster)
* [kubectl](https://kubernetes.io/docs/tasks/tools/)
* [helm](http://helm.sh)

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

For details, see [Grafana](https://grafana.com).

1. Look up port for Grafana service: `kubectl get service -n monitoring`
1. Forward local port to Grafana service port: `kubectl port-forward service/kube-prometheus-stack-grafana 3000:80 --namespace monitoring`
where `80` is the Grafana service port
1. Look up Grafana username and password: `kubectl get secret kube-prometheus-stack-grafana -n monitoring -o json | jq -r '.data."admin-user"' | base64 --decode` and `kubectl get secret kube-prometheus-stack-grafana -n monitoring -o json | jq -r '.data."admin-password"' | base64 --decode` where `kube-prometheus-stack-grafana` is the name of the config map
1. Log in to dashboard at `http://localhost:3000/`

## Install minimal Python app

The application is loosely based on an [example](https://github.com/JasonHaley/hello-python) from the Kubernetes blog [post](https://kubernetes.io/blog/2019/07/23/get-started-with-kubernetes-using-python/).
Python logging to [Loki](https://grafana.com/oss/loki/) uses the [python-loggin-loki](https://github.com/GreyZmeem/python-logging-loki) package, as described [here](https://medium.com/geekculture/pushing-logs-to-loki-without-using-promtail-fc31dfdde3c6).

### Build image

1. `eval $(minikube docker-env)` (to use local images in minicube with `imagePullPolicy: Never`, see [docs](https://minikube.sigs.k8s.io/docs/commands/docker-env/))
1. `docker build . --tag minimal-app:latest`

### Check app

`docker run --rm -p 5001:5000 minimal-app:latest` to check app in Docker at `http://localhost:5001/` or `http://localhost:5001/docs`

### Deploy to k8s

1. `kubectl apply -f ./k8s/`
1. `kubectl port-forward 5001:6000 service/minimal-app-service` to check app in k8s at `http://localhost:5001/` or `http://localhost:5001/docs`

Logs should now be visible on the Grafana dashboard [Explore](https://grafana.com/docs/grafana/latest/explore/), when selecting Loki as the data source.

##  Clean up

`minikube stop; minikube delete`
