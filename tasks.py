import os
import boto3
from invoke import task
from os import getenv
from dotenv import find_dotenv, load_dotenv
from contextlib import contextmanager

load_dotenv(find_dotenv())

PROJECT_NAME = 'le-dash'
PROJECT_ROOT = '/var/www/%s' % PROJECT_NAME
VENV_DIR = os.path.join(PROJECT_ROOT, '.venv')
REPO = 'git@github.com:harvard-dce/%s.git' % PROJECT_NAME


@contextmanager
def lightsail_client():
    boto3.setup_default_session(
        profile_name=getenv('AWS_PROFILE'),
        region_name=getenv('AWS_REGION', 'us-east-1')
    )
    yield boto3.client('lightsail')


@task
def list(ctx):
    with lightsail_client() as client:
        resp = client.get_instances()
        for inst in resp['instances']:
            print("%s %s" % (inst['publicIpAddress'], inst['name']))


@task
def create(ctx, name, le_dash_revision='master', static_ip_name=None):
    new_instance(name, static_ip_name)
    deploy(name, le_dash_revision)


@task
def new_instance(name, static_ip_name=None):
    with lightsail_client() as client:
        client.create_instances(
            instanceNames=[name],
            availabilityZone='us-east-1e',
            blueprintId='string',
            bundleId='string',
            userData='apt-get -y update',
            keyPairName=getenv('AWS_KEYPAIR_NAME')
        )

        if static_ip_name is None:
            static_ip_name = name + '-ip'
            client.allocate_static_ip(
                staticIpName=static_ip_name
            )

        client.attach_static_ip(
            staticIpName=static_ip_name,
            instanceName=name
        )

        client.open_instance_public_ports(
            portInfo={
                'fromPort': 443,
                'toPort': 443,
                'protocol': 'tcp'
            },
            instanceName=name
        )


@task
def destroy(ctx, name, release_ip=True):
    with lightsail_client() as client:
        client.delete_instance(
            instanceName=name
        )
        if release_ip:
            client.release_static_ip(
                staticIpName=name + '-ip'
            )


@task
def deploy(ctx, name, le_dash_revision='master'):
    pass
