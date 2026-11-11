# Local Kubernetes deployment

These manifests target Docker Desktop Kubernetes and use locally built images.
For local browser access, use `kubectl port-forward` as shown below. A
NodePort service does not necessarily map its port to Windows localhost in a
Docker Desktop kind cluster.

## 1. Start a local cluster

In Docker Desktop, enable Kubernetes in **Settings > Kubernetes** and wait for
the cluster to start. Confirm that `kubectl` is using the Docker Desktop
context:

```powershell
kubectl config get-contexts
kubectl config use-context docker-desktop
kubectl get nodes
```

If you use Minikube or kind instead, select that context and load the locally
built images into the cluster before deploying.

## 2. Build the images

Run these commands from the `src` directory:

```powershell
docker build -t enterprise-ai-backend:local .\backend
docker build --build-arg NEXT_PUBLIC_API_BASE_URL=http://localhost:30080 -t enterprise-ai-frontend:local .\frontend
```

Docker Desktop's Kubernetes cluster uses its own containerd image store. A
successful `docker build` only adds images to Docker's local image store, so
the Kubernetes node may not see them. If pods report `ErrImageNeverPull`,
import the images into the Docker Desktop node. In Docker Desktop, enable
**Show system containers** in the Kubernetes view, then from PowerShell:

```powershell
docker save -o .\enterprise-ai-k8s-images.tar enterprise-ai-backend:local enterprise-ai-frontend:local
docker cp .\enterprise-ai-k8s-images.tar desktop-control-plane:/enterprise-ai-k8s-images.tar
docker exec desktop-control-plane ctr -n k8s.io images import /enterprise-ai-k8s-images.tar
docker exec desktop-control-plane rm /enterprise-ai-k8s-images.tar
Remove-Item .\enterprise-ai-k8s-images.tar
```

The node container name may differ if the cluster was configured differently;
check `docker ps -a` after enabling system containers. Confirm both images are
available to Kubernetes with `kubectl describe pod -n enterprise-ai -l app=backend`
and the equivalent command for `app=frontend`, or simply wait for the pods to
retry. For other local clusters, use their documented image-loading command.

The frontend API URL is compiled into the browser bundle at build time. It
must be reachable from the browser, so do not use the Kubernetes-only service
DNS name here.

## 3. Deploy and verify

```powershell
kubectl apply -f .\k8s\app.yaml
kubectl get pods,services,pvc -n enterprise-ai
kubectl rollout status deployment/backend -n enterprise-ai
kubectl rollout status deployment/frontend -n enterprise-ai
```

The backend Deployment waits for its schema initialization and health probe.
The frontend starts independently and has its own startup, readiness, and
liveness probes. Open two PowerShell windows from the `src` directory and run:

```powershell
kubectl port-forward service/frontend 30000:3000 -n enterprise-ai
```

```powershell
kubectl port-forward service/backend 30080:8000 -n enterprise-ai
```

Keep both commands running while using the app. Open
`http://localhost:30000` and the API docs at `http://localhost:30080/docs`.

Ollama is expected to run on the Windows host, with the `llama3.2` and
`nomic-embed-text` models available. The ConfigMap defaults to
`http://host.docker.internal:11434`; if your cluster cannot resolve or reach
that address, change `OLLAMA_BASE_URL` in `app.yaml` to an address reachable
from your Kubernetes node, then re-apply the manifest.

## 4. Learn common Kubernetes operations

```powershell
kubectl get all,pvc -n enterprise-ai
kubectl describe pod -n enterprise-ai -l app=backend
kubectl logs deployment/backend -n enterprise-ai
kubectl logs deployment/frontend -n enterprise-ai
kubectl port-forward service/backend 8000:8000 -n enterprise-ai
```

To test replacing frontend pods:

```powershell
kubectl rollout restart deployment/frontend -n enterprise-ai
kubectl rollout status deployment/frontend -n enterprise-ai
kubectl rollout history deployment/frontend -n enterprise-ai
```

For an application update, build a new image tag and update the Deployment:

```powershell
docker build -t enterprise-ai-frontend:v2 --build-arg NEXT_PUBLIC_API_BASE_URL=http://localhost:30080 .\frontend
kubectl set image deployment/frontend frontend=enterprise-ai-frontend:v2 -n enterprise-ai
kubectl rollout status deployment/frontend -n enterprise-ai
```

If the rollout fails, return to its previous revision with
`kubectl rollout undo deployment/frontend -n enterprise-ai`.

To scale the stateless frontend:

```powershell
kubectl scale deployment/frontend --replicas=3 -n enterprise-ai
kubectl get pods -n enterprise-ai -l app=frontend -w
```

Keep the backend at one replica: it uses SQLite on a `ReadWriteOnce` volume,
which is not safe for multiple backend replicas. Its update strategy also
avoids starting two backend pods against that database volume at once. For
multi-replica backend scaling, move the database to a shared server such as
PostgreSQL and revisit file storage.

## 5. Stop or remove the deployment

```powershell
kubectl delete deployment backend frontend -n enterprise-ai
kubectl delete service backend frontend -n enterprise-ai
kubectl delete configmap backend-config -n enterprise-ai
```

These commands stop the app but retain its PVCs, database, and uploaded files.
To permanently delete the stored data and namespace, explicitly delete them:

```powershell
kubectl delete pvc backend-data backend-uploads -n enterprise-ai
kubectl delete namespace enterprise-ai
```
