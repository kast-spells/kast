
helm install argocd -n argocd --create-namespace -f extra-values.yaml .

```shell
kubectl create secret generic kast-ssh-secret \
  --namespace=argocd \
  --from-file=sshPrivateKey=/home/namen/.ssh/id_rsa \
  --from-literal=url="git@github.com:kast-spells" \
  --type=Opaque 

kubectl label secret kast-ssh-secret argocd.argoproj.io/secret-type=repo-creds -n argocd
```