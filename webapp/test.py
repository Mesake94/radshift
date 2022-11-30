import requests

url = "http://ap-ne1-guest.cloud.cambiumnetworks.com:444/cgi-bin/hotspot_login.cgi?ga_ssid=rogowifi&ga_ap_mac=BC-E6-7C-49-5E-A0&ga_nas_id=TESTAP_BASE&ga_srvr=ap-ne1-guest.cloud.cambiumnetworks.com&ga_cmac=76-7C-98-06-87-99&ga_Qv=eUROBR86HBgAGDEEVgQAGw4UWRUCACYVMgFPTFRZWFpfU1FGUVdFIn5ZRVZLBhMUMww."

r = requests.post(url)