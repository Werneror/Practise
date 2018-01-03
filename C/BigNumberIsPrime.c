/*编译命令：gcc p.c -std=c99 -lm */

#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<time.h>

int isprime(unsigned long long);

int main(int argc,char *argv[])
{
	int i;
	unsigned long long c = 18446744073709551615L;
	time_t start = clock();
	for(i=0;i<500;i++)
	{
		if(isprime(c-i))
		    printf("%llu is a prime integer\n", c-i);
	}
	time_t end = clock();
	printf("Total time : %f seconds.\n", ((double)(end -start)/CLOCKS_PER_SEC));
	return 0;
}

int isprime(unsigned long long n)
/*判断一个大整数是否是质数,若是质数,返回1,其他,返回0*/
{
	unsigned long long primelist[13] = {18446744073709551557,
								18446744073709551533,
								18446744073709551521,
								18446744073709551437,
								18446744073709551427,
								18446744073709551359,
								18446744073709551337,
								18446744073709551293,
								18446744073709551263,
								18446744073709551253,
								18446744073709551191,
								18446744073709551163,
								18446744073709551113};
	unsigned long long i=0;
	unsigned long long sqn;
	if(n<2)
	{
		return 0;
	}
	else if(n>18446744073709551112)
	{

		for(i=0;i<13;i++)
		{
			if(n==primelist[i])
				return 1;	
		}
		return 0;
	}
	else
	{
		sqn = (unsigned long long)sqrt(n);
		if(n==2){
		    return 1;
		}
		if(n%2==0){
		    return 0;
		}
		i=1;
		do{
		    i = i+2;
		    if( i > sqn ){
		        return 1;
		    }
		    if( n%i == 0 ){
		        return 0;
		    }
		}while(1);
	}
}
