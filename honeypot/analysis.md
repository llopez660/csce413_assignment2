# Honeypot Analysis


## Summary of Observed Attacks

I was able to successfully implement a honeypot on port 2222 using paramiko. During testing, I was able to successfully intercept and log all login attempts, including their IP, and attempted passwords and usernames while rejecting all the credentials to keep them guessing and logging more activity done by the attacker. 

## Notable Patterns

The logs all have a standard format which captures all the data being inputted from the attacker along with the attacker's IP. An observation that was made is that all attacks are being originated from the Docker gateway IP because this is a result of the Docker Bridge Network configuration. Regardless we are able to get all the other metadata such as the username and password in the same format.

## Recommendations
To improve this I would recommend making this honeypot more interatacble by having a list of username and passwords that may work and it make the attacker think they were able to succesfully ssh into the port and we will be able to gather any malicious scripts they may want to run. 