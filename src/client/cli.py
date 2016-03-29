"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mclient` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``client.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``client.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import sys

from client.newcli import common_cli

from client import common
from client import dss


iam_help = {
        'CreateUser                   ' : "[--Email <email>] [--Password <password>] --Name <username>                                           ",
        'DeleteUser                   ' : "[--Id <userid> | --Name <username>]                                                                   ",
        'ListUsers                    ' : "                                                                                                      ",
        'UpdateUser                   ' : "[--Id <userid> | --Name <username>] --NewEmail <email> --NewPassword <newpassword>                    ",
        'GetUser                      ' : "[--Id <userid> | --Name <username>]                                                                   ",
        'GetUserSummary               ' : "[--Id <userid> | --Name <username>]                                                                   ",
        'CreateCredential             ' : "[--Id <userid> | --Name <username>]                                                                   ",
        'DeleteCredential             ' : "[--Id <credentialid> | --AccessKey <accesskey>]                                                       ",
        'GetUserCredential            ' : "[--Id <userid> | --Name <username>]                                                                   ",
        'CreateGroup                  ' : "[--Name  <groupname>] --Description <groupdescription>                                                ",
        'GetGroup                     ' : "[--Id <groupid> | --Name <group>]                                                                     ",
        'DeleteGroup                  ' : "[--Id <groupid> | --Name <group>]                                                                     ",
        'ListGroups                   ' : "                                                                                                      ",
        'AssignUserToGroup            ' : "[--UserId <userid> | --UserName <username>] [--GroupId <groupid> | --GroupName <groupname>]           ",
        'CheckUserInGroup             ' : "[--UserId <userid> | --UserName <username>] [--GroupId <groupid> | --GroupName <groupname>]           ",
        'RemoveUserFromGroup          ' : "[--UserId <userid> | --UserName <username>] [--GroupId <groupid> | --GroupName <groupname>]           ",
        'ListGroupsForUser            ' : "[--Id <userid> | --Name <username>]                                                                   ",
        'ListUserInGroup              ' : "[--Id <groupid> | --Name <groupname>]                                                                 ",
        'UpdateGroup                  ' : "[--Id <groupid> | --Name <groupname>] --NewName <newname> --NewDescription <newdescription>           ",
        'GetGroupSummary              ' : "[--Id <groupid> | --Name <groupname>]                                                                 ",
        'CreatePolicy                 ' : "[--PolicyDocument <policydocument>]                                                                   ",
        'GetPolicy                    ' : "[--Id <policyid> | --Name <policyname>]                                                               ",
        'ListPolicies                 ' : "                                                                                                      ",
        'DeletePolicy                 ' : "[--Id <policyid> | --Name <policyname>]                                                               ",
        'UpdatePolicy                 ' : "[--Id <policyid> | --Name <policyname>] --PolicyDocument  <policydocument>                            ",
        'AttachPolicyToUser           ' : "[--PolicyId <policyid> | --PolicyName <policyname>] [--UserId  <userid> | --UserName  <username>]     ",
        'DetachPolicyFromUser         ' : "[--PolicyId <policyid> | --PolicyName <policyname>] [--UserId  <userid> | --UserName  <username>]     ",
        'AttachPolicyToGroup          ' : "[--PolicyId <policyid> | --PolicyName <policyname>] [--GroupId <groupid> | --GroupName <groupname>]   ",
        'DetachPolicyFromGroup        ' : "[--PolicyId <policyid> | --PolicyName <policyname>] [--GroupId <groupid> | --GroupName <groupname>]   ",
        'GetPolicySummary             ' : "[--Id <policyid> | --Name <policyname>]                                                               ",
        'CreateResourceBasedPolicy    ' : "[--PolicyDocument <policydocument>]                                                                   ",
        'GetResourceBasedPolicy       ' : "[--Id <rbpid> | --Name <rbpname>]                                                                     ",
        'ListResourceBasedPolicies    ' : "                                                                                                      ",
        'DeleteResourceBasedPolicy    ' : "[--Id <rbpid> | --Name <rbpname>]                                                                     ",
        'UpdateResourceBasedPolicy    ' : "[--Id <rbpid> | --Name <rbpname>] --PolicyDocument <policydocument>                                   ",
        'AttachPolicyToResource       ' : "[--PolicyId <policyid> | --PolicyName <policyname>] --Resource <resource>                             ",
        'DetachPolicyFromResource     ' : "[--PolicyId <policyid> | --PolicyName <policyname>] --Resource <resource>                             ",
        'GetResourceBasedPolicySummary' : "[--Id <rbpid> | --Name <rbpname>]                                                                     "
}

vpc_help = {
        'CreateVpc                    ' : "--CidrBlock <cidrBlock>                                                                              ",
        'DeleteVpc                    ' : "--VpcId <vpcId>                                                                                      ",
        'DescribeVpcs                 ' : "[--VpcId.N <vpcId>]                                                                                  ",
        'CreateSubnet                 ' : "--CidrBlock <cidrBlock> --VpcId <vpcId>                                                              ",
        'DeleteSubnet                 ' : "--SubnetId <subnetId>                                                                                ",
        'DescribeSubnets              ' : "[--SubnetId.N <subnetId>]                                                                            ",
        'CreateSecurityGroup          ' : "--VpcId <vpcId> --GroupName <groupName> --GroupDescription <groupDescription>                        ",
        'AuthorizeSecurityGroupIngress' : "--GroupId <groupId> --IpPermissions.N.IpProtocol <protocol> --IpPermissions.N.ToPort <Port> --IpPermissions.N.FromPort <Port> [--IpPermissions.N.IpRanges.N.CidrIp <cidrIp> | --IpPermissions.N.Groups.1.GroupIp <groupId>]                          ",
        'AuthorizeSecurityGroupEgress ' : "--GroupId <groupId> --IpPermissions.N.IpProtocol <protocol> --IpPermissions.N.ToPort <Port> --IpPermissions.N.FromPort <Port> [--IpPermissions.N.IpRanges.N.CidrIp <cidrIp> | --IpPermissions.N.Groups.1.GroupIp <groupId>]                          ",
        'RevokeSecurityGroupIngress   ' : "--GroupId <groupId> --IpPermissions.N.IpProtocol <protocol> --IpPermissions.N.ToPort <Port> --IpPermissions.N.FromPort <Port> [--IpPermissions.N.IpRanges.N.CidrIp <cidrIp> | --IpPermissions.N.Groups.1.GroupIp <groupId>]                          ",
        'RevokeSecurityGroupEgress    ' : "--GroupId <groupId> --IpPermissions.N.IpProtocol <protocol> --IpPermissions.N.ToPort <Port> --IpPermissions.N.FromPort <Port> [--IpPermissions.N.IpRanges.N.CidrIp <cidrIp> | --IpPermissions.N.Groups.1.GroupIp <groupId>]                          ",
  
        'DescribeSecurityGroups       ' : "[--SecurityGroupId.N <securityGroupId>                                                               ",
        'DeleteSecurityGroup          ' : "--SecurityGroupId <securityGroupId>                                                                  ",
        'CreateRoute                  ' : "--DestinationCidrBlock <destinationCidrBlock> --RouteTableId <routeTableId> --InstanceId <instanceId> ",
        'DeleteRoute                  ' : "--DestinationCidrBlock <destinationCidrBlock> --RouteTableId <routeTableId>                          ",
        'CreateRouteTable             ' : "--VpcId <vpcId>                                                                                      ",
        'DeleteRouteTable             ' : "--RouteTableId <routeTableId>                                                                        ",
        'AssociateRouteTable          ' : "--RouteTableId <routeTableId> --SubnetId <subnetId>                                                  ",
        'DisassociateRouteTable       ' : "--AssociationId <associationId>                                                                      ",
        'DescribeRouteTables          ' : "[--RouteTableId.N <routeTableId>]                                                                    ",
        'AllocateAddress            ' : "--Domain <vpc>                                                                                         ",
        'AssociateAddress           ' : "--AllocationId <allocationId> --InstanceId <instanceId>                                                ",
        'DisassociateIpAddress        ' : "--AssociationId <associationId>                                                                        ",
        'ReleaseAddress             ' : "--AllocationId <allocationId>                                                                          ",
        'DescribeAddresses          ' : "[--AllocationId.N <allocationId>]                                                                      ",
}





compute_help = {
        'CreateKeyPair                ' : "--KeyName <keyname>",
        'DeleteKeyPair                ' : "--KeyName <keyname>",
        'ImportKeyPair                ' : "--KeyName <keyname> --PublicKeyMaterial <base64 encoded public key>",
        'UpdateDeleteOnTerminationFlag' : "--volumeId <volumeId> --deleteOnTermination <True|False>",
        'DescribeImages               ' : "[--ImageId.N]                                                                                         ",
        'DescribeInstanceTypes        ' : "[--InstanceTypeId.N]",
        'RunInstances                 ' : "--ImageId <imageId> --InstanceTypeId <instanceTypeId> [--BlockDeviceMapping.N <BlockDeviceMapping>] [--InstanceCount <integer>] [--SubnetId <subnetId>] [--PrivateIPAddress <PrivateIPAddress>] [--SecurityGroupId.N <SecurityGroupId>] [--KeyName <KeyName>]                                                                ",
        'DescribeInstances            ' : "[--InstanceId.N <instanceid> --Filter.N.Name <filtername> --Filter.N.Value <filtervalue>",
        'StopInstances                ' : "[--InstanceId.N <instanceid>] [--Force <True | False>]",
        'StartInstances               ' : "[--InstanceId.N <instanceid>]",
        'RebootInstances              ' : "[--InstanceId.N <instanceid>]",
        'TerminateInstances           ' : "[--InstanceId.N <instanceid>]",
        'DescribeKeyPairs             ' : "",
        'DetachVolume                 ' : "--InstanceId <instance_id> --VolumeId <volume_id> [--Force <True | False>",
        'ShowDeleteOnTerminationFlag  ' : "--volumeId <volume_id>",
        'AttachVolume                 ' : "--InstanceId <instance_id> --VolumeId <volume_id> --Device <device>",
        #'ShowPassword                 ' : "[--Id <userid> | --Name <username>]",
}


def main(argv=sys.argv):
    """
    Args:
        argv (list): List of arguments

    Example usage of 'newcli':
        jcs newcli rds describe-db-instances --instance-identifier mydb
    """

    if argv[1] == 'rds':
        # args = argv[1:] if len(argv) > 2 else ['--help']
        common_cli.generate_cli_output(argv[1:] if len(argv) > 2 else ['rds', '--help'])
        return

    debug = False

    if len(argv) < 3 or argv[1] in ['-h', '--help', 'help']:
        print "Example usage: jcs [--curl|--prettyprint] compute Action=DescribeInstances\n"
        print "               jcs [--curl|--prettyprint] compute 'Action=CreateVolume&Size=1'\n"
        print "               jcs [--curl|--prettyprint] dss <command> [<src-path>] <target-path>\n"
        print "               jcs iam ActionName --Param1 <value> --Param2 <value>"
        print "               jcs iam --help"
        print "               jcs iam ActionName --help"
        print "Service argument can be 'iam', 'rds', 'compute', 'vpc' or 'dss'"
        print "If '--curl' is specified, only curl request input will be"
        print "produced. No request will be made"
        print "If --prettyprint is specified, response of request made will be"
        print "printed using a pretty printer"
        print "DSS <target-path> is the path of the entity you want to address"
        print "It can be just the bucket name, or bucket name followed by object name. Eg. /bucket1/obj2"
        sys.exit(1)

    ## Separate out DSS workflow
    if argv[2].lower() == "dss" or argv[1].lower() == "dss":
        dss.initiate(argv)
        return 0

    if '--debug' in argv:
        argv.remove('--debug')
        debug = True
    elif '-d' in argv:
        argv.remove('-d')
        debug = True

    if '--help' in argv or '-h' in argv or 'help' in argv:
        argv.remove(argv[-1])
        if argv[-1] == 'iam':
            for row in iam_help:
                print row, 'jcs iam ' + row.strip() + ' ' + iam_help[row]
        elif argv[-1] == 'compute':
            for row in compute_help:
                print row, 'jcs compute ' + row.strip() + ' ' + compute_help[row]
        
        elif argv[-1] == 'vpc':
            for row in vpc_help:
                print row, 'jcs vpc ' + row.strip() + ' ' + vpc_help[row]


        else:
            found = False
            for row in iam_help:
                if row.strip() == argv[-1]:
                    found = True
                    print 'Usage:\n'
                    print 'jcs iam ' + row.strip() + ' ' + iam_help[row]
            for row in compute_help:
                if row.strip() == argv[-1]:
                    found = True
                    print 'Usage:\n'
                    print 'jcs compute ' + row.strip() + ' ' + compute_help[row]
            if not found:
                print "Invalid client request. Refer to help using, jcs <service> --help"
        return 0

    try:
        if argv[1] == '--curl' and len(argv) == 4:
            common.curlify(argv[2], argv[3])
        elif argv[1] == '--prettyprint' and len(argv) == 4:
            common.curlify(argv[2], argv[3], False, True, True)
        elif len(argv) == 3 and '=' in argv[2]:
            common.curlify(argv[1], argv[2], False, True)
        elif len(argv) >= 3:
            common.curlify(argv[1], argv[2:], True, True)
        else:
            print "Invalid client request "
            if argv[1] == 'iam':
                print "refer to, jcs iam --help"
            else:
                print "refer to, jcs --help"
    except Exception as e:
        if debug:
            raise
        else:
            #print("{}: {}".format(type(e).__name__, e))
            pass

    return 0
