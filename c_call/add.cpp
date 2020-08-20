#include <stdio.h>

extern "C"
int add(const int a,const int b)
{
    printf("a + b = %d\n", a+b);
    return a + b;
}