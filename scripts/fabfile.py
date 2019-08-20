#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is a sample code, it can install Moodle or any other PHP app

from __future__ import unicode_literals

from datetime import datetime, timedelta
import os
import psutil
#import dotenv
import pyodbc

from fabric.api import *
from fabric.contrib.files import exists
from fabric.operations import sudo

from fabric.network import join_host_strings, normalize
from fabric.state import connections
#from fabric.connection import Connection

# from fabric.main import env


"""
Base configuration
"""
env.hosts = ['site1.example.com','site2.example.com']
env.gateway = 'jumpbox.example.com'
env.project_name = 'scaffold-test'
env.settings = 'production'
env.user = 'fabricprod'
env.password = 'stupidpassword'
env.key_filename = '~/.ssh/id_ed25519'
env.forward_agent = False
env.port = '22'


# This should go to settings.production
env.production_site_domain = 'site1.example.com'
env.production_user = 'testansible'  # this should exists under environments, but ....
env.production_web = 'web1-srv.example.com'  
env.production_db = 'db1-srv.example.com'  


# This should go to settings.staging
env.staging_user = 'fabricdeploy'  # this should exists under environments, but ....


# This should go to settings.development
env.development_user = 'fabricdev'  # this should exists under environments, but ....


# Sort of global variables

# @TODO: 
# This should be bend per env [ dev | production | staging ]
env.site_domain = env.production_site_domain
env.site_path = '/var/www/vhosts/%(site_domain)s' % env
env.site_permissions = '2770'
env.site_db_type = 'mysqli'  # [ mysqli | postgres | mssql ] ; defined for - $CFG->dbtype    = 'mysqli';
env.site_db_host = 'localhost' 
#env.site_db_host = ''
#env.site_db_port = '3306'
env.site_db_port = '5432'
env.site_db_persistent = 0
env.site_db_name = 'site1'
env.site_db_user = 'site1-user'
env.site_db_password = 'thisishiddenpassword'
env.site_db_prefix = 'why_'
env.branch = 'master'
env.tag = ''
env.repo = 'ssh://repo.example.com/fork/project.git'
env.repo_dir = env.site_path + '/httpdocs'
env.repo_upstream = 'ssh://repo.example.com/core/project.git'
env.site_data = env.site_path + '/moodledata'
env.site_config = 'config.php'
env.site_admin = 'admin'
env.site_password = 'testingdeployment'
env.site_email = 'noreply@example.com'
env.site_short_name = 'Scaffold deployment'
env.site_full_name = 'Scafold deployment testing full site name'
env.site_lang = 'en'

"""
Environments
"""
env.timeout = 3600


def sudo_run(*args, **kwargs):
    if env.use_sudo:
        sudo(*args, **kwargs)
    else:
        run(*args, **kwargs)


# @TODO:
# def environment():
#     envars = dotenv.load_dotenv(
#         os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
#     )
#


def production():
    """
    Work on production environment
    """
    env.settings = 'production'
    master()


def preheat():
    """
    Work on preheat environment
    """
    env.settings = 'preheat'


def staging():
    """
    Work on staging environment
    """
    env.settings = 'staging'
    release()


def development():
    """
    Work on development environment
    """
    env.settings = 'development'


# env.hosts = ['$(staging_domain)']
# env.user = '$(staging_user)'
# env.s3_bucket = '$(staging_s3)'


def testing():
    """
    Work on testing environment - disposable build, run automated tests, provide results and destroy
    """
    env.settings = 'testing'


"""
Branches
"""
def master():
    """
    Work on master - production branch.
    """
    env.branch = 'master'


def release():
    """
    Work on release - uat branch.
    """
    env.branch = 'stable'


def integration():
    """
    Work on integration - development branch.
    """
    env.branch = 'integration'


def branch(branch_name):
    """
    Work on any specified branch.
    """
    env.branch = branch_name


# Check host
def host_type():
    run('uname -s')


def install_packages():
    """ Install a bare minimum LAMP stack """
    run('apt-get -y -qqq install fabric')


"""
Commands - setup
"""


def setup_info():
    run('uname -a')


def setup_directories():
    """
    Create directories necessary for deployment and clone the site repo
    """
    if not exists(env.site_path):
        run('mkdir -p %(site_path)s' % env)

        with cd(env.site_path):

            # details: https://docs.moodle.org/35/en/Installing_Moodle
            run('git clone ' + env.repo + ' ' + 'httpdocs')
            run('mkdir logs')
            run('mkdir moodledata')


        # Set a branch
        with cd(env.repo_dir):
            # If this throws exception it means there is no branch master in repo
            run('git checkout ' + env.branch)

            # Fix missing branch - pwn da forked repo (thanks Mr.A for forking)
            # @TODO: add condition to check if master exists or not (OMG)
            if env.branch == 'master':
                # run('git branch master') # creates master branch
                run('git checkout master')
                run('git push --set-upstream origin master')


        # run('ln -s %(log_path)s %(path)s/logs' % env) # Extend this for moodledata we suppose to clean that up
    else:
        with cd(env.path):
            # @TODO: make this little bit more clever, like scrap config and provide DB name i.e.
            run('ls -l')
            print('directory exists')
            exit()


def install_requirements():

   if exists(env.repo_dir + '/package.json'):
        run('NODE_ENV=' + env.settings + ' npm install ')


    # @TODO: use composer properly; integrate with phpunit tests - https://getcomposer.org/doc/03-cli.md#install-i
    elif exists(env.repo_dir + '/composer.json'):

        # @TODO: --dev vs --no-dev no other environments? Resolve handling of dependencies (all except production is --dev ?)
        run('composer install --dry-run --no-progress --lock')
        # if exists(env.repo_dir + '/node_modules'):
        #     return True
        # else:
        #     print("Can't install npm dependencies")
        #     return False

    else:
        print("Site doesn't have a have requirements, we're good to go")


def install_site():

    with cd(env.repo_dir):
        run('php ' + env.repo_dir + '/admin/cli/install.php'
            ' --lang=' + env.site_lang +
            ' --chmod=' + env.site_permissions +
            ' --wwwroot=' + env.site_path +
            ' --dataroot=' + env.site_data +
            ' --non-interactive'
            ' --adminuser=' + env.site_admin +
            ' --adminpass=' + env.site_password +
            ' --adminemail=' + env.site_email +
            ' --agree-license'
            ' --fullname="' + env.site_full_name + '"'
            )

def install_db():
    """
    Installs Moodle using install.php which fails as it's generating the config.php file,
    but in our case were're generating the file either in config_php function

    :return: boolean
    """
    with cd(env.repo_dir):
        run('php ' + env.repo_dir + '/admin/cli/install_database.php'
            ' --lang=' + env.site_lang +
            ' --adminuser=' + env.site_admin +
            ' --adminpass=' + env.site_password +
            ' --adminemail=' + env.site_email +
            ' --agree-license'
            ' --shortname="' + env.site_short_name + '"'
            ' --fullname="' + env.site_full_name + '"'
            )


def config_php():
    """
    This horrible thing is only for testing purposes at the end we will use .env file
    :return:
    """

unset($CFG);
global $CFG;
$CFG = new stdClass();

$CFG->debug = 32767;
$CFG->debugdisplay = 1;

$CFG->dbtype    = '%s'; // '{env.site_db_type}';
$CFG->dblibrary = 'native';
$CFG->dbhost    = '%s'; // '{env.site_db_host}';
$CFG->dbname    = '%s'; // '{env.site_db_name}';
$CFG->dbuser    = '%s'; // '{env.site_db_user}';
$CFG->dbpass    = '%s'; // '{env.site_db_password}';
$CFG->prefix    = 'mdl_';
$CFG->dboptions = array (
  'dbpersist' => %s, // {env.site_db_persistent},
  'dbport' => '%s', // '{env.site_db_port}',
  'dbsocket' => '',
);

$CFG->wwwroot   = '%s'; // '{env.site_domain}';
$CFG->dataroot  = '%s'; // '{env.site_data}';
$CFG->admin     = '%s'; // '{env.site_admin}';
$CFG->directorypermissions = '%s'; // {env.site_permissions};

$CFG->noreplyaddress = '%s'; // '{env.site_email}';
$CFG->emailonlyfromnoreplyaddress = true;
$CFG->noemailever = true;

require_once(dirname(__FILE__) . '/lib/setup.php');
""" % (env.site_db_type,
       env.site_db_host,
       env.site_db_name,
       env.site_db_user,
       env.site_db_password,
       env.site_db_persistent,
       env.site_db_port,
       env.site_domain,
       env.site_data,
       env.site_admin,
       env.site_permissions,
       env.site_email
       )
    return output

def site_config():
    """
    Writes localy config.php and transfers destination server

    :return: boolean
    """

    with cd(env.repo_dir):
        with open(env.site_config, mode='w+') as config:
            config.write(config_php())

        # Copy generated file to remote location
	# 
	# config is for now generated in local folder from where you fire
	# up this script. Different uscase. User rather .env
        put('config.php', env.repo_dir + '/config.php')


def pull_upstream():
    with cd(env.repo_dir):
        run('git checkout master')
        run('git pull ' + env.repo_upstream + ' ' + env.branch)
        run('git add .')
        run('git commit -a \'Merge from upstream add timestamp and some info here in fabfile\'')
        run('git push origin master')


"""
    Moodle / specific functions and possibly tasks
    
    @TODO: integrate more moodle specific things
    https://docs.moodle.org/28/en/Administration_via_command_line
"""

@task
def maintenance_enable():
    with cd(env.repo_dir):
        run('php admin/cli/maintenance.php --enable')

@task
def maintenance_disable():
    with cd(env.repo_dir):
        run('php admin/cli/maintenance.php --disable')


#@task
def purge_caches():
    run('php admin/cli/purge_caches.php')


#@task
def upgrade():
    """
    Upgrade tries to upgrade the site, this one is very simple.

    :return:
    """
    with cd(env.repo_dir):
        maintenance_enable()
        run('git pull')
        # You may want to run migration first
        # https://docs.moodle.org/35/en/Database_transfer
        run('php admin/cli/upgrade.php')
        maintenance_disable()


def setup_db():
    """
    Creates the required user and database on remote node. This is using pyodbc to create the DB connection.
    @TODO: you can hook this to IAM or even AD/ADFS or where ever you want.

    :return:
    """
    return True


@task
def check_db():
    """
    Running moodle admin cli, it's not fixing the tables by default

    @TODO: add condition which will check site_db_type and only performs action over mysql

    :return: boolean
    """
    with cd(env.repo_dir):
        run('php admin/cli/mysql_engine.php --engine=InnoDB')
        run('php admin/cli/mysql_compressed_rows.php --list')
        #run('php admin/cli/mysql_compressed_rows.php --fix')


def reset_password():
    """
    Replace this script with something what can run from cmd line without user interaction.
    @TODO: PHP devs are just ...... clever.

    :return: FAIL
    """
    with cd(env.repo_dir):
        run('php admin/cli/reset_password.php')


def sanitize_data():
    """
    This suppose to be a separate 'module/script' doing sanitization, by default this should connect to db and
    do the magic over the mdl_user table

    For now blank function, we don't want to use db connections from python.
    @TODO: finish this function; send query to sanitize user data use pyodbc

    :return: boolean
    """
    return True


def replace_script():
    """
    This runs default moodle script if it's present when it's not it doesn't care at all. We can't use it as it requires
    command line interaction ... not always, but it's not always present. Same as reset_password.

    :return: boolean
    """
    with cd(env.repo_dir):
        run('php admin/cli/replace.php --search=' + env.production_site_domain + ' --replace=' + env.site_domain)

    return False


def copy_db_from_production():
    """
    Copy DB backup from production server. This copy the file to webnode we're currently operating on, but that's not
    always the same machine with DB.

    This can't fit/serve all, only as a code sample

    @TODO: check backup size before we start copying

    :return: boolean
    """

    # with Connection(host=env.staging_db, user=env.staging_user, port=env.staging_port, connect_timeout=30) as c:
    #     c.run('echo "fabric trix" > /tmp/hereIgo')
    #     c.get('/tmp/hereIgo')

    # read dbhost value from the config to get the ip of DB server
    #run('grep -i dbhost /var/www/vhosts/' + env.site_domain + '/httpdocs/config.php')

    # @TODO: get the last file from the folder with same dbname in filename .... pretty cool
    #run('rsync --delete -avhP -e "ssh -l ' + env.production_user + ' -p22" ' + env.production_user + '@' + env.production_db + ':/mnt/backups/test.tgz /tmp/')

    mytime = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')

    with cd(env.site_path):
        if not exists(env.site_path + '/transfer'):
            run('mkdir -p ' + env.site_path + '/transfer')

        run('rsync --delete -avhP -e \'ssh -l ' + env.production_user + ' -p22\' '
            + env.production_user + '@' + env.production_db +
            ':/var/www/backups/' + env.site_db_name + '-' + mytime + '.sql.gz /tmp/')

        # run('rsync -avhP '
        #     '-e "ssh -p' + env.port + ' -l ' + env.production_user + '" '
        #     '--files-from=<(find -ctime -1 -type -f -iname "*.sql.gz") ' + env.production_user + '@' + env.production_db +
        #     ':/var/www/backups/ ' + env.site_path + '/transfer')


def copy_to_db_server():
    """
    This is PoC workaround to get around the yubikey auths

    :return: boolean
    """
    run('rsync --delete -avhP -e "ssh -l ' + env.production_user + ' -p22" '
        + env.site_path + '/transfer/' + env.site_db_name + mytime + '.sql.gz'
        + env.production_user + '@' + env.production_db +
        ':/tmp/' + env.site_db_name + mytime + '.sql.gz')


def import_db_on_db_server():
    """
    :return: boolean
    """
    return False


def sync_moodledata_from_production():
    """
    :return: boolean
    """
    run('rsync --delete -avhP -e \'ssh -l ' + env.production_user + ' -p2222\' '
        + env.production_user + '@' + env.production_web +
        ':/var/www/vhosts' + env.production_site_domain + '/filedir '
        + env.site_path + '/moodledata/filedir')


def get_file_size(file_path):
    """
    Returns file size in bytes of provided file, expects absolute path.
    docs url: https://docs.python.org/3/library/os.html#os.lstat

    :param file: string (absolute path)
    :return: int
    """
    return os.path.getsize(file_path)


def get_dir_size(dir_path):
    """
    Returns size of the directory in bytes

    :param dir: string (absolute dir path)
    :return: int
    """
    return 1


def get_free_space(path):
    """
    Returns free space of requested mount_point using df

    @TODO: if on Python ≥3.3, there's shutil.disk_usage(path)
    or https://psutil.readthedocs.io/en/latest/#psutil.disk_usage

    :param path: string (absolute path)
    :return: int
    """
    # to use psutil you must run fab on server not on your local machine - maybe move few parts to helper server scripts
    #psutil.disk_usage(path)

    # returns the block device where the file exists
    find_partition = run("findpart() { [ -e " + path + " ] && df -P " + path +
                         "  | awk '/^\/dev/ {print $1}' || echo \"" + path + " not found\"; }")

    # returns free space on requested partition
    free_space = run("df -Tl --type btrfs --type ext4 --type ext3 --type ext2 --type vfat --type iso9660 " + find_partition +
            "| awk {'print $1,$5'} | sed -e's/%//g' | grep '\/dev\/'")

    return free_space


def get_threshold():
    """
    Returns just 100MB in bytes

    # @TODO: move to constant
    :return: int (bytes)
    """
    return 100 * 1024 * 1024  # 100MB


def check_space_before_copy(source_path, dest_path):
    """
    Checks if we can copy the file or directory from source to destination, it's trying to find out where on what drive
    is the destination path and check if we have enough space before copy.

    :param source_path: source file or directory we want to copy
    :param dest_path: destination directory within to copy file or directory
    :return: int (free space in bytes)
    """
    free_space = get_free_space(dest_path) - get_file_size(source_path)

    THRESHOLD = get_threshold()

    if free_space <= (THRESHOLD * 5):
        print('Critical lack of free space: you\'re below 500MB if you try to copy operation aborted')
        return 0

    elif free_space >= (THRESHOLD * 10):
        return free_space


#@task
def refresh():
    """
    This function is little bit tricky, we have to determine how we do the refresh basically it should have two states:

    refresh_backup
    refresh_restore

    :return:
    """

    copy_db_from_production()

    # @TODO: Lines below not yet tested
    #sync_moodledata_from_production()
    #copy_to_db_server()
    #import_db_on_db_server()
    #run_replace_script
    #sanitize_user_data
    #verify_healthcheck

    return False


#@task
def testme():
    """
    For testing purposes only - call function you like to test
    :return:
    """
    copy_db_from_production()


@task
def setup():
    """
    Setup a fresh site (there is not a site on vhosts so we will first create the new directory structure for required
    domain. 

    Does NOT perform the functions of deploy().
    """
    require('settings', provided_by=[production])  # this calls a function as a provider
    require('branch', provided_by=[master])  # this calls a function as a provider

    # Creates /var/www/$site/{httpdocs,logs,moodledata} - clones repo
    setup_directories()

    # Install additional dependencies - site or environment specific (*.json, *.yml, *.txt / production, development..)
    #install_requirements()

    # Generates config.php for Totara (credentials must exists - this can be extended as different task)
    site_config()

    # Installs the Totara - creates tables, generates basic moodledata (use install when you have a config.php
    # @TODO: related to install_site and config_php and install_db - read notes
    #install_site()
    install_db()


@task
def deploy():
    """
    Deploy the latest version
    """
    # Push changes to repository
    # local("git push origin master")
    if exists(env.repo_dir):
        with cd(env.repo_dir):
            # Fetch & Merge from the remote repo
            run('git checkout ' + env.branch)

            if env.branch == run('git rev-parse --abbrev-ref HEAD --'):
                run('git pull ' + env.repo)
                #run('git pull origin master')

            else:
                print("your repo contains uncommited changes, can't swap the branch")
                exit(0)

    else:
        print("Site path doesn't exists: " + env.site_path)


@task
def shiva_the_destroyer():
    """
    Destroy the project usually for testing purposes only
    :return: epicfail if you use it on wrong project / env
    """
    if exists(env.site_path):
        run('ionice -c3 rm -rf ' + env.site_path)
        return True
    else:
        print("Site path doesn't exists " + env.site_path)
        return False
