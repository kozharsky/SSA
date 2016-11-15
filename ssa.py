#!/usr/bin/python


from troposphere import Template, Ref, Output, Join, GetAtt, Parameter
import troposphere.ec2 as ec2

template = Template()

keypair = template.add_parameter(Parameter(
    "KeyPair",
    Type="String",
    Description="~/keys/kozharsky.pem",
))

# Create a security group
sg = ec2.SecurityGroup('awscli')
sg.GroupDescription = "Allow access to MyInstance"
sg.SecurityGroupIngress = [
    ec2.SecurityGroupRule(
        IpProtocol="tcp",
        FromPort="22",
        ToPort="22",
        CidrIp="0.0.0.0/0",),
    ec2.SecurityGroupRule(
        IpProtocol="tcp",
        FromPort="80",
        ToPort="80",
        CidrIp="0.0.0.0/0",
    )]

template.add_resource(sg)

# Create an instance
instance = ec2.Instance("KInstance")
instance.ImageId = "ami-8504fdea"
instance.InstanceType = "t2.micro"
instance.SecurityGroups = [Ref(sg)]
instance.KeyName = Ref(keypair)

# Add output to template
#template.add_output(Output(
#    "InstanceAccess",
#    Description="Command to use to SSH to instance",
#    Value=Join("", ["ssh -i ", Ref(keypair), " ubuntu@", GetAtt(instance, "PublicDnsName")])
#))

# Add instance to template
template.add_resource(instance)

print template.to_json()





