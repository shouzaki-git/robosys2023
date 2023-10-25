#1/bin/bush

ng () {
        echo NG at LINE "$1"
	ret=1
}

ret=0

out=$(seq 5 | ./plus)

[ "${out}" = 15 ] || ng ${LINENO}

[ "$ret" = 0 ] && echo OK
exit $ret


