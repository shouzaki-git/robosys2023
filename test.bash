#1/bin/bush -xv
# SPDX-FileCopyrightText: 2023 Sho Uzaki
# SPDX-License-Identifier: BSD-3-Clause

ng () {
        echo NG at LINE "$1"
	ret=1
}

ret=0

### I/O ###
out=$(seq 5 | ./plus)
[ "${out}" = 15 ] || ng ${LINENO}

### STRANGE INPUT ###
out=$(echo あ | ./plus)
[ "$?" = 1 ]      || ng {LINENO}
[ "${out}" = "" ] || ng {LINENO}    

out=$(echo | ./plus)
[ "$?" = 1 ]      || ng ${LINENO}
[ "${out}" = "" ] || ng ${LINENO}

[ "$ret" = 0 ] && echo OK
exit $ret


