#include<stdio.h>
int FibonacciKM(int k, int m);
int main(){
    int k,m;
    scanf("%d",&k);
    scanf("%d",&m);
    printf("结果是%d。\n",FibonacciKM(k, m));
    return 0;
}
int FibonacciKM(int k, int m){
    //计算k阶斐波那契数列第m项的值
    //规定从第0项算起
    int i;
    int number =0;
    if(m<k-1) return 0;
    else if(m==k-1) return 1;
    else{
        for(i=1;i<=k;i++)
            number += FibonacciKM(k, m-i);
        return number;
    }
}//FibonacciKM
