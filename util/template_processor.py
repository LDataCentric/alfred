import json
import os

from util.constants import (
    DOCKER_COMPOSE,
    DOCKER_COMPOSE_TEMPLATE,
    SERVICE_VERSIONS,
    SETTINGS,
    PATHS,
    PASSWORDS,
)
from util.docker_helper import get_credential_ip


def process_docker_compose_template(refinery_dir: str) -> None:

    credential_ip = get_credential_ip()
    cred_endpoint = f"{credential_ip}:7053"

    with open(DOCKER_COMPOSE_TEMPLATE, "r") as f:
        template = f.read()

    with open(PASSWORDS, "r") as f:
        passwords = json.load(f)

    with open(PATHS, "r") as f:
        paths = json.load(f)

    with open(SERVICE_VERSIONS, "r") as f:
        versions = json.load(f)

    with open(SETTINGS, "r") as f:
        settings = json.load(f)
        for volume, rel_path in settings.items():
            settings[volume] = os.path.normpath(os.path.join(refinery_dir, rel_path))

    docker_compose = template.format(
        **passwords,
        **paths,
        **versions,
        **settings,
        **{
            "CRED_ENDPOINT": cred_endpoint,
            # "MINIO_ENDPOINT": minio_endpoint,
        },
    )

    with open(DOCKER_COMPOSE, "w") as f:
        f.write(docker_compose)
