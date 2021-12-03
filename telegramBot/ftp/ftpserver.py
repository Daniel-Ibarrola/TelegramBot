from ftplib import FTP

def download_file(user, password):
    """ Download latest file from ftp server

        Parameters
        ----------
        user : str
            Name of the ftp user.
        
        password : str
            Password of the ftp server.
    """
    #Connect to ftp server
    ftp = FTP()
    ftp.connect('132.248.105.35', 2421)
    ftp.login(user, password)

    #Get latest file
    entries = list(ftp.mlsd())
    entries.sort(key = lambda entry: entry[1]['modify'], reverse = True)
    latest_name = entries[0][0]
    
    localfile = open(latest_name, 'wb')
    #Download file in blocks of 1024 bytes
    ftp.retrbinary('RETR ' + latest_name, localfile.write, 1024 )

    ftp.quit()
    localfile.close()

def upload_file_to_ftp(user, password, file_name):
    """ Upload a file to an ftp server.
    
        Parameters
        ----------
        user : str
            Name of the ftp user.
        
        password : str
            Password of the ftp server.
            
        file_name : str
            Path or name of the file that will be uploaded.
        
    """
    #Connect to ftp server
    ftp = FTP()
    ftp.connect('132.248.105.35', 2421)
    ftp.login(user, password)

    ftp.storbinary('STOR ' + file_name, open(file_name, 'rb'))
    ftp.quit()


def remove_files_from_ftp(user, password, file_list):
    """ Remove a file from an ftp server
    
        Parameters
        ----------
        user : str
            Name of the ftp user.
        
        password : str
            Password of the ftp server.
            
        file_list : list of str
            List with files that will be deleted.
    
    """
    ftp = FTP()

    ftp.connect('132.248.105.35', 2421)
    ftp.login(user, password)

    for file in file_list:
        ftp.delete(file)