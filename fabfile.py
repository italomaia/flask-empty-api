from fabric.api import env
from fabric.api import local
from fabric.api import run
from fabric.api import task
from fabric.context_managers import cd, lcd

import os
import json

env.forward_agent = True
env.user = 'root'
env.hosts = ['your production host']

project_dst = 'project-name'

compose_cmd = [
    'docker-compose',
    '-f', 'docker-compose.yml',
    '-f',
]

# service to run commands against
service_name = None
renv = 'dev'  # dev by default
opts = []
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STYLES_DIR = os.path.join(CURRENT_DIR, 'styles')
UX_DIR = os.path.join(CURRENT_DIR, 'ux')


def get_compose_cmd():
    return compose_cmd + ['docker-compose-%s.yml' % renv]


def get_fn():
    """
    Returns the correct function call for the environment.
    """
    return run if renv == 'prd' else local


def get_cmd_exists(cmd):
    def tell_on(arg, rs):
        if rs:
            print('"%s" found in path.' % arg)
        else:
            print('"%s" not found in path. Please, install it to continue.' % arg)  # noqa
        return rs

    fn = get_fn()
    rs = fn('which %s' % cmd, capture=True)
    return tell_on(cmd, ('not found' not in rs))


@task(alias='setup')
def do_setup():
    """
    Helps you setup your environment. Call it once per project.
    """
    msg = "Command not found. Please, install %s"
    assert get_cmd_exists('npm'), msg % "npm"
    assert get_cmd_exists('vue'), msg % "vue-cli"
    assert get_cmd_exists('fab'), msg % "fabric3"
    assert get_cmd_exists('docker'), msg % "docker"
    assert get_cmd_exists('docker-compose'), msg % "docker-compose"

    print("Setting up VueJS (just accept defaults)")
    local('vue init webpack ux', shell='/bin/bash')

    print("Setting up SemanticUI (just accept defaults)")
    with lcd(STYLES_DIR):
        local('npm install semantic-ui', shell='/bin/bash')

        semantic_settings = os.path.join(STYLES_DIR, 'semantic.json')
        with open(semantic_settings, 'r') as fs:
            data = json.load(fs)

        data['autoInstall'] = True
        with open(semantic_settings, 'w') as fs:
            json.dump(data, fs)

    print(
        "IMPORTANT: run the following command:\n"
        "sudo echo \"127.0.0.1  dv\" >> /etc/hosts")

    print(
        "IMPORTANT: make sure to update your envfile file with "
        "your project production configuration.")
    print(
        "IMPORTANT: make sure to update your fabfile "
        "hosts with your production host.")
    print("")
    print("Now you're ready to go:")
    print('  fab env:dev up  # for development mode')
    print('  fab env:prd up  # for production mode')
    print('  fab env:tst up  # to simulate production mode')
    print('Locally, your project will be available at http://dv:8080')


@task(alias='env')
def set_renv(local_renv):
    "Sets docker-compose environment"
    global renv
    assert local_renv in ('dev', 'prd')
    renv = local_renv


@task(alias='dae')
def set_daemon():
    opts.append('-d')


@task(alias='up')
def compose_up(name=None):
    """
    Calls docker compose up using the correct environment.
    """
    with cd(project_dst):
        local_cmd = get_compose_cmd() + ['up']
        local_cmd += opts
        local_cmd += [name] if name else []
        get_fn()(' '.join(local_cmd))


@task(alias='build')
def compose_build(name=None):
    """
    Calls docker compose build using the correct environment.
    """
    with cd(project_dst):
        local_cmd = get_compose_cmd() + ['build']
        local_cmd += [name] if name else []

        get_fn()(' '.join(local_cmd))


@task(alias='on')
def on_service(name):
    """
    Define service where command should run
    """
    global service_name
    service_name = name


@task(alias='run')
def compose_run(cmd):
    """
    Calls docker compose run using the correct environment.

    :param cmd: run command, including container name.
    """
    opts.append('--rm')

    if service_name is None:
        print("please, provide service name")
        exit()

    with cd(project_dst):
        local_cmd = get_compose_cmd() + ['run']
        local_cmd += opts
        local_cmd += [service_name]
        local_cmd += cmd.split()
        get_fn()(' '.join(local_cmd))


@task(alias='logs')
def docker_logs(name):
    """
    Get docker container logs.
    """
    get_fn()('docker logs %s' % name)
