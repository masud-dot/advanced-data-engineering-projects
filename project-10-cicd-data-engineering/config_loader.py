import os, yaml
env=os.getenv('ENVIRONMENT','dev')
config=yaml.safe_load(open(f'configs/{env}.yaml'))
