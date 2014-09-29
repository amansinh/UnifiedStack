#import TS_Setup as TS


class SwitchConfigurator:
    
    # Returns SSH connection through which terminal needs to be invoked to send
    # a command and recieve it's output
    def establish_connection(self, ipaddress, username, password):
        remote_conn_pre = paramiko.SSHClient()
        # Automatically add untrusted hosts
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        remote_conn_pre.connect(
            ipaddress,
            username=username,
            password=password)
        return remote_conn_pre

    # Used to configure any switch with reference to the topology provided from
    # config file.
    # TODO - Commonds file is later auto-generated and not sent as a parameter
    def configure_switch(self, ip_address, username, password, commands_file):
        remote_conn_client = self.establish_connection(
            ipaddress=ip_address,
            username=username,
            password=password)
        # Use invoke_shell to establish an 'interactive session'
        remote_conn = remote_conn_client.invoke_shell()
        output = remote_conn.recv(1000)
        for line in open(commands_file):
            # error check for ssh connection and send function and retry 3
            # times if fail
            success = False
            attempts = 0
            while (success == False) and (attempts < 3):
                try:
                    remote_conn.send(line)
                    time.sleep(1)
                    success = True
                except socket.error as e:
                    # print "Connection is not established : " + e.strerror
                    attempts += 1
        output = remote_conn.recv(5000)

    def configure_switch(self, console):
        #sw3750_config = sw_3750.Switch3750Configurator()
        #sw3750_config.configure_3750switch(console)
        #console.cprint_progress_bar("Configured the 3750 switch", 50)
        
        # Configuring 3750 Switch
        ip_address_9k = Config.get_switch_field("3750-ip-address")
        username_9k = Config.get_switch_field("3750-username")
        password_9k = Config.get_switch_field("3750-password")
        self.configure_switch(ipaddress = ip_address_9k,
                              username = username_9k,
                              password = password_9,
                              commands_file = 'netswitch/sw3750_commands.txt')
        
        # Configuring 9k Switch
        ip_address_9k = Config.get_switch_field("9k-ip-address")
        username_9k = Config.get_switch_field("9k-username")
        password_9k = Config.get_switch_field("9k-password")
        self.configure_switch(ipaddress = ip_address_9k,
                              username = username_9k,
                              password = password_9,
                              commands_file = 'netswitch/sw9k_commands.txt')
        
        console.cprint_progress_bar("Configured the N9K switch", 100)


if __name__ == "__main__":
    sw_config = sw.SwitchConfigurator()
    sw_config.configure_switch()
