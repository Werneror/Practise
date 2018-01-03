#include<stdio.h>
#include<stdlib.h>
#include"sqstack.h"
int main(){
    char str[100];
    scanf("%s",str);
    if(Matchkuohao(str))
        printf("匹配\n");
    else
        printf("不匹配\n");
    return OK;    
}
Status Matchkuohao(char *a){
    //检查字符串中的括号(){}[]<>是否匹配
    char tempchar; //用于临时存放字符的变量
    SqStack S;  //需要一个真实存在的*a，否则会发生段错误
    InitStack(&S);
    do{
        if(*a=='['||*a=='('||*a=='<'||*a=='{')
            Push(&S,*a);
        else if(*a==']'||*a==')'||*a=='>'||*a=='}'){
            if(Pop(&S,&tempchar)==ERROR) return FALSE;
            switch(tempchar){
                case '[': if(*a!=']') return FALSE;break;
                case '(': if(*a!=')') return FALSE;break;
                case '<': if(*a!='>') return FALSE;break;
                case '{': if(*a!='}') return FALSE;break;
                default: return ERROR;
            }//switch
        }//else if
    }while(*a++!='\0');
    if(StackEmpty(S)==FALSE) return FALSE;//如果栈不为空，则不匹配
    return TRUE;
}//Matchkuohao
