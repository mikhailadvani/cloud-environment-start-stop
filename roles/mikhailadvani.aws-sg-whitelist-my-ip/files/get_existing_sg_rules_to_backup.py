import sys
import json
from boto.ec2 import EC2Connection

group_name = sys.argv[1]
vpc_id = sys.argv[2]

ec2_connection = EC2Connection()

def get_group_name_from_id(group_id, vpc_id):
    account_number_removed_group_id = '-'.join(group_id.split('-')[:2])
    security_groups = ec2_connection.get_all_security_groups(group_ids=[account_number_removed_group_id], filters={'vpc_id': vpc_id})
    return security_groups[0].name


def jsonify_security_group_rules(rules):
    jsonified_rules = []
    for rule in rules:
        jsonified_rule = {}
        jsonified_rule['proto'] = rule.ip_protocol
        jsonified_rule['from_port'] = rule.from_port
        jsonified_rule['to_port'] = rule.to_port
        for grant in rule.grants:
            sg_rule = jsonified_rule
            if 'sg' in str(grant):
                sg_rule['group_name'] = get_group_name_from_id(str(grant), vpc_id)
            else:
                sg_rule['cidr_ip'] = str(grant)
            jsonified_rules.append(sg_rule)
    return jsonified_rules

def get_security_group_facts():
    security_group = ec2_connection.get_all_security_groups(filters={'group-name': [group_name], 'vpc_id': vpc_id})

    security_group_details = dict()
    security_group_details["name"] = group_name
    security_group_details["description"] = security_group[0].description
    security_group_details["vpc_id"] = vpc_id
    security_group_details["rules"] = jsonify_security_group_rules(security_group[0].rules)

    return json.dumps(security_group_details)

print get_security_group_facts()