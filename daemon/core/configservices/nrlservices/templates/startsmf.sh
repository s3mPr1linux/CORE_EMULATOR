<%
  ifaces = ",".join(ifnames)
  if has_nhdp:
    flood = "ecds"
  elif has_olsr:
    flood = "smpr"
  else:
    flood = "cf"
%>
#!/bin/sh
# auto-generated by NrlSmf service
nrlsmf instance ${node.name}_smf ${flood} ${ifaces} hash MD5 log /var/log/nrlsmf.log < /dev/null > /dev/null 2>&1 &
