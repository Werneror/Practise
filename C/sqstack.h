#include"adt.h"
#define STACK_INIT_SIZE 100 //存储空间初始分配量
#define STACKINCREMENT 10   //存储空间分配曾量
typedef int Status;

typedef char SElemType;

typedef struct {
   SElemType * base;    //栈底指针，在栈构造前和销毁后，其值为NULL
   SElemType * top; //栈顶指针
   int stacksize;   //当前已分配的存储空间，以元素为单位
}SqStack;

Status InitStack(SqStack *S){
    //构造一个空栈
    (*S).base = (SElemType *)malloc(STACK_INIT_SIZE*sizeof(SElemType));
    if(!(*S).base) exit(OVERFLOW);
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

Status ClearStack(SqStack *S){
    //把S置为空栈
    if(!(*S).base) return ERROR;
    (*S).top = (*S).base;
    return OK;
}//ClearStack

Status StackEmpty(SqStack S){
    //若栈S为空，则返回TRUE，否则返回FASLE
    if(S.base==NULL || S.base!=S.top) return FALSE;
    return TRUE;
}//StackEmpty

int StackLength(SqStack S){
    //返回(*S)的元素个数，即栈的长度
    if(!S.base) return ERROR;
    return S.top-S.base;
}//StackLength

Status GetTop(SqStack S, SElemType *e){
    //若栈不空，则用e返回S的栈顶元素，并返回OK，否则返回ERROR
    if(!S.base) return ERROR;
    *e = *(S.top-1);
    return OK;
}//GetTop

Status Push(SqStack *S, SElemType e){
    //插入元素e为新的栈顶元素
    if(!(*S).base) return ERROR;
    if((*S).top-(*S).base>=(*S).stacksize){
        //栈已满，扩大空间
        (*S).base = (SElemType*)realloc((*S).base, ((*S).stacksize+STACKINCREMENT)*sizeof(SElemType));
        if(!(*S).base) exit(OVERFLOW);
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

Status StackTraverse(SqStack S, Status(*visit)()){
    //从栈底到栈顶依次对栈中每个元素调用函数visit()。一旦visit()调用失败，则操作失败
    SElemType *p;
    if(!S.base) return ERROR;
    p = S.base;
    while(p!=S.base) visit(p++);
    return OK;
}
