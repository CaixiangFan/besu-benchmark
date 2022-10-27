import openstack
from dotenv import dotenv_values
env = dotenv_values("../caliper-benchmarks/cc.env")


def create_connection():
    return openstack.connect(
        auth_url=env['OS_AUTH_URL'],
        project_name=env['OS_PROJECT_NAME'],
        username=env['OS_USERNAME'],
        password=env['OS_PASSWORD'],
        region_name=env['OS_REGION_NAME'],
        user_domain_name=env['OS_USER_DOMAIN_NAME'],
        project_domain_name=env['OS_PROJECT_DOMAIN_NAME'],
        project_id=env['OS_PROJECT_ID'],
        app_name='bpet',
        app_version='1.0',
    )


def get_nodeaddr(conn, instance_name):
    serverObj = conn.compute.find_server(instance_name)
    serverInfo = conn.compute.get_server(serverObj)
    return serverInfo.addresses['rrg-khazaei-network'][0]['addr']


def run(network_size):
    conn = create_connection()
    for id in range(network_size):
        instance_name = 'besu-'+str(id+1)
        ip = get_nodeaddr(conn, instance_name)
        print('{} {}'.format(instance_name, ip))


if __name__ == "__main__":
    network_size = 8
    run(network_size)
