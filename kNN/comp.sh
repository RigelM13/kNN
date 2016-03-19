
gcc kNN.c -o kNN -lm
echo
echo 'd: Euclidea'
echo 'k = 1'
./kNN 1 e t
echo
echo
echo 'k = 3'
./kNN 3 e t
echo
echo
echo 'k = 5'
./kNN 5 e t

echo
echo 'd: Absoluta'
echo 'k = 1'
./kNN 1 a t
echo
echo
echo 'k = 3'
./kNN 3 a t
echo
echo
echo 'k = 5'
./kNN 5 a t

