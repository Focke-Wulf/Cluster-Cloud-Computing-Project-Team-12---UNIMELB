from boto.ec2.connection import EC2Connection as Ec2conn
from boto.ec2.regioninfo import RegionInfo

Ec2_Access = '441c203a11b44748b74eb60d0554a9a9'
Ec2_Secret = '04ff601e290f4970b371fdede46a6101'
Img = '18bba5e4-d266-4209-9dde-2336465f0384'
Key_Pair = 'ccct12'
A_Zone = 'melbourne'

conn = Ec2conn(aws_access_key_id=Ec2_Access,
                     aws_secret_access_key=Ec2_Secret,
                     is_secure=True,
                     region=RegionInfo(name="NeCTAR", endpoint="nova.rc.nectar.org.au"),
                     validate_certs=False,
                     port=8773,
                     path="/services/Cloud")

def create_instances(name):
    conn.run_instances(DEFAULT_IMAGE_ID,
                               key_name=DEFAULT_KEY_PAIR,
							   instance_profile_name=name
                               instance_type='m2.medium',
                               security_groups=['SSH','HTTP'],
                               placement=DEFAULT_PLACE)
							   )

    return map(lambda x: x.instances[0], instance_list)
def deleteInstance(name):
	conn.terminate_instances(instance_ids=name)