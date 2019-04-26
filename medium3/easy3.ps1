# RITSEC Demos Week 13
# Easy 3

New-NetIPAddress -InterfaceIndex 11 -IPAddress 192.168.1.1 -PrefixLength "24" -DefaultGateway 192.168.1.254
Set-DnsClientServerAddress -InterfaceIndex 11 -ServerAddresses 192.168.1.1
Install-WindowsFeature AD-Domain-Services
Set-ADDomain -Identity DHCP1 -AllowedDNSSuffixes @{Add="ritsec.com"}