win_dns
=======

Ansible role which helps to manage DNS records on Windows DNS.

The configuration of the role is done in such way that it should not be
necessary to change the role for any kind of configuration. All can be done
either by changing role parameters or by declaring completely new configuration
as a variable. That makes this role absolutely universal. See the examples below
for more details.

Please report any issues or send PR.


Examples
--------

```yaml
---

- name Example of how to add A record
  hosts: dc.example.com
  gather_facts: no
  become: no
  vars:
    win_dns_zone: example.com
    win_dns_name: test
    win_dns_type: A
    win_dns_value: 1.2.3.4
  roles:
    - win_dns

- name Example of how to add A record with TTL
  hosts: dc.example.com
  gather_facts: no
  become: no
  vars:
    win_dns_zone: example.com
    win_dns_name: test
    win_dns_ttl: 300
    win_dns_type: A
    win_dns_value: 1.2.3.4
  roles:
    - win_dns

- name Example of how to add A record with automatic PTR record
  hosts: dc.example.com
  gather_facts: no
  become: no
  vars:
    win_dns_zone: example.com
    win_dns_name: test
    win_dns_ttl: 300
    win_dns_type: A
    win_dns_value: 1.2.3.4
    win_dns_autoptr: yes
  roles:
    - win_dns

- name Example of how to add CNAME record
  hosts: dc.example.com
  gather_facts: no
  become: no
  vars:
    win_dns_zone: example.com
    win_dns_name: testing
    win_dns_type: CNAME
    win_dns_value: test.example.com
  roles:
    - win_dns

- name Example of how to add PTR record
  hosts: dc.example.com
  gather_facts: no
  become: no
  vars:
    win_dns_zone: 3.2.1.example.com
    win_dns_name: 4
    win_dns_type: CNAME
    win_dns_value: test.example.com
  roles:
    - win_dns

- name Example of how to remove record
  hosts: dc.example.com
  gather_facts: no
  become: no
  vars:
    win_dns_zone: example.com
    win_dns_name: test
    win_dns_type: A
    win_dns_value: 1.2.3.4
    win_dns_state: absent
  roles:
    - win_dns

- name Example of how to manage multiple records at once
  hosts: dc.example.com
  gather_facts: no
  become: no
  vars:
    # Allow to manage PTR records automatically
    win_dns_autoptr: yes
    # List of records to manage
    win_dns_records:
      - zone: example.com
        name: test
        type: A
        value: 1.2.3.4
      - zone: example.com
        name: testing
        type: CNAME
        value: test.example.com
        state: absent
  roles:
    - win_dns
```

In order to run the playbook, you have to make WinRM working on the machine from
where you run Ansible. It usually requires latest version of
`requests-kerberos`:

```shell
pip install requests-kerberos
```

Then you can run it like this:

```shell
ansible-playbook \
  -i dc.example.com, \
  -e "{ \
    ansible_connection: winrm, \
    ansible_port: 5986, \
    ansible_user: ansible@EXAMPLE.COM, \
    ansible_winrm_transport: kerberos, \
    ansible_winrm_server_cert_validation: ignore, \
    ansible_password: myt0ps3cr3tp4ssword }" \
  ./site.yaml
```


Role variables
--------------

List of variables used by the role:

```yaml
# Zone name (must be provided by the user)
win_dns_zone: null

# Name in the zone (must be provided by the user)
win_dns_name: null

# Default record type (A, AAAA, CNAME, PTR)
win_dns_type: null

# Value of the specific type (must be provided by the user)
win_dns_value: null

# TTL (optional)
win_dns_ttl: null

# Default TTL
win_dns_ttl_default: 3600

# Default state
win_dns_state: present

# Whether to add PTR record automatically for every A record
win_dns_autoptr: no

# Final list of records
win_dns_records:
  - name: "{{ win_dns_name }}"
    type: "{{ win_dns_type }}"
    value: "{{ win_dns_value }}"
    ttl: "{{ win_dns_ttl }}"
    zone: "{{ win_dns_zone }}"
    state: "{{ win_dns_state }}"
```


License
-------

MIT


Author
------

Jiri Tyr
