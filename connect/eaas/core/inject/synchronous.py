import os

from fastapi import Depends, Header


from connect.client import ConnectClient


def get_installation_client(
    x_connect_installation_api_key: str = Header(),
    x_connect_api_gateway_url: str = Header(),
    x_connect_user_agent: str = Header(),
):
    return ConnectClient(
        x_connect_installation_api_key,
        endpoint=x_connect_api_gateway_url,
        use_specs=False,
        default_headers={'User-Agent': x_connect_user_agent},
    )


def get_extension_client(
    x_connect_api_gateway_url: str = Header(),
    x_connect_user_agent: str = Header(),
):
    return ConnectClient(
        os.getenv('API_KEY'),
        endpoint=x_connect_api_gateway_url,
        use_specs=False,
        default_headers={'User-Agent': x_connect_user_agent},
    )


def get_installation(
    client: ConnectClient = Depends(get_installation_client),
    x_connect_extension_id: str = Header(),
    x_connect_installation_id: str = Header(),
):
    extension = client('devops').services[x_connect_extension_id]
    return extension.installations[x_connect_installation_id].get()


def get_environment(
    client: ConnectClient = Depends(get_installation_client),
    x_connect_extension_id: str = Header(),
    x_connect_environment_id: str = Header(),
):
    extension = client('devops').services[x_connect_extension_id]
    return list(extension.environments[x_connect_environment_id].variables.all())