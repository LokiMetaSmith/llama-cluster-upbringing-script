import os
import json
import pytest
from jinja2 import Environment, FileSystemLoader

def test_pxe_server_nomad_template():
    """
    Tests that the pxe_server.nomad.j2 template renders correctly with dedicated HTTP port,
    resilience stanzas (restart, reschedule, update), Consul service registration, and check_restart.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.abspath(os.path.join(base_dir, '../../ansible/roles/pxe_server/templates'))

    assert os.path.exists(template_dir), f"Template directory not found: {template_dir}"

    j2_env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True)
    j2_env.filters['to_json'] = json.dumps
    template = j2_env.get_template('pxe_server.nomad.j2')

    context = {
        'pxe_image_cid': 'QmTestHashCID123',
        'pxe_http_port': 8093,
        'cluster_domain': 'local.mesh',
        'nomad_datacenters': ['dc1'],
    }

    result = template.render(context)

    # Check that HTTP port is set to dedicated port 8093 (not default 80)
    assert 'static = 8093' in result, "pxe_server.nomad.j2 must bind the dedicated pxe_http_port (8093)"
    assert 'static = 80\n' not in result, "pxe_server.nomad.j2 should not hardcode port 80"

    # Check for resilience stanzas
    assert 'restart {' in result, "pxe_server.nomad.j2 must include restart stanza"
    assert 'reschedule {' in result, "pxe_server.nomad.j2 must include reschedule stanza"
    assert 'update {' in result, "pxe_server.nomad.j2 must include update stanza"

    # Check for Consul service registration and Traefik mesh tags
    assert 'provider = "consul"' in result, "pxe-http service must specify provider = consul"
    assert 'address  = "${attr.unique.network.ip-address}"' in result, "service must specify host network address"
    assert 'traefik.enable=true' in result, "service must include traefik.enable=true tag for flexible mesh routing"

    # Check for check_restart with grace period
    assert 'check_restart {' in result, "pxe-http check must include check_restart"
    assert 'grace           = "60s"' in result, "check_restart must define a startup grace period"


def test_pxe_boot_ipxe_and_dhcp_templates():
    """
    Tests that dhcpd.conf.j2 and boot.ipxe.j2 render URLs with the dedicated HTTP port.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.abspath(os.path.join(base_dir, '../../ansible/roles/pxe_server/templates'))

    j2_env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True)

    dhcp_template = j2_env.get_template('dhcpd.conf.j2')
    dhcp_result = dhcp_template.render({
        'pxe_interface': 'eth0',
        'pxe_server_ip': '10.0.0.1',
        'pxe_http_port': 8093,
        'pxe_subnet': '10.0.0.0',
        'pxe_netmask': '255.255.255.0',
        'pxe_range_start': '10.0.0.200',
        'pxe_range_end': '10.0.0.240',
        'ansible_default_ipv4': {'address': '10.0.0.1'},
        'ansible_facts': {
            'eth0': {'ipv4': {'address': '10.0.0.1', 'network': '10.0.0.0', 'netmask': '255.255.255.0'}},
            'default_ipv4': {'address': '10.0.0.1', 'network': '10.0.0.0', 'netmask': '255.255.255.0'}
        }
    })
    assert 'http://10.0.0.1:8093/boot.ipxe' in dhcp_result, "DHCP config must serve iPXE URL with pxe_http_port"

    ipxe_template = j2_env.get_template('boot.ipxe.j2')
    ipxe_result = ipxe_template.render({
        'pxe_server_ip': '10.0.0.1',
        'pxe_http_port': 8093,
        'ansible_default_ipv4': {'address': '10.0.0.1'},
        'ansible_facts': {'default_ipv4': {'address': '10.0.0.1'}}
    })
    assert 'set http_port 8093' in ipxe_result
    assert 'http://${server_ip}:${http_port}/live/vmlinuz' in ipxe_result
    assert 'http://${server_ip}:${http_port}/debian' in ipxe_result
