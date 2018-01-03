#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>
#define TRUE 1
#define FALSE 0
#define OK 1
#define ERROR 0
#define INFEASTABLE -1
#define OVERFLOW -2
#define PlusInfinity 65535
#define Number 6    //有向图节点个数
typedef int status;
//定义一个队列结构
typedef struct QNode{
    int data;
    struct QNode * next;
}QNode, *QueuePtr;
typedef struct{
   QueuePtr front;  //队头指针
   QueuePtr rear;   //队尾指针
}LinkQueue;

void SHORTESTPATHS(unsigned int cost[Number][Number]);
int main(){
    unsigned int cost[Number][Number] = {{0, 20, 15, PlusInfinity, PlusInfinity, PlusInfinity},
                      {2, 0, PlusInfinity, PlusInfinity, 10, 30},
                      {PlusInfinity, 4, 0, PlusInfinity, PlusInfinity, 10},
                      {PlusInfinity, PlusInfinity, PlusInfinity, 0, PlusInfinity, PlusInfinity},
                      {PlusInfinity, PlusInfinity, PlusInfinity, 15, 0, PlusInfinity},
                      {PlusInfinity, PlusInfinity, PlusInfinity, 4, 10, 0}};
    SHORTESTPATHS(cost);
    return 0;
}
void SHORTESTPATHS(unsigned int cost[Number][Number]){
    //cost是有向图的成本邻接矩阵，是一个n乘n的二维数组
    unsigned int s[Number]={0};
    unsigned int dist[Number]={0};
    LinkQueue path[Number];             //存放到各个节点的路径
    unsigned int i=0;                   //循环计数变量
    unsigned int j=0;                   //循环计数变量
    unsigned int flag=0;
    unsigned int n=0;

    s[0]=1;                             //将第一个节点加入s
    for(i=0;i<Number;++i){
        dist[i]=cost[0][i];             //初始化dist
        InitQueue(&path[i]);            //初始化path
        EnQueue(&path[i],0);            //将第一个节点的路径加入path
    }
    for(j=0;j<Number-1;++j){
        flag=PlusInfinity;
        n=PlusInfinity;
        //找出将第几个节点加入s
        for(i=0;i<Number;++i){
            if(s[i]==0){
                if(dist[i]<flag){
                    flag=dist[i];
                    n=i;
                }
            }
        }
        s[n]=1;                             //将第n个节点加入s
        EnQueue(&path[n], n);                //将第n个节点的路径加入path
        //更新dist
        for(i=0;i<Number;++i){
            if(s[i]==0){
                flag = cost[n][i]+dist[n];
                if(flag<dist[i]){
                    dist[i]=flag;
                    CpQueue(&path[i], &path[n]);
                }
            }
        }
    }
    for(j=0;j<Number;++j){
        printf("第%d个节点，路径长度为%2d， 路径为 ",j+1, dist[j]);
        while(QueueEmpty(path[j])==FALSE){
            DeQueue(&path[j], &n);
            printf("%d ",n+1);
        }
        printf("\n");
    }
}

//队列相关的函数
status InitQueue(LinkQueue *Q){
    //构造一个新队列
    (*Q).front = (*Q).rear = (QueuePtr)malloc(sizeof(int));
    if(!(Q->front)) exit(OVERFLOW);
    Q->front->next=NULL;
    return OK;
}//end of InitQueue
status DestroyQueue(LinkQueue *Q){
    //销毁队列Q
    while(Q->front){
        Q->rear = Q->front->next;
        free(Q->front);
        Q->front=Q->rear;
    }
    return OK;
}//end of DestroyQueue
status QueueEmpty(LinkQueue Q){
    //若队列Q为空队列，则返回TRUE，否则返回FALSE
    if(Q.front==Q.rear) return TRUE;
    else return FALSE;
}//end of QueueEmpty
status EnQueue(LinkQueue *Q, int e){
    //插入元素e为Q的新的队尾元素
    QueuePtr p;
    p = (QueuePtr)malloc(sizeof(int));
    if(!p) exit(INFEASTABLE);
    p->data=e;
    p->next=NULL;
    Q->rear->next=p;
    Q->rear=p;
    return OK;
}//end EnQueue
status DeQueue(LinkQueue *Q, int *e){
    //若队列不为空，则删除Q的对头元素，用e返回其值，并返回OK；
    //否则返回ERROR；
    QueuePtr p;
    if(Q->front==Q->rear) return ERROR;
    p = (*Q).front->next;
    (*e) = p->data;
    (*Q).front->next = p->next;
    if(Q->rear==p) Q->rear=Q->front;
    free(p);
    return OK;
}//end of DeQueue
status CpQueue(LinkQueue *Q, LinkQueue *P){
    //拷贝队列P到Q，会销毁Q原有的值
    int temp;
    DestroyQueue(Q);
    InitQueue(Q);
    QueuePtr p;
    if(P->front==P->rear) return OK;    //P为空
    p = (*P).front->next;
    while(p!=NULL){
        temp = p->data;
        EnQueue(Q, temp);
        p = p->next;
    }
    return OK;
}
