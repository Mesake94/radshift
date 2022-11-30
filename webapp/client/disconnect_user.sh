                              
#!/bin/sh    

# script to run radclient to disconnect user
cat disconnect_packet.txt | radclient -x 192.168.1.101:3799 disconnect 'testing123'