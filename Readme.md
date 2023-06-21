Kast is an ArgoCD 'applications of applications' system designed to function in conjunction with other components of the magical k8s framework. This setup includes the Spellbook specification, Rune style charting, and the RunicIndexer, which provides access to various glyphs that can be used to augment existing spells.

The use of a pseudo-magical lexicon, inspired by Arthur C. Clark's three laws, is a conscious effort to avoid confusion with the often-overlapping terminologies prevalent in technology. For instance, differentiating between issues that arise on the 'deployment side' versus those that occur within the 'deployment object' can often be confusing. To streamline the process and make terminology easier to comprehend, the term 'spell' has been introduced to refer to an 'application', while 'spellDefinition' refers to the configuration of a spell.

The Spellbook is a specification of a Git repository that houses configurations, analogous to chapters and spells. It is designed to simplify the classification of configurations for different clusters, production environments, or even smaller development spaces.

To enhance the versatility of spells, a Rune specification is used with its corresponding glyph to define a Helm chart or Kubernetes objects that can be incorporated into a spell. This system allows for the efficient detection and use of common resources. For example, it facilitates the identification of the default Istio gateway name provided by the book, which is used to create virtual services and mesh entries for other spells, such as ArgoCD or Vault.

To ensure that the system is functional and efficient, continuous iterations and improvements are implemented based on ongoing observations and feedback.


## Usage
to get the minimal definition of an spell u can use the default spell defined on ur book that we call summon because it summons ur code to life or to a healthy k8s state.

for example u can create a nginx like this using our summon spell
```yaml
name: nginx
```
or define a more complex and external spell like so:
```yaml
spell:
  name: nginx
  repository: https://github.com/nginxinc
  revision: master
  path: deployment/charts
  definition:
    service: #this is not rly needed but is a good example
      type: ClusterIP
      port: 80
```

more documentation is comming soon


## License

This project is licensed under the Creative Commons Attribution-ShareAlike NonCommercial (CC BY-SA-NC) license. See the [LICENSE](LICENSE) file for details.

