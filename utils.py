from exceptions import InvalidPortError, InvalidGroupError
import sys

def validate_port(port):
    """ Validate a port number

        Returns
        -------
        port : int
            The port number.
            
        Raises
        ------
        InvalidPortError
            If the port is not a number or is negative.
    """
    try: 
        port = int(port)
    except:
        raise InvalidPortError(f"{port} is not a valid value for port")
        
    if port < 0:
        raise InvalidPortError("Port must be a number greater than zero")
    
    return port

def validate_group(group):
    """ Validate a telegram group name.

        Returns
        -------
        group : str
            The name of the group.
            
        Raises
        ------
        InvalidGroupError
            If the group is not a string or the name is no in the list.
    """
    if not isinstance(group, str):
        raise InvalidGroupError("Group must be of type str.")
    
    group = group.lower()
    valid_groups = list(get_valid_groups().keys())
    
    if group not in valid_groups:
        raise InvalidGroupError(f"{group} is not a valid group name")

    return group

def get_valid_groups(groups_file="./chats.txt"):
    """ Get a dictionary of telegram groups with its respective id.
    
        Returns
        -------
        valid_groups : dict
            Dictionary with group names as keys and ids as values.
    """
    valid_groups = {}
    
    with open(groups_file, "r") as fh:
        for line in fh.readlines():
            chat_info = line.split(",")
            group_name = chat_info[0].lower()
            group_id = chat_info[-1].rstrip()
            valid_groups[group_name] = group_id
    
    return valid_groups


def get_ftp_login_data(ftp_file="./ftp.txt"):
    """Get the user and password for the ftp server.

        Parameters
        ----------
        ftp_file : str
            Path to the file containing the data.

        Returns
        -------
        user : str
            The username of the ftp server
            
        password : str
            The password of the ftp.
    """
    with open(ftp_file, "r") as fh:
        lines = fh.readlines()
        user = lines[0].rstrip()
        password = lines[-1].rstrip()

    return user, password

def get_argv_data(argvs):
    """ Get port number and grop name from passed argvs

        Parameters
        ----------
        argvs : list
            List with the argvs
            
        Returns
        -------
        port : int
            The port number
        
        group : str
            Name of the telegram group.
    """
    
    if len(sys.argv) == 3:
        port = validate_port(sys.argv[1])
        group = validate_group(sys.argv[2])
    elif len(sys.argv) == 2:
        port = validate_port(sys.argv[1])
        group = "RACM"
    else:
        port = 16050
        group = "RACM"
    
    return port, group
    