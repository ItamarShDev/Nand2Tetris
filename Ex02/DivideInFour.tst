load DivideInFour.hdl,
output-file DivideInFour.out,
compare-to DivideInFour.cmp,
output-list in%B1.16.1 a%B1.16.1  b%B1.16.1;

set in %B0000100001010110,  // in = 2134
eval,
output;

set in %B0000000000000000,  // in = 0
eval,
output;

set in %B1111111111111111,  // in = -1 (equivalent to 2^16-1)
eval,
output;

set in %B1000100100011111,  // in = 35103
eval,
output;
