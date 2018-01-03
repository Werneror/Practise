//题目网址：http://poj.org/problem?id=1416
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <malloc.h>
//函数结果状态代码
#define TRUE 1
#define FALSE 0
#define OK 1
#define ERROR 0
#define INFEASIBLE -1
// Status是函的数类型，其值是函数结果状态代码
typedef int Status;

#define STACK_INIT_SIZE 101 //存储空间初始分配量
#define STACKINCREMENT 10   //存储空间分配曾量

typedef int SElemType;

typedef struct {
   SElemType * base;    //栈底指针，在栈构造前和销毁后，其值为NULL
   SElemType * top; //栈顶指针
   int stacksize;   //当前已分配的存储空间，以元素为单位
}SqStack;

int numberlen(int);
int Shredding(int flag[], int n, int papernumber, int p);
int function(int flag[], int sole[], int n, int c, int papernumber, int target);
int main(){
  int target;
  int papernumber;
  int flag[6];
  int i;
  int j;
  int n;
  int sole[6];
  do{
    scanf("%d%d", &target, &papernumber);
    //printf("target=%d, papernumber=%d\n", target, papernumber);
    if(target==0&&papernumber==0){
      break;
    }
    n = numberlen(papernumber);
    for(i=0;i<n-1;i++){
      flag[i] = 0;
      sole[i] = 0;
    }
    function(flag, sole, n, 0, papernumber, target);
  }while(1);
  return 0;
}
int function(int flag[], int sole[], int n, int c, int papernumber, int target){
  //用于实现递归调用
  static int rejected=0;
  static int rrr=0;
  int temp;
  int i=0;
  int flag1[6];
  int flag2[6];
  if(c>n-1) return;
  for(i=0;i<n-1;i++){
    flag1[i]=flag[i];
    flag2[i]=flag[i];
  }
  for(i=0;i<n-1;i++){
    //printf("%d ", flag[i]);
  }
  //printf("\n");
  temp = Shredding(flag, n, papernumber, 0);
  if(temp>=rrr&&temp<=target){
    if(temp==rrr){
      for(i=0;i<n-1;i++){
        if(sole[i]!=flag[i])
          rejected=1;
      }
    }
    else rejected=0;
    rrr=temp;
    for(i=0;i<n-1;i++){
      //printf("%d ", flag[i]);
      sole[i]=flag[i];
    }
    //printf("\n");
  }
  else if(temp<rrr) return;
  function(flag1, sole, n, c+1, papernumber, target);
  flag2[c]=1;
  function(flag2, sole, n, c+1, papernumber, target);
  if(c==0){
    if(rejected){
      printf("rejected\n");
      rejected=0;
    }
    else if(rrr!=0){
      printf("%d ", rrr);
      Shredding(sole, n, papernumber, 1);
      rrr=0;
    }
    else
      printf("error\n");
    }
}
int Shredding(int flag[], int n, int papernumber, int p){
  //按照分割数组flag分割数字papernumber，数字长度是n，返回划分和
  //p控制是否打印划分，p=1则打印，否则不打印
  int sum=0;
  int temp=0;
  int pn;
  int i=1;
  int j=0;
  SqStack S;
  if(p) InitStack(&S);
  pn = papernumber;
  while(n-i>=0){
    i++;
    temp = temp + (pn%10)*pow(10,j);
    if(flag[n-i]==1){
      sum+=temp;
      if(p)
        Push(&S, temp);
      temp=0;
      j=0;
    }
    else{
      j+=1;
    }
    pn/=10;
  }
  if(p&&temp!=0)
    Push(&S, temp);
  sum += temp;
  if(p){
    while(StackLength(S)>1){
      Pop(&S, &temp);
      printf("%d ", temp);
    }
    Pop(&S, &temp);
    printf("%d\n", temp);
    DestroyStack(&S);
  }
  return sum;
}
int numberlen(int n) {
  //返回十进制数的位数
  int re=1;
  while(1) {
    n=n/10;
    if (n!=0) re++;
    else return re;
  }
}

Status InitStack(SqStack *S){
    //构造一个空栈
    (*S).base = (SElemType *)malloc(STACK_INIT_SIZE*sizeof(SElemType));
    if(!(*S).base) return OVERFLOW;
    (*S).top = (*S).base;
    (*S).stacksize = STACK_INIT_SIZE;
    return OK;
}//InitStack

Status DestroyStack(SqStack *S){
    //销毁栈S，S不再存在
    if(!(*S).base) return ERROR;
    free((*S).base);
    (*S).base = NULL;
    (*S).top = NULL;
    (*S).stacksize = 0;
    return OK;
}//DestroyStack

int StackLength(SqStack S){
    //返回(*S)的元素个数，即栈的长度
    if(!S.base) return ERROR;
    return S.top-S.base;
}//StackLength

Status Push(SqStack *S, SElemType e){
    //插入元素e为新的栈顶元素
    if(!(*S).base) return ERROR;
    if((*S).top-(*S).base>=(*S).stacksize){
        //栈已满，扩大空间
        (*S).base = (SElemType*)realloc((*S).base, ((*S).stacksize+STACKINCREMENT)*sizeof(SElemType));
        if(!(*S).base) return OVERFLOW;
        (*S).top = (*S).base + (*S).stacksize;
        (*S).stacksize += STACKINCREMENT;
    }//if
    *(*S).top++ = e;
    return OK;
}//Push

Status Pop(SqStack *S, SElemType *e){
    //若栈不为空，则删除(*S)的栈顶元素，用e返回其值，并返回OK，否则返回ERROR
    if(!(*S).base) return ERROR;
    if((*S).base== (*S).top) return ERROR;
    *e = *--(*S).top;
    return OK;
}//Pop
