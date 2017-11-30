import paramiko
def run(host='35.154.100.41', port=2200, user='grader',
                  command="mpstat | grep 'all'", bufsize=-1, key_filename='/home/ubuntu/grader_key',
                  timeout=120, pkey=None):
    """
    Excecutes a command using paramiko and returns the result.
    :param host: Host to connect
    :param port: The port number
    :param user: The username of the system
    :param command: The command to run
    :param key_filename: SSH private key file.
    :param pkey: RSAKey if we want to login with a in-memory key
    :return:
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(hostname=host, port=port,
            username=user, key_filename=key_filename, banner_timeout=10)
    chan = client.get_transport().open_session()
    chan.settimeout(timeout)
    chan.set_combine_stderr(True)
    chan.get_pty()
    chan.exec_command(command)
    stdout = chan.makefile('r', bufsize)
    stdout_text = stdout.read()
    status = int(chan.recv_exit_status())
    client.close()
    temp_text = ''
    try:
        temp_text = str(stdout_text,'utf-8')
    except:
        status = 1
    return temp_text, status

if __name__ == '__main__':
    text,status = run()
    text = str(text,'utf-8')
    print(text.strip().split())
    cpu = text.strip().split()
    print(text)
