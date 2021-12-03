from telegramBot.utils.exceptions import InvalidPortError, InvalidGroupError

def validate_port(port):
    """ Validate a port number
    
        Parameters
        ----------
        port : str
            The port number in string format.

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

def validate_group(group, valid_groups):
    """ Validate a telegram group name.
    
        Parameters
        ----------
        group : str
            Name of the group.
            
        valid_groups : list of str
            List with names of valid groups.

        Returns
        -------
        group : str
            The name of the group in lowercase.
            
        Raises
        ------
        InvalidGroupError
            If the group is not a string or the name is not in the list.
    """
    if not isinstance(group, str):
        raise InvalidGroupError("Group must be of type str.")
    
    group = group.lower()
    
    if group not in valid_groups:
        raise InvalidGroupError(f"{group} is not a valid group name")

    return group

def get_valid_groups(groups_file="./data/chats.txt"):
    """ Get a dictionary of telegram groups with its respective id.

        Parmaters
        ---------
        groups_file : 
            Name or path of the file that contains the group names an ids.
        
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
            group_id = int(chat_info[-1].rstrip())
            valid_groups[group_name] = group_id
    
    return valid_groups


def get_ftp_login_data(ftp_file="./data/ftp.txt"):
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

def get_default_group_id(groups_file="./data/chats.txt"):
    """ Get the default group id.
    
        This function is used in case a group was not passed as an argv.
        
        Parmaters
        ---------
        groups_file : str
            Name or path of the file that contains the group names an ids.
        
        Returns
        -------
        int
            The default group id.
        
    """
    default_idx = -1
    with open(groups_file, "r") as fh:
        lines = fh.readlines()
        return int(lines[default_idx].split(",")[-1])
    

def get_group_and_port(argvs, groups_file="./data/chats.txt"):
    """ Get port number and group id from argvs passed to the program.

        Parameters
        ----------
        argvs : list
            List with the argvs
        
        groups_file : str
            Name or path of the file that contains the group names an ids.
            
        Returns
        -------
        port : int
            The port number
        
        group : int
            Id of the telegram group.
    """
    if len(argvs) == 3:
        port  = validate_port(argvs[1])
        valid_groups = get_valid_groups(groups_file)
        group_name = validate_group(argvs[2], list(valid_groups.keys()))
        group_id = valid_groups[group_name]
    
    elif len(argvs) == 2:
        port  = validate_port(argvs[1])
        group_id = get_default_group_id(groups_file)
    else:
        port = 13384
        group_id = get_default_group_id(groups_file)
    
    return group_id, port
