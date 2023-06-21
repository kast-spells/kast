
Kast is an argocd apps of apps to work in conjuction with the rest of the magical kubernetes abstraction that includes the spellbooc spec, runes style of charting and the runicIndexer to access the diferent glyphs u can use to extend exisiting spells.

we are using pseudo-magical lexicon becauese the three laws of Arthur C. Clark and because all the other techy words are already taken. What do i mean with this, how many times do u needed to explain that the issue is on the deployment side no in the deployment object and why are thouse diferent things or for us started happening witht the app definition and what an app is so we take a easy route and call it spell and the values or configuration or how do u need to config any given spell is called a definition hence a spellDefinition.

we combine our spells in a spellbook that is a specification of a git repository with some files a directories that we call chapters and spells. the idea behind this was how do u call the thingie that holds all ur configurations for a cluster or production or even the space for a little dev enviroment.

to add a way to extend ur spells in a simple way we use a rune specification with his glyph to define a helm chart or some k8s objects u want to use in a spell. for example we use this way to detect the name of the istio gateway the book provides by default and is used to create the virtual services and mesh entry for other spells like the argocd or vault ones. (more on this later)

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

