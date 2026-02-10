# Honeypot Analysis


## Summary of Observed Attacks

I was able to attack the port and I was able to succesfully log all the authentication methods I used such as passwords and usernames. I was able to accomplish this by using paramiko on port 2222

## Notable Patterns

The logs all look identical except for the IP address from the attacker, since all attacks are being originated from the gateway IP but the username and password change depending on the different methods I tried to breach the port. Along with this they inclue critical information such as date and time. 

## Recommendations
To improve this I would recommend maybe having a list of username and passwords that may work often and letting the user actually think they are and gather malicious scripts they may want to run.