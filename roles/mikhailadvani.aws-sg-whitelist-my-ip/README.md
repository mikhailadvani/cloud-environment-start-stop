aws-sg-whitelist-my-ip
=========

Role to whitelist the external IP of the machine the code is running on a.k.a. Ansible controller or a custom IP specified as an extra var with support of resetting to the original state or re-compute a changed external IP

Requirements
------------
- Python 2.7
- boto
- AWS access keys with EC2FullAccess privileges

Role Variables
--------------

- AWS_ACCESS_KEY_ID: Access key with EC2FullAccess privileges being set as environment variable as shown in the sample below
- AWS_SECRET_ACCESS_KEY: Corresponding secret access key to AWS_ACCESS_KEY_ID
- EC2_REGION: The AWS region of your infrastructure
- path_to_role: Path to the directory of the role. **Default**: *roles/mikhailadvani.aws-sg-whitelist-my-ip*
- security_groups: The security group rules that should be modified to allow the IP of the controller machine. Supports multiple security groups
    - name: Name of the security group to be updated
    - vpc_id: The id of the VPC of the security group
    - rules: The additional inbound rules to be added from the controller IP. cidr_ip needs to be "{{my_ip}}" which will be resolved dynamically as a pre-task
- access: set/unset/reset. Whether your external IP needs to be added, removed or updated to the security groups mentioned in vars **Mandatory**: *yes*. **Default**: *none*
- my_ip: Optional extra var to whitelist specified IP instead of querying external API myexternalip.com. **Default**: Auto-computed to the external IP of the controller machine 


Example Playbook
----------------

`ansible-playbook aws-sg-whitelist-my-ip.yml -v -e "access=set"`

`ansible-playbook aws-sg-whitelist-my-ip.yml -v -e "access=reset"`

`ansible-playbook aws-sg-whitelist-my-ip.yml -v -e "access=unset"`

    - hosts: localhost
      connection: local
      pre_tasks:
        - include: "{{path_to_role}}/tasks/get_my_ip.yml"
          when: my_ip is not defined and (access == 'set' or access == 'reset')
      environment:
        AWS_ACCESS_KEY_ID: "{{AWS_ACCESS_KEY_ID}}"
        AWS_SECRET_ACCESS_KEY: "{{AWS_SECRET_ACCESS_KEY}}"
        EC2_REGION: "{{EC2_REGION}}"
      roles:
        - {role: aws-sg-whitelist-my-ip}

License
-------

MIT

Author Information
------------------

The role was created in 2016 by [Mikhail Advani](https://github.com/mikhailadvani "Github")

Twitter Handle: [@mikhail_advani](https://twitter.com/mikhail_advani "Twitter")
