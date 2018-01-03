#include<stdio.h>
#include<math.h>
#define True 1
#define Flase 0
#define None -1

int isprime(unsigned long long n)
/*判断一个正整数是否是质数,若是质数,返回True,其他,返回Flase*/
{
	unsigned long long i=0;
	unsigned long long sqn;
	short flag=None;
	if(n<2)
	{
		flag=Flase;
	}
	else if(n==2)
	{
		flag=True;
	}
	else if(n%2==0)
	{
		flag=Flase;
	}
	else
	{
		i=1;
		sqn = (unsigned long long)sqrt(n);
		do{
		    i = i+2;
		    if( i > sqn ){
		        flag=True;
		    }
		    if( n%i == 0 ){
		        flag=Flase;
		    }
		}while(flag==None);
	}
	return flag;
}
