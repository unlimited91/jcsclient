
from jcsclient import exception
from jcsclient import utils
from jcsclient import help
import ast

def populate_params_from_cli_args(params, args):
    """After the argparser has processed args, populate the
       params dict, processing the given args.

       param params: a dict to save the processed args

       param args: Namespace object where args are saved

       returns: None
    """
    if not isinstance(args, dict):
        args = vars(args)
    for arg in args:
        key = utils.underscore_to_camelcase(arg)
        if arg == 'port' and args[arg] :
            params['IpPermissions.1.FromPort'] = args[arg]
            params['IpPermissions.1.ToPort'] = args[arg]
        elif isinstance(args[arg], list):
            if key=="IpPermissions" :
                ### To match fromat of IpPermissions API
                push_ip_permissions(params, key, args[arg])
            else:
                push_indexed_params(params, key, args[arg])
        elif args[arg]:
            params[key] = args[arg]




def push_ip_permissions(params, key, vals):
    ## Creating a new arg parse to check All related values are there
    ## Not an optimized way
    indx = 1
    for val in vals:
        val = val[1:-1]
        val = ast.literal_eval(val)
        required = ('FromPort', 'ToPort', 'IpProtocol', 'IpRanges')
        if set(required).issubset(val) :
            params[key+ '.' + str(indx)+'.FromPort'] = val['FromPort']
            params[key+ '.' + str(indx)+'.ToPort'] = val['ToPort']
            params[key+ '.' + str(indx)+'.IpProtocol'] = val['IpProtocol']
            cidr_indx = 1
            for cidr in val['IpRanges'] :
                if 'CidrIp' in cidr :
                    params[key+ '.' + str(indx)+'.IpRanges.'+str(cidr_indx)+'.CidrIp'] = cidr['CidrIp']
                else :
                    msg = help.ERROR_STRING
                    msg =msg+'\njcs: error: unsupported value: '+str(val)
                    raise ValueError(msg)                
                cidr_indx +=1
            indx += 1 
        else:
            msg = help.ERROR_STRING
            msg =msg+'\njcs: error: unsupported value: '+ str(val)
            raise ValueError(msg)



def push_indexed_params(params, key, vals):
    # Naive way to check plural, but works
    if key[-1] == 's':
        key = key[:-1]

    idx = 1
    for val in vals:
        elements = val
        #pdb.set_trace()
        temp_key = key + '.' + str(idx)
        idx += 1
        # This is for cases like --filter 'Name=xyz,Values=abc'
        if val.find(',') != -1:
            elements = val.split(',')
            for element in elements:
                if element.find('=') != -1:
                    parts = element.split('=')
                    if len(parts) != 2:
                        msg = 'Unsupported value ' + element + 'given in request.'
                        raise ValueError(msg)
                    element_key, element_val = parts[0], parts[1]
                    key = key + '.' + element_key
                    params[element_key] = element_val
                else:
                    msg = 'Bad request syntax. Please see help for valid request.'
                    raise ValueError(msg)
        else:
            params[temp_key] = elements

