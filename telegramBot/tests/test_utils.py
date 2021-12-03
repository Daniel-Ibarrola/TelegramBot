import telegramBot.utils.utils as utils
from telegramBot.utils.exceptions import InvalidPortError, InvalidGroupError
import pytest

def test_get_valid_groups():
    
    valid_groups = utils.get_valid_groups("./tests/data/mock-groups.txt")
    assert "grupo_1" in valid_groups
    assert "grupo_2" in valid_groups
    assert "grupo_3" in valid_groups
    assert valid_groups["grupo_1"] == -500023
    assert valid_groups["grupo_2"] == -650012
    assert valid_groups["grupo_3"] == -123567

def test_validate_group():
    
    valid_groups = list(utils.get_valid_groups("./tests/data/mock-groups.txt").keys())
    group_name = "patito-de-hule"
    with pytest.raises(InvalidGroupError, match="is not a valid group name"):
        utils.validate_group(group_name, valid_groups)
    
    group_name = "Grupo_1" 
    assert utils.validate_group(group_name, valid_groups) == "grupo_1"
    
    group_name = "grupo_2" 
    assert utils.validate_group(group_name, valid_groups) == "grupo_2"

def test_validate_port():
    port = "13a26"
    with pytest.raises(InvalidPortError, match="is not a valid value for port"):
        utils.validate_port(port)
    
    port = "-5436"
    with pytest.raises(InvalidPortError, match="Port must be a number greater than zero"):
        utils.validate_port(port)
        
    port = "16050"
    assert utils.validate_port(port) == 16050

def test_get_ftp_login_data():
    user, password = utils.get_ftp_login_data("./tests/data/mock-ftp.txt")
    assert user == "patito-de-hule@email.com"
    assert password == "asdfg1234"

def test_get_default_group_id():
    assert utils.get_default_group_id("./tests/data/mock-groups.txt") == -123567

def test_get_group_and_port():
    
    argvs = ["main.py", "13500", "Grupo_1"]
    group_id, port = utils.get_group_and_port(argvs, "./tests/data/mock-groups.txt")
    assert group_id == -500023
    assert port == 13500
    
    argvs = ["main.py", "14500"]
    group_id, port = utils.get_group_and_port(argvs, "./tests/data/mock-groups.txt")
    assert group_id == -123567
    assert port == 14500
    
    argvs = ["main.py"]
    group_id, port = utils.get_group_and_port(argvs, "./tests/data/mock-groups.txt")
    assert group_id == -123567
    assert port == 13384