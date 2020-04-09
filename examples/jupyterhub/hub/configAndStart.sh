#!/bin/bash
for i in "$@"
do
case $i in
    --ldap=*)
    	LDAP="${i#*=}"
    	shift # past argument=value
    ;;
    --port=*)
    	PORT="${i#*=}"
    	shift # past argument=value
    ;;
    *)
	# Unknown Option
	echo "Unknown option $i"
	shift
    ;;
esac
done

if [ ! -z "$LDAP" ];
then
	sed --regexp-extended --in-place "s/c.LDAPAuthenticator.server_address = .+/c.LDAPAuthenticator.server_address = '${LDAP}'/" jupyterhub_config.py
else
	echo "Using default ldap server 172.17.0.2. Use '--ldap=SERVER_IP' to specify a custom value'"
fi

if [ -z "$PORT" ];
then
	PORT=8000
	echo "Using default port 8000. Use '--port=####' to specify a custom value'"
fi

if [ ! -d "/certs" ];
then
	echo "No certificate directory was found at '/certs/'"
	echo "Use a docker mount point to mount a directory containing a single .key and .crt file for your certificate"
	echo "By adding the flag '-v /SOME/CERT/DIR:/certs/:z' to your 'docker run' command"
	exit 1
fi 

KEY=`find /certs/ -name "*.key" | head -1`
CERT=`find /certs/ -name "*.crt" | head -1`

if [ -z "$KEY" ] || [ -z "$CERT" ];
then
	echo "A .key or .crt file could not be found in the '/certs/' directory"
	exit 1
fi

echo "Using keyfile: $KEY"
echo "Using certfile: $CERT"

jupyterhub --ssl-key=$KEY --ssl-cert=$CERT --port=$PORT
