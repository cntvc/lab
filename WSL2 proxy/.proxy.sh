hostip=$(cat /etc/resolv.conf | grep nameserver | awk '{ print $2 }')
wslip=$(hostname -I | awk '{print $1}')
port=10800
PROXY_SOCKS="http://${hostip}:${port}"

function display() {
    echo "Host ip: ${hostip}"
    echo "WSL client ip: ${wslip}"
    echo "current PROXY: ${PROXY_SOCKS}"
}

function set_proxy() {
    export http_proxy="${PROXY_SOCKS}"
    export https_proxy="${PROXY_SOCKS}"
    echo "env http/https proxy set."
}

function unset_proxy() {
    unset http_proxy
    unset https_proxy
    echo "env proxy unset."
}

function test_proxy() {
    curl -vv www.google.com
}

if [ "$1" = "show" ]; then
    display
elif [ "$1" = "set" ]; then
    set_proxy
elif [ "$1" = "unset" ]; then
    unset_proxy
elif [ "$1" = "test" ]; then
    test_proxy
else
    echo "incorrect arguments."
fi