from fabric.api import env, local, cd, run, settings, sudo

env.use_ssh_config = True
env.hosts = ['root@skylines']


def deploy(branch='master', force=False):
    push(branch, force)
    restart()


def push(branch='master', force=False):
    cmd = 'git push %s:/opt/skylines/src/ %s:master' % (env.host_string, branch)
    if force:
        cmd += ' --force'

    local(cmd)


def restart():
    with cd('/opt/skylines/src'):
        run('git reset --hard')

        # compile i18n .mo files
        manage('babel compile')

        # generate JS/CSS assets
        manage('assets build')

        # do database migrations
        with settings(sudo_user='skylines'):
            sudo('./manage.py migrate upgrade')

        # restart services
        restart_service('skylines-fastcgi')
        restart_service('mapserver-fastcgi')
        restart_service('skylines-daemon')
        restart_service('celery-daemon')


def restart_service(service):
    run('sv restart ' + service)


def manage(cmd):
    with cd('/opt/skylines/src'):
        run('./manage.py %s' % cmd)
