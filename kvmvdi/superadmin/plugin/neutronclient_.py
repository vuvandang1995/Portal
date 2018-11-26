from superadmin.plugin import opsutils
from neutronclient.v2_0 import client as client

class neutron_():
    def __init__(self, ip, token_id, project_name, project_domain_id):
        self.auth = v3.Token(auth_url="http://"+ip+":5000/v3", token=token_id, project_domain_id=project_domain_id, project_name=project_name, reauthenticate=False)
        self.sess = session.Session(auth=self.auth)
        self.neutron = client.Client(session=self.sess)
    
    def free_ips(self, ip_net):
        total_ips = neutron.show_network_ip_availability(network=ip_net)['network_ip_availability']['total_ips']
        used_ips = neutron.show_network_ip_availability(network=ip_net)['network_ip_availability']['used_ips']
        return total_ips-used_ips