import git
import base64
import os
from kubernetes import client, config
import subprocess
import yaml
import shutil

# Variables
git_ssh_key_path = '/home/namen/.ssh/id_rsa'
helm_values_file = '../../library/hildy/ishtar/argocd.yaml'
repo_dest = '/tmp/helm-chart-repo'

# Load Helm values from file
with open(helm_values_file, 'r') as f:
    helm_values = yaml.safe_load(f)

# Clone Git repository with SSH key for a specific version
git.Repo.clone_from(helm_values['repository'], repo_dest, branch=helm_values['revision'], env={'GIT_SSH_KEY': git_ssh_key_path})


#write a temp file with a yaml based on helm_values.definition
with open('temp.yaml', 'w') as f:
    yaml.dump(helm_values['definition'], f)



# Set up Kubernetes client
config.load_kube_config()

# chart_path = os.path.join(repo_dest, helm_values['path'])
# subprocess.check_call([
#     'helm', 'upgrade', '--install',
#     helm_values['name'],
#     chart_path,
#     '--namespace', 'argocd',
#     '-f ./temp.yaml',
#     '--create-namespace'
# ])
# Remove cloned Git repository
shutil.rmtree(repo_dest)

# Remove temp file
os.remove('temp.yaml')

# Create SSH key secret for ArgoCD
with open(git_ssh_key_path, 'r') as f:
    git_ssh_key = f.read()

secret = client.V1Secret(
    api_version='v1',
    kind='Secret',
    type='Opaque',
    metadata=client.V1ObjectMeta(
        name='hildy-ssh-secret',
        namespace='argocd',
        labels={'argocd.argoproj.io/secret-type': 'repo-creds'}
    ),
    data={
        'sshPrivateKey': base64.b64encode(git_ssh_key.encode()).decode(),
        "url": base64.b64encode("git@github.com:hildy-ai/".encode()).decode(),
        }
)

k8s_client = client.CoreV1Api()
k8s_client.create_namespaced_secret(namespace='argocd', body=secret)
secret = client.V1Secret(
    api_version='v1',
    kind='Secret',
    type='Opaque',
    metadata=client.V1ObjectMeta(
        name='kast-ssh-secret',
        namespace='argocd',
        labels={'argocd.argoproj.io/secret-type': 'repo-creds'}
    ),
    data={
        'sshPrivateKey': base64.b64encode(git_ssh_key.encode()).decode(),
        "url": base64.b64encode("git@github.com:kast-spells/".encode()).decode(),
        }
)

k8s_client = client.CoreV1Api()
k8s_client.create_namespaced_secret(namespace='argocd', body=secret)
