> [!IMPORTANT]
> WIP!!

# Kast

### Description

> Todo!

## How to use Kast

### Create Bookrack

First you need a repository to manage Kast Bookrack,

```Bash
mkdir my-bookrack
cd my-bookrack
git init
```

After that you need to "install" kast on your repository


```Bash
git submodule add https://github.com/kast-spells/kast.git kast
```

Now create a directory with the name `bookrack` to manage your books inside

> [!IMPORTANT]
> The name bookrack is mandatory since this is the directory that kast uses to build you Bookrack in ArgoCD

```bash
mkdir bookrack
cd bookrack # my-bookrack/bookrack
```

After that, you are ready to setup your first book, now, lets make it, as an example this book is going to be called "my-first-book"

> [!WARNING]
> name must be lower case to comply with kubernetes namerules

```bash
mkdir my-first-book
cd my-first-book #my-bookrack/bookrack/my-first-book
```

A book needs an `index.yaml` file that says the "chapters" and book name, just like this.

```yaml
#my-bookrack/bookrack/my-first-book/index.yaml
name: my-first-book
chapters:
   - production
```
> [!IMPORTANT]
> Chapters have to be added manually so you can work with you repo without having to sync non-ready chapters

as you seen we added a chapter named production so we have to add this chapter's directory!

```bash
mkdir production
cd production #my-bookrack/bookrack/my-first-book/production
```

You can add index files and more stuff on chapters but for this basic instalation guide, we are going to just add a spell (app), which looks something like this:

```yaml
#my-bookrack/bookrack/my-first-book/production/app-name.yaml
name: app-name
repository: git@github.com:helmchart/chart.git
path: /path/to/chart
revision: main # or any branch or release you prefer
namespace: app-name # or the namespace you prefer
values: # add the values you want to override from default values
   someValueToOverride:
   - name: override-this
# Kast gonna take the default value and just replace the things that you modified here

appParams: 
  disableAutoSync: true
```

now we can git add, commit and push all out changes to a remote repo. lets imagine is in `me/my-bookrack`

your directory tree should look like this:
```
my-bookrack
│
├── bookrack
│   └── my-first-book
│       ├── production
│       │   └── app-name.yaml
│       └── index.yaml
└── kast # ...
```
now we have a spell on a chapter, on a book, on a bookrack, now we have to add the bookrack to argoCD and let Kast do the rest.

create a new manifest like this one and apply it.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-bookrack
  namespace: argocd
spec:
  project: default
  source:
    repoURL: git@github.com:me/my-bookrack.git
    targetRevision: main
    path: kast # dont change this!
    helm:
      parameters:
        - name: "name"
          value: my-first-book
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    retry:
      limit: 2
    syncOptions:
      - CreateNamespace=true
```

now apply this manifest and now you can see your app of apps on argocd! and keep track on values from bookrack repository

> [!WARNING]
> A known issue is that sometimes it can fail of sync since the project (with the name of the book) is not created, you can solve this by simple syncing the project name first

---
# OLD TUTORIAL
1) in a git repository that will be used to store the spellbooks:


2) create the library directory, here will be stored each of your spellbooks
3) create a directory for a spellbook with its name in the folder
4) create any number of directories inside the spellbook, each one of this will be your chapters
5) create an index.yaml file inside the spellbook directory and add a yaml following this example
```yaml
name: spellbookName #the name of the main spellbook folder
chapters:
  - chapterName #the name of the folders inside the spellbook
```
6) inside your chapters create your spell files. lower is an example of values to install argocd
7) commit your changes
8) create an argocd application to start the process
```yaml
---
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: spellbookName
  namespace: argocd
spec:
  project: default # if u change the project remember to create it before
  source:
    repoURL: git@github.com:Project/repo.git
    targetRevision: master
    path: kast # this will be the submodule path u create 
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    retry:
      limit: 2
    syncOptions:
      - CreateNamespace=true
```
9) (optional) y can create a spell file with the definition to your kast installation so u can administrate ur kast from kast

## Example Values

```yaml
name: argocd #application name
repository: https://github.com/argoproj/argo-helm.git #tanto como para git como para helm
path: charts/argo-cd # en el caso de ser un helm repo usar chart: nombre del chart
revision: argo-cd-5.46.8
namespace: argocd # opcional si no existe toma el nombre de la app
noHelm: true #default is false toma el contenido de el repo + path como solo archivos yaml y aplica en argo
values: #equivalente a values 
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
  annotations: #argocd app annotations
    enviroment: prod
  customFinalaizers: []
  skipCrds: true # helm/argocd parameter

useExistingProject: default # optional by default uses the spellbok name
cleanDefinition: true # default is false. if true will remove any custom data added to the value conten of the helm for using in case of hard defined helm charts

clusterSelector:
  environment: prod #needs a k8s-cluster definition in the lexicon to be used
projectDisabled: true #will disable the creation of the project
projectName: "" #if defined will override the spellbook name can be combined with projectDisabled
runes: #esto permite dentro de una sola argo app instalar varios repos dfe helm o no se puede usar para dependencias o plugins de cosas ej istio como todo un set
  - repository: https://github.com/otro/repo.git
    path: cosa # en el caso de ser un helm repo usar chart: nombre del chart
    revision: argo-cd-5.46.8
    values: # y sus values

```
## Using Chapters and herency: 

inside each chapter folder you can create a new index.yaml file the content of this can have any configuration and it will be added or overwrite any spellbook definition

the herency is from bigger to small when the smaller is always the more important one


## Lexicon:
the lexicon is a compilation of infrastructure or resources that can be consumed by a book.
the only ifrastructure needed for kast as an appOfApps is the clusters where the apps will be instaled
each cluster defined in the lexicon need to be added to the argocd where the spellbook will be used
```yaml
lexicon:
  - name: jorge
    type: k8s-cluster
    labels:
      environment: dev
    clusterURL: https://jorge.clusters.api
```
when used with a `clusterSelector` in any index or spell file will match all the labels in the selector with the ones in the lexicon if no cluster is selected will defautl to the local cluster

## aditional stuff

```
glosary:
  lexicon: is a list of small snipets of configuration that provides a pointer to a rune of some type and enable the consumption of it
  spellbook: a set of spell definitions used to implement each thing u will use and need
  defaultSpell: the default spell to apply to a definition in case it does not contains a spell tree
  spell: a helm chart used to create resources in a k8s enviroment
  defaultGlyphs: a list of glyphs that will be added to all the spells on it scope (spellbook or chapter)
  chapter: a directory with can have an index.yaml to with his own set of spells (equal to a k8s namespace)
  glyph: a helm chart used in conjuntion with a spell definitin to consume through the lexicon a specific rune
  definition: the "values" of a helm chart, the conntent of the values.yaml file
  kast-glyph: a helm library with only .tpl files to consume the lexicon 
  summon: kast default spell to create workload a helm chart to create a deployment, sts or cronjob
  runicSelectors: a set of labels used in the summon to consume from the lexicon
```

#### spellbook Spec
```
bookrack/bookName/index.yaml
bookrack/bookName/intro/mysql.yaml
bookrack/bookName/bases/index.yaml
bookrack/bookName/bases/hello-world.yaml
```



## License

This project is licensed under the Creative Commons Attribution-ShareAlike NonCommercial (CC BY-SA-NC) license. See the [LICENSE](LICENSE) file for details.

