```yaml
name: argocd #application name
repository: https://github.com/argoproj/argo-helm.git #tanto como para git como para helm
path: charts/argo-cd # en el caso de ser un helm repo usar chart: nombre del chart
revision: argo-cd-5.46.8
namespace: argocd # opcional si no existe toma el nombre de la app
noHelm: true #default is false toma el contenido de el repo + path como solo archivos yaml y aplica en argo
definition: #equivalente a values 
  dex:
    enabled: false
  global:
    image:
      tag: v2.9.0-rc2


appParams:
  disableAutoSync: true
  ignoreDifferences:
    - group: admissionregistration.k8s.io
      kind: ValidatingWebhookConfiguration
      name: istiod-default-validator
      jsonPointers:
        - /webhooks/0/failurePolicy
  managedNamespaceMetadata: #https://argo-cd.readthedocs.io/en/stable/user-guide/sync-options/#namespace-metadata
    labels:
      istio-injection: enabled
  # Sync policy
  syncPolicy:
    # managedNamespaceMetadata:
    #   labels: # The labels to set on the application namespace
    #     any: label
    #     you: like
    # annotations: # The annotations to set on the application namespace
    #   the: same
    #   applies: for
    #   annotations: on-the-namespace
    automated: # automated sync by default retries failed attempts 5 times with following delays between attempts ( 5s, 10s, 20s, 40s, 80s ); retry controlled using `retry` field.
      prune: true # Specifies if resources should be pruned during auto-syncing ( false by default ).
      selfHeal: true # Specifies if partial app sync should be executed when resources are changed only in target Kubernetes cluster and no git change detected ( false by default ).
      # allowEmpty: false # Allows deleting all application resources during automatic syncing ( false by default ).
    syncOptions: # Sync options which modifies sync behavior
      - CreateNamespace=true # Namespace Auto-Creation ensures that namespace specified as the application destination exists in the destination cluster.
      - PrunePropagationPolicy=foreground # Supported policies are background, foreground and orphan.
      - PruneLast=true # Allow the ability for resource pruning to happen as a final, implicit wave of a sync operation
    # The retry feature is available since v1.7
    retry:
      limit: 2 # number of failed sync attempt retries; unlimited number of attempts if less than 0
      backoff:
        duration: 5s # the amount to back off. Default unit is seconds, but could also be a duration (e.g. "2m", "1h")
        factor: 2 # a factor to multiply the base duration after each failed retry
        maxDuration: 3m # the maximum amount of time allowed for the backoff strategy
useExistingProject: default # optional by default uses the spellbok name
cleanDefinition: true # default is false. if true will remove any custom data added to the value conten of the helm for using in case of hard defined helm charts
app: #deberia exisitir dentro de app params 
  annotations: #argocd app annotations
    enviroment: prod
  customFinalaizers: []
  skipCrds: true # helm/argocd parameter

runes: #esto permite dentro de una sola argo app instalar varios repos dfe helm o no se puede usar para dependencias o plugins de cosas ej istio como todo un set
  - repository: https://github.com/otro/repo.git
    path: cosa # en el caso de ser un helm repo usar chart: nombre del chart
    revision: argo-cd-5.46.8
    definition: # y sus values

```

## License

This project is licensed under the Creative Commons Attribution-ShareAlike NonCommercial (CC BY-SA-NC) license. See the [LICENSE](LICENSE) file for details.

