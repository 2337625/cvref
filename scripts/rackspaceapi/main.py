#!/usr/bin/env python3

from os import getenv
from dotenv import load_dotenv, find_dotenv
import pathlib
import json
import datetime
from rackspace import connection
from pprint import pprint
import csv

# Load .env file from current directory
load_dotenv(find_dotenv())

# Credentials from .env
api_user = getenv('username')
api_key = getenv('api_key')
api_region = getenv('region')

# Default timestamps
ts = datetime.datetime.now()
ts_iso = datetime.date.isoformat(ts) # iso'YYYY-mm-dd'

# Output file
output_file = "test.log"

# Dictonary storing returned json of servers
servers = dict()

# Stores the 'largest server' with most fields, this is used to build final CSV headers, variable is used within
# normalize_server_list function during iterations
most_fields = dict()
most_fields = {'none': 0}

# Debug output / prints 'debug messages'
VERBOSITY = True
DETAILED = True


def printer(message):
    """ Helper to print debug message when VERBOSITY is True """
    if VERBOSITY:
        pprint(message)


def connect():
    """
    Connect to rackspace using connection object
    :return: connection object
    """
    return connection.Connection(username=api_user,
                                api_key=api_key,
                                region=api_region)

def file_downloaded(filename):
    """
    Checking if file is downloaded in current directory

    @TODO: modify function to accept path as second argument

    :param filename:
    :return: boolean
    """
    fc = pathlib.Path(filename)
    if fc.is_file():
        return True
    else:
        return False


def get_server_list():
    """
    Returns list of server from provider

    :return: dict
    """

    if file_downloaded(output_file):
       server_list = load_server_list_json()
       printer('Server list loaded from JSON')

    #server_list = load_server_list_json()
    #printer('Server list loaded from JSON')

    else:
        # Connect to RS
        rsconn = object
        rsconn = connect()

        # Store the JSON response from list_servers
        printer("Fetching server list from Rackspace...")

        server_list = rsconn.list_servers(detailed = DETAILED)
        save_server_list_json(server_list)

        printer('Server list loaded via API call')

    return server_list


def save_server_list_json(server_list):
    """
    Saving the JSON output in file to reduce api calls

    :return: dictionary
    """

    with open(output_file,"w+") as f:
        json.dump(server_list, f)

    return server_list


# Broken fix first
def export_server_list_json(server_list, filename):
    """
    Saving the JSON output in file to reduce api calls
    @TODO: figure out why it's overriding output_file

    :return: dictionary
    """

    with open(filename,"w+") as f:
        json.dump(server_list, f)

    return server_list


def load_server_list_json():
    with open(output_file) as f:
        jsn = json.load(f)

    return jsn


# Deprecated - @TODO: delete after proper testing; use get_server_list()
def load_servers():
    server_list = get_server_list()
    return server_list


def normalize_server_list_json(server_list):
    """
    exports the list of servers with most important
    details.

    sample:

    [name]
        [summary]
        name=name   # RS name in webui not hostname of server mylearning-omg
        flavor='cloud 100 , 1gb , 1 cpu lol' # read below
        region=region
        hostname=hostname # @TODO: determine from IP
        public_ipv4=public_ipv4 # mandatory ip (other are access,interface)
        public_ipv6=public_ipv6 # mandatory ip
        private_v4=private_v4 # mandatory ip

        status=status # RS web status ACTIVE/RESTARTING..
        state=state # 1 # (int)
        progress=progress # 100 #'(int)%'
        vm_state=vm_state # 'active' / ??

        updated=updated
        created=created
        lanuched_at=launched_at # default None
        terminated_at=terminated_at

        id=id
        host_id=host_id
        tenant_id=tenant_id
        image=Munch[0]['id'] #
        user_id=user_id # user accessing the api?

        ## All above is present for each VM
        ## Volumes if exists (/dev/sdb onwards) some instances has /dev/sdba visible
        volumes=[
            volume_type=volume_type # SATA / SSD
            drive=volumes[{attachments : [{'device':'/dev/xvda'}] # xvda appears on compute node i..e
        ]

        task_state=task_state
        updated=updated
        created=created
        terminated_at=terminated_at
        power_state=power_state
        vm_state=vm_state
        host_id=host_id
        id=id # it's different on RS id vs host_id
        project_id=project_id


        [details]
        name=volumes['attachments']['name']
        volume_status=volumes['attachments']['status']
        size=volumes['attachments']['size']
        security_groups=security_groups

        [properties]

        [volumes]
        volumes=volumes[{'attachments'}:
            ['attachment_id', server_id, volume_id, id, device]
            display_name=display_name #hostname?
            name=name
            status=status
            size=size
            device=device # /dev/xvd[abcd]
            created_at=created_at
            properties=properties['volume_image_metadata] # return dict
            volume_type=volume_type # SATA or SSD
            metadata=metadata['storage-node'] #storage node id?
            location=location['region_name'] #


        [metadata]
        # contains various errors like nova_agent
        addresses=addressess['galaxy','private','public']
        network='galaxy'
            [access]
            ipv4=accessIPv4
            ipv6=accessIPv6
            [public]
            ipv4=munch({'addr'})
            [private]
            ipv4=munch({'addr'})

    :return:
    """
    myservers = dict()
    global most_fields
    #most_fields = dict()
    #most_fields = {'none': 0} # too lazy to make complex condition

    for server in server_list:
        """
            Iterate over servers and cherry pick wanted variables/data
        """
        myservers[server['name']] = {
            "name": server['name'],
            "flavor_id": server['flavor']['id'],
            "flavor_name": str(server['flavor']['name']),
            "image_id":  server['image']['id'],
            "region_name":  server['location']['region_name'],
            "project_id":  server['location']['project']['id'],
            "access_ip4": server['accessIPv4'],
            "access_ip6": server['accessIPv6'],
            "interface_ip4": server['interface_ip'],
            "created_at": server['created_at'],
            "updated_at": server['updated'],
            "terminated_at": server['terminated_at'],
            "status": server['status'],
            "power_state": server['power_state'],
            "provider_ip_zone": server['RAX-PUBLIC-IP-ZONE-ID:publicIPZoneId'],
            "host_id": server['host_id'],
            "id": server['id'],
            "tenant_id": server['tenant_id']
        }

        # @TODO: move this to function add checks when some fields are missing
        if len(server['volumes']) > 0:
            i = 0
            for vol in server['volumes']:
                myservers[server['name']].update({
                    "vol" + str(i) + '_id': vol['id'],
                    "vol" + str(i) + '_name': vol['name'],
                    "vol" + str(i) + '_status': vol['status'],
                    "vol" + str(i) + '_size': vol['size'],
                    "vol" + str(i) + '_created_at': vol['created_at'],
                    "vol" + str(i) + '_updated_at': vol['updated_at'],
                    "vol" + str(i) + '_type': vol['volume_type'],
                    "vol" + str(i) + '_device': vol['device'],
                    "vol" + str(i) + '_storage_node': vol['metadata']['storage-node'],
                    #"vol" + str(i) + '_storage_mode': vol['metadata']['attached_mode'],
                    "vol" + str(i) + '_server_id': vol['attachments'][0]['server_id'],
                    "vol" + str(i) + '_attachment_id': vol['attachments'][0]['attachment_id'],
                    "vol" + str(i) + '_host_name': vol['attachments'][0]['host_name'],
                    "vol" + str(i) + '_volume_id': vol['attachments'][0]['volume_id'],
                    "vol" + str(i) + '_az': vol['availability_zone']
                })
                i = i + 1

        else:
            myservers[server['name']].update({
                "additional_storage": 0
            })

        if int(len(myservers[server['name']])) > int(list(most_fields.values())[-1]):
            most_fields = dict()
            most_fields[server['name']] = int(len(myservers[server['name']]))

        # @TODO: add iteration via server['metadata'] when len > 0
        # @TODO: add iteration via server['properties'] when len > 0
        # @TODO: add iteration via server['addresses'] and dynamically add 'networks - Galaxy, public, private ..'

    return myservers


def save_server_list_csv(server_list):
    """
    Save normalized server list to csv

    :param server_list:
    :return:
    """
    global most_fields

    # Get 'key/server_name' with most 'columns'
    key = list(most_fields.keys())[-1]
    # Get record from server_list to provide headers
    srv = server_list[str(key)]
    # Create headers for CSV
    headers = list(srv.keys())

    with open('new-servers.csv', 'w', newline='') as of:
        writer = csv.writer(of)
        writer.writerow(headers)

        for server in server_list.values():
            server_values = list(server.values()) # Y
            writer.writerow(map(str, server_values))


def main():
    try:
        printer("Starting main ...")
        servers = normalize_server_list_json(get_server_list())
        pprint(servers)
        save_server_list_csv(servers)

    except Exception as e: print(e)


if __name__ == "__main__":
    main()
