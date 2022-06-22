import yaml


def get_config(file_name="config.yaml"):
    with open(file_name, 'r') as fd:
        y = yaml.safe_load(fd)
    return y
