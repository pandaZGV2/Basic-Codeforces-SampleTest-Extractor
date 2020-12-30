FILE=a.out
PROG_NAME=$1
if !(test -f "$PROG_NAME"); then
    echo "$PROG_NAME does not exist!"
    exit 0
else
    contest_number=$(echo $PROG_NAME | sed -r -e "s/(^.+?[0-9])[A-Z]\.+?/\1/")
    qno_letter=$(echo $PROG_NAME | sed -r -e "s/^.+?[0-9]([A-Z])\.*/\1/")
    eval "python3 cftestcase.py $contest_number $qno_letter"
fi
if test -f "$FILE"; then
    echo "$FILE removed!"
    rm $FILE
fi
re1='^.*\.cpp'
re2='^.*\.c'
contest_number=$(echo $PROG_NAME | sed -r -e "s/(^.+?[0-9])[A-Z]\.+?/\1/")
qno_letter=$(echo $PROG_NAME | sed -r -e "s/^.+?[0-9]([A-Z])\.*/\1/")
echo "$contest_number"
echo "$qno_letter"
if [[ $1 =~ $re1 ]]; then
    echo "CPP Detected"
    eval "g++ -Wall -Wextra -pedantic -std=c++17 -O2 -Wshadow -Wformat=2 -Wfloat-equal -Wconversion -Wlogical-op -Wshift-overflow=2 -Wduplicated-cond -Wcast-qual -Wcast-align -D_GLIBCXX_DEBUG -D_GLIBCXX_DEBUG_PEDANTIC -D_FORTIFY_SOURCE=2 -fsanitize=address -fsanitize=undefined -fno-sanitize-recover -fstack-protector $PROG_NAME"

elif [[ $1 =~ $re2 ]]; then
    echo "C Detected"
    eval "gcc -Wall -Wextra -pedantic -std=c99 -O2 -Wshadow -Wformat=2 -Wfloat-equal -Wconversion -Wlogical-op -Wshift-overflow=2 -Wduplicated-cond -Wcast-qual -Wcast-align -D_GLIBCXX_DEBUG -D_GLIBCXX_DEBUG_PEDANTIC -D_FORTIFY_SOURCE=2 -fsanitize=address -fsanitize=undefined -fno-sanitize-recover -fstack-protector $PROG_NAME"
fi


if test -f "$FILE"; then
    ./$FILE < input.txt > output.txt
fi