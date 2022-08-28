# Minimal Python app monitoring on k8s with Grafana Loki

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

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm upgrade loki-stack grafana/loki-stack \
    --install \
    --namespace=monitoring \
    --create-namespace \
    --values ./helm/loki-stack-values.yaml
```

Wait for all resource to be available: `kubectl get pods -n monitoring -w`.

For details, see the [loki-stack](https://github.com/grafana/helm-charts/tree/main/charts/loki-stack) Helm chart.

## Connect to Grafana dashboard

```bash
kubectl port-forward service/loki-stack-grafana 3000:80 -n monitoring
```

where `80` is the Grafana service port. To look up the port, run: `kubectl get service -n monitoring | grep grafana`.

You can now log in to dashboard at [http://localhost:3000/](http://localhost:3000/).

To get the login credentials, run:

```bash
kubectl get secret loki-stack-grafana -n monitoring -o jsonpath='{.data.admin-user}' | base64 --decode; echo
kubectl get secret loki-stack-grafana -n monitoring -o jsonpath='{.data.admin-password}' | base64 --decode; echo
```

where `loki-stack-grafana` is the name of the config map.

## Install minimal Python app

The application is based on an [example](https://github.com/JasonHaley/hello-python) from the [Kubernetes blog](https://kubernetes.io/blog/2019/07/23/get-started-with-kubernetes-using-python/).

### Test app in Docker (optional)

```bash
docker build . -t minimal-app:latest
docker run --rm -p 5001:5000 minimal-app:latest
```

To check the app in Docker, open [http://localhost:5001/](http://localhost:5001/).

### Build image

```bash
eval $(minikube docker-env)
docker build . -t minimal-app:latest
```

The first line enables us to [use local images in minikube](https://minikube.sigs.k8s.io/docs/commands/docker-env/), when we set the image pull policy to "Never" in the k8s manifest files. This works by pointing your terminal's Docker client to the Docker client used inside minikube.

### Run app in Kubernetes

```bash
kubectl apply -f ./k8s/
kubectl port-forward service/minimal-app-service 5001:6000 
```

To check the app, open [http://localhost:5001/](http://localhost:5001/) (or [http://localhost:5001/docs](http://localhost:5001/docs) for API docs).

## View logs

To view logs on the Grafana dashboard, go to the [Explore](https://grafana.com/docs/grafana/latest/explore/) page and select Loki as the data source.

To filter out the application logs, run this [LogQL](https://grafana.com/docs/loki/latest/logql/) query:

```bash
{app="minimal-app"} |= `` 
```

To view logs in k8s, run:

```bash
kubectl logs -f -l app=minimal-app
```

##  Clean up

```bash
minikube stop
minikube delete
```
