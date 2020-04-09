c.JupyterHub.authenticator_class = 'ldapauthenticator.LDAPAuthenticator'
c.LDAPAuthenticator.server_address = '172.17.0.2'
c.LDAPAuthenticator.bind_dn_template = [
    "uid={username},dc=example,dc=org"
]

c.JupyterHub.spawner_class = 'simplespawner.SimpleLocalProcessSpawner'
c.SimpleLocalProcessSpawner.args = ['--allow-root']
