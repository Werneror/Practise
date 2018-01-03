#include <stdio.h>
#include <malloc.h>
#include <stdlib.h>
#include <string.h>

/*---------page 10 on textbook ---------*/
#define TRUE 1
#define FALSE 0
#define OK 1
#define ERROR 0
#define INFEASTABLE -1
#define OVERFLOW -2

typedef int status;
typedef char ElemType; //数据元素类型定义
typedef struct BiTNode{
    ElemType   data;
    struct BiTNode  *lchild, *rchild;//左右孩子指针
}BiTNode, *BiTree;
int strnum = 0;       //定义全局变量，在CreateBiTree时使用

//定义一个队列结构
typedef struct QNode{
    BiTree data;
    struct QNode * next;
}QNode, *QueuePtr;
typedef struct{
   QueuePtr front;  //队头指针
   QueuePtr rear;   //队尾指针
}LinkQueue;

status InitBiTree(BiTree *headp);       //1
status DestroyBiTree(BiTree *headp);    //2
status CreateBiTree(BiTree *root, char *definition);           //3
status ClearBiTree(BiTree *headp);      //4
status BiTreeEmpty(BiTree headp);       //5
int BiTreeDepth(BiTree root);           //6
BiTNode Root(BiTree headp);             //7
BiTree Value(BiTree headp, ElemType e); //8
status Assign(BiTree headp, ElemType o, ElemType n);           //9
BiTree Parent(BiTree headp, ElemType e);                       //10
BiTree LeftChild(BiTree headp, ElemType e);                    //11
BiTree ReftChild(BiTree headp, ElemType e);                    //12
BiTree LeftSibling(BiTree headp,ElemType e);                   //13
BiTree ReftSibling(BiTree headp,ElemType e);                   //14
status InsertChild(BiTree headp,ElemType e,int LR,BiTree c);   //15
status DeleteChild(BiTree headp,ElemType e,int LR);            //16
void PreOrderTraverse(BiTree root);     //17
void InOrderTraverse(BiTree root);      //18
void PostOrderTraverse(BiTree root);    //19
void LevelOrderTraverse(BiTree root);   //20
BiTree CreateNode();
int main(){
  int op=1;
  int lr=0;
  status flag;
  BiTree headp=NULL;
  BiTree c=NULL;
  BiTree re;            //接收函数返回值
  char def[100];        //作为输入二叉树的缓冲区
  char a;
  char b;
  while(op){
    system("clear");
    printf("\n");
	printf("      Menu for Binary Trees On Binary Linked List      \n");
	printf("-------------------------------------------------------\n");
	printf("    1. InitBiTree              11. LeftChild\n");
	printf("    2. DestroyBiTree           12. RightChild\n");
	printf("    3. CreateBiTree            13. LeftSibling\n");
	printf("    4. ClearBiTree             14. RightSibling\n");
	printf("    5. BiTreeEmpty   	       15. InsertChild\n");
	printf("    6. BiTreeDepth             16. DeleteChild\n");
	printf("    7. Root                    17. PreOrderTraverse\n");
    printf("    8. Value                   18. InOrderTraverse\n");
    printf("    9. Assign                  19. PostOrderTraverse\n");
    printf("   10. Parent                  20. LevelOrderTraverse\n");
	printf("                                0. Exit                \n");                    
    printf("-------------------------------------------------------\n");
	printf("    请选择你的操作[0-20]:");
	scanf("%d",&op);
    switch(op){
	   case 1:  //InitBiTree
           flag = InitBiTree(&headp);
           if(flag==TRUE){
                printf("二叉树初始化成功！");
           }
           else if(flag==ERROR){
                printf("二叉树已存在。");
           }
           else{
                printf("二叉树初始化失败！");
           }
           getchar();getchar();
           break;
	   case 2:  //DestroyBiTree
           flag = DestroyBiTree(&headp);
           if(flag==TRUE){
                printf("二叉树销毁成功！");
           }
           else if(flag==ERROR){
                printf("二叉树不存在，请先初始化。");
           }
           else{
                printf("二叉树销毁失败！");
           }
		   getchar();getchar();
		   break;
	   case 3:  //CreateBiTree
           //先判断二叉树是否存在、是否为空
           flag = BiTreeEmpty(headp);
           if(flag==INFEASTABLE){
                a='n'; 
                printf("二叉树不存在，请先初始化。");
           }
           else if(flag==FALSE){
                printf("二叉树不为空，是否覆盖原有二叉树？(Y or N)\n");
                getchar();scanf("%c", &a);
                if(a=='Y' || a=='y'){
                    a='y'; 
                }
           }
           else if(flag==TRUE){
                a='y'; 
           }
           if(a=='y'){
                printf("请输入二叉树的书写形式串：\n");
                printf("(即以#代表空的先根遍历序列)\n");
                scanf("%s", def);
                strnum = 0;
                flag = CreateBiTree(&((*headp).rchild), def);
                if(flag==OK){
                    printf("二叉树创建成功！");
                }
                else{
                    printf("二叉树创建失败！");
                }
           }
		   getchar();getchar();
		   break;
	   case 4:  //ClearBiTree
           flag = ClearBiTree(&headp);
           if(flag==TRUE){
                printf("二叉树清空成功！");
           }
           else if(flag==ERROR){
                printf("二叉树不存在。");
           }
           else{
                printf("二叉树销毁失败！");
           }
		   getchar();getchar();
		   break;
	   case 5:  //BiTreeEmpty
           flag = BiTreeEmpty(headp);
           if(flag==TRUE){
                printf("二叉树为空！");
           }
           else if(flag==FALSE){
                printf("二叉树不为空。");
           }
           else if(flag==INFEASTABLE){
                printf("二叉树不存在。");
           }
           else{
                printf("操作出现未知错误！");
           }
		   getchar();getchar();
		   break;
	   case 6:  //BiTreeDepth
         //先判断二叉树是否存在、是否为空
         flag = BiTreeEmpty(headp);
         if(flag==INFEASTABLE){
            printf("二叉树不存在，请先初始化。");
         }
         else if(flag==TRUE){
            printf("二叉树为空。");
         }
         else{
            printf("树的深度是%d。",BiTreeDepth((*headp).rchild));
         }
         getchar();getchar();
         break;
	   case 7:  //Root
         //先判断二叉树是否存在、是否为空
         flag = BiTreeEmpty(headp);
         if(flag==INFEASTABLE){
            printf("二叉树不存在，请先初始化。");
         }
         else if(flag==TRUE){
            printf("二叉树为空。");
         }
         else{
            printf("树的根节点的值是%c。",Root(headp).data);
         }
		 getchar();getchar();
		 break;
	   case 8:  //Value
         printf("请输入要查询的节点：\n");
         getchar();scanf("%c", &a);
         re = Value(headp,a);
         if(re==NULL){
            printf("要查询的节点不存在。\n");
         }
         else{
            printf("要查询的节点的值是：%c。\n",re->data);
         }
		 getchar();getchar();
		 break;
	   case 9:  //Assign
         printf("请输入要修改的节点：\n");
         getchar();scanf("%c", &a);
         printf("请输入要修改成什么值：\n");
         getchar();scanf("%c", &b);
         flag = Assign(headp,a,b);
         if(flag==OK){
            printf("修改成功。\n");
         }
         else{
            printf("修改失败。\n");
         }
		 getchar();getchar();
		 break;
	   case 10:  //Parent
         printf("请输入要查询的节点：\n");
         getchar();scanf("%c", &a);
         re = Parent(headp,a);
         if(re==NULL){
            printf("未查询到该节点的父节点。\n");
         }
         else{
            printf("要查询的节点的父节点是：%c。\n",re->data);
         }
		 getchar();getchar();
		 break;
		 getchar();getchar();
		 break;
	   case 11:  //LeftChild
         printf("请输入要查询的节点：\n");
         getchar();scanf("%c", &a);
         re = LeftChild(headp,a);
         if(re==NULL){
            printf("未查询到该节点的左孩子节点。\n");
         }
         else{
            printf("要查询的节点的左孩子节点是：%c。\n",re->data);
         }
		 getchar();getchar();
		 break;
	   case 12:  //ReftChild
         printf("请输入要查询的节点：\n");
         getchar();scanf("%c", &a);
         re = ReftChild(headp,a);
         if(re==NULL){
            printf("未查询到该节点的右孩子节点。\n");
         }
         else{
            printf("要查询的节点的右孩子节点是：%c。\n",re->data);
         }
		 getchar();getchar();
		 break;
	   case 13:  //LeftSibling
         printf("请输入要查询的节点：\n");
         getchar();scanf("%c", &a);
         re = LeftSibling(headp,a);
         if(re==NULL){
            printf("未查询到该节点的左兄弟节点。\n");
         }
         else{
            printf("要查询的节点的左兄弟节点是：%c。\n",re->data);
         }
		 getchar();getchar();
		 break;
	   case 14:  //ReftSibling
         printf("请输入要查询的节点：\n");
         getchar();scanf("%c", &a);
         re = ReftSibling(headp,a);
         if(re==NULL){
            printf("未查询到该节点的右兄弟节点。\n");
         }
         else{
            printf("要查询的节点的右兄弟节点是：%c。\n",re->data);
         }
		 getchar();getchar();
		 break;
	   case 15:  //InsertChild
         flag = BiTreeEmpty(headp);
         if(flag==INFEASTABLE){
            printf("二叉树不存在，请先初始化。");
         }
         else if(flag==TRUE){
            printf("二叉树为空。");
         }
         else{
                printf("请输要插入的子二叉树的书写形式串：\n");
                printf("(要求其右子树为空，否则会被删除)\n");
                printf("(要求输入的新树关键字与老树不重复)\n");
                printf("(即以#代表空的先根遍历序列)\n");
                scanf("%s", def);
                strnum = 0;
                InitBiTree(&c);
                flag = CreateBiTree(&((*c).rchild), def);
                if(flag==OK){
                    printf("请输入要插入子树的节点：\n");
                    getchar();scanf("%c", &a);
                    printf("请选择要插入左子树还是右子树：(L or R)\n");
                    getchar();scanf("%c", &b);
                    if(b=='l'||b=='L') lr=0;
                    else lr=1;
                    flag = InsertChild(headp, a, lr, c);
                    if(flag==OK){
                        printf("插入子二叉树成功。\n");
                    }
                    else{
                        printf("插入子二叉树失败。\n");
                    }
                }
                else{
                    printf("子二叉树创建失败！");
                }
         }
		 getchar();getchar();
		 break;
	   case 16:  //DeleteChild
         //先判断二叉树是否存在、是否为空
         flag = BiTreeEmpty(headp);
         if(flag==INFEASTABLE){
            printf("二叉树不存在，请先初始化。");
         }
         else if(flag==TRUE){
            printf("二叉树为空。");
         }
         else{
            printf("请输入要删除子树的节点：\n");
            getchar();scanf("%c", &a);
            printf("请选择要删除左子树还是右子树：(L or R)\n");
            getchar();scanf("%c", &b);
            if(b=='l'||b=='L') lr=0;
            else lr=1;
            flag = DeleteChild(headp,a,lr);
            if(flag==TRUE){
                 printf("子树删除成功！");
            }
            else if(flag==ERROR){
                 printf("子树删除失败，");
                 if(lr==0) printf("左子树不存在。");
                 else printf("右子树不存在。");
            }
            else if(flag==INFEASTABLE){
                 printf("操作失败，输入的节点不存在！");
            }
         }
		 getchar();getchar();
		 break;
	   case 17:  //PreOrderTraverse
         //先判断二叉树是否存在、是否为空
         flag = BiTreeEmpty(headp);
         if(flag==INFEASTABLE){
            printf("二叉树不存在，请先初始化。");
         }
         else if(flag==TRUE){
            printf("二叉树为空。");
         }
         else{
            PreOrderTraverse((*headp).rchild);
         }
		 getchar();getchar();
		 break;
	   case 18:  //InOrderTraverse
         //先判断二叉树是否存在、是否为空
         flag = BiTreeEmpty(headp);
         if(flag==INFEASTABLE){
            printf("二叉树不存在，请先初始化。");
         }
         else if(flag==TRUE){
            printf("二叉树为空。");
         }
         else{
            InOrderTraverse((*headp).rchild);
         }
		 getchar();getchar();
		 break;
	   case 19:  //PostOrderTraverse
         //先判断二叉树是否存在、是否为空
         flag = BiTreeEmpty(headp);
         if(flag==INFEASTABLE){
            printf("二叉树不存在，请先初始化。");
         }
         else if(flag==TRUE){
            printf("二叉树为空。");
         }
         else{
            PostOrderTraverse((*headp).rchild);
         }
		 getchar();getchar();
		 break;
	   case 20:  //LevelOrderTraverse
         //先判断二叉树是否存在、是否为空
         flag = BiTreeEmpty(headp);
         if(flag==INFEASTABLE){
            printf("二叉树不存在，请先初始化。");
         }
         else if(flag==TRUE){
            printf("二叉树为空。");
         }
         else{
            LevelOrderTraverse((*headp).rchild);
         }
		 getchar();getchar();
		 break;
	   case 0:
         break;
       default:
         printf("输入无效，请重新输入");
         getchar();getchar();
         break;
	}//end of switch
  }//end of while
  printf("欢迎下次再使用本系统！\n");
  return 0;
}//end of main()
status InitBiTree(BiTree *headp){   //1
    //初始条件是二叉树 T 不存在;
    //操作结果是构造空二叉树 T
    //也就是让头指针指向头节点
    if(*headp!=NULL) return ERROR;
    *headp = CreateNode();
    return OK;
}//end of InitBiTree
status DestroyBiTree(BiTree *headp){    //2
    //初始条件是二叉树 T 已存在;
    //操作结果是销毁二叉树 T
    if(*headp==NULL) return ERROR;
    //释放二叉树占据的内存空间
    if((**headp).lchild!=NULL){
        DestroyBiTree(&((**headp).lchild));
    }
    if((**headp).rchild!=NULL){
        DestroyBiTree(&((**headp).rchild));
    }
    free(*headp);
    *headp = NULL;
    return OK;
}//end of DestroyBiTree
status CreateBiTree(BiTree *root, char *definition){    //3
    //初始条件是 definition 给出二叉树 T 的定义
    //操作结果是按 definition 构造二叉树 T
    // definition 是以#代表空的先根遍历序列
    //注意第一个参数不是头指针，而是根节点(为便于递归)
    if(strnum>strlen(definition)) return;
    if(definition[strnum]=='#'){
        strnum++;
        return;
    }
    *root = CreateNode();  
    (**root).data = definition[strnum++];
    if(definition[strnum]!='#'){
        (**root).lchild = CreateNode();
        (**root).lchild->data = definition[strnum++];
        CreateBiTree(&((**root).lchild->lchild), definition);
        CreateBiTree(&((**root).lchild->rchild), definition);
    }
    else{
        strnum++;
    }
    if(definition[strnum]!='#'){
        (**root).rchild = CreateNode();
        (**root).rchild->data = definition[strnum++];
        CreateBiTree(&((**root).rchild->lchild), definition);
        CreateBiTree(&((**root).rchild->rchild), definition);
    }
    else{
        strnum++;
    }
    return OK;
}//end of CreateBiTree
status ClearBiTree(BiTree *headp){  //4
    //初始条件是二叉树 T 存在;
    //操作结果是将二叉树 T 清空。
    //这一操作并不销毁头节点
    if(*headp==NULL) return ERROR;
    //释放二叉树占据的内存空间
    if((**headp).lchild!=NULL){
        DestroyBiTree(&((**headp).lchild));
    }
    if((**headp).rchild!=NULL){
        DestroyBiTree(&((**headp).rchild));
    }
    (**headp).lchild=NULL;
    (**headp).rchild=NULL;
    return OK;
}//end of ClearBiTree
status BiTreeEmpty(BiTree headp){   //5
    //初始条件是二叉树 T 存在;
    //操作结果是若 T 为空二叉树则返回 TRUE,否则返回 FALSE。
    if(headp==NULL) return INFEASTABLE;
    if((*headp).rchild==NULL){
        return TRUE; 
    }
    else{
        return FALSE;
    }
}//end of BiTreeEmpty
int BiTreeDepth(BiTree root){       //6
    //初始条件是二叉树 T 存在;
    //操作结果是返回 T 的深度。
    int depth=0;
    int rd = 0;//右子树深度
    int ld = 0;//左子树深度
    if(root==NULL) return 0;
    rd = BiTreeDepth(root->rchild);
    ld = BiTreeDepth(root->lchild);
    if(rd>=ld){
        depth = rd+1;
    } 
    else{
        depth = ld+1;
    }
    return depth;
}//end of BiTreeDepth
BiTNode Root(BiTree headp){           //7
    //初始条件是二叉树 T 已存在
    //操作结果是返回 T 的根
    return *(headp->rchild);
}//end of Root
BiTree Value(BiTree headp, ElemType a){//8
    //初始条件是二叉树 T 已存在,a 是 T
    //中的某个结点;操作结果是返回指向 a 的指针。
    BiTree e=NULL;
    BiTree root=NULL;
    if((headp==NULL)||((*headp).rchild==NULL)) return NULL;
    root=headp->rchild;
    LinkQueue Q;
    InitQueue(&Q);
    EnQueue(&Q,root);
    while(QueueEmpty(Q)!=TRUE){
        DeQueue(&Q,&e);
        if(e->data==a){
            DestroyQueue(&Q);
            return e;
        }
        if(e->lchild!=NULL){
            EnQueue(&Q, e->lchild);
        }
        if(e->rchild!=NULL){
            EnQueue(&Q, e->rchild);
        }
    }
    DestroyQueue(&Q);
    return NULL;
}//end of Value
status Assign(BiTree headp, ElemType o, ElemType n){   //9
    //初始条件是二叉树 T 已存在,
    //e 是 T 中的某个结点;操作结果是结点 e 赋值为 value。
    BiTree temp=NULL;
    temp = Value(headp, o);
    if(temp==NULL){
        return ERROR;
    }
    else{
        temp->data=n;
        return OK;
    }
}//end of Assign
BiTree Parent(BiTree headp, ElemType a){                //10
    //初始条件是二叉树 T 已存在, a 是 T 中的某个结点
    //操作结果是若 a 是 T 的非根结点,则返回它的双亲结点指针,否则返回 NULL。
    BiTree e=NULL;
    BiTree root=NULL;
    if((headp==NULL)||((*headp).rchild==NULL)) return NULL;
    root=headp->rchild;
    if(root->data==a) return NULL;
    LinkQueue Q;
    InitQueue(&Q);
    EnQueue(&Q,root);
    while(QueueEmpty(Q)!=TRUE){
        DeQueue(&Q,&e);
        if(e->lchild!=NULL){
            if(e->lchild->data==a){
                DestroyQueue(&Q);
                return e;
            }
            EnQueue(&Q, e->lchild);
        }
        if(e->rchild!=NULL){
            if(e->rchild->data==a){ 
                DestroyQueue(&Q);
                return e;
            }
            EnQueue(&Q, e->rchild);
        }
    }
    DestroyQueue(&Q);
    return NULL;
}//end of Parent
BiTree LeftChild(BiTree headp, ElemType e){            //11
    //初始条件是二叉树 T 存在, e 是 T 中某个节点
    //操作结果是返回 e 的左孩子结点指针。若 e 无左孩子,则返 回 NULL。
    BiTree temp=NULL;
    temp = Value(headp, e);
    if(temp==NULL) return NULL;
    return temp->lchild;
}//end of LeftChild
BiTree ReftChild(BiTree headp, ElemType e){            //12
    //初始条件是二叉树 T 存在, e 是 T 中某个节点
    //操作结果是返回 e 的右孩子结点指针。若 e 无左孩子,则返 回 NULL。
    BiTree temp=NULL;
    temp = Value(headp, e);
    if(temp==NULL) return NULL;
    return temp->rchild;
}//end of ReftChild
BiTree LeftSibling(BiTree headp,ElemType e){           //13
    //初始条件是二叉树 T 存在,e 是 T 中某个结点
    //操作结果是返回 e 的左兄弟结点指针
    //若 e 是 T 的左孩子或者无左兄弟,则返回 NULL
    BiTree temp=NULL;
    temp = Parent(headp, e);
    if(temp==NULL) return NULL;
    if((temp->lchild!=NULL)&&(temp->lchild->data!=e)){
        return temp->lchild;
    }
    return NULL;
}//end of LeftSibling
BiTree ReftSibling(BiTree headp,ElemType e){           //14
    //初始条件是二叉树 T 存在,e 是 T 中某个结点
    //操作结果是返回 e 的右兄弟结点指针
    //若 e 是 T 的右孩子或者无右兄弟,则返回 NULL
    BiTree temp=NULL;
    temp = Parent(headp, e);
    if(temp==NULL) return NULL;
    if((temp->rchild!=NULL)&&(temp->rchild->data!=e)){
        return temp->rchild;
    }
    return NULL;
}//end of ReftSibling
status InsertChild(BiTree headp,ElemType e,int LR,BiTree c){   //15
    //初始条件是二叉树 T 存在, e 是 T 中的某个结点,LR 为 0 或 1,
    //非空二叉树 c 与 T 不相交且右子树为空,不为空则删除其右子树
    //操作结果是根据 LR 为 0 或者 1,插入 c 为 T 中 p 所指结点的左或右子树
    //e 的原有左子树或右子树则为 c 的右子树。
    BiTree temp=NULL;
    if(c->rchild==NULL) return INFEASTABLE;
    //若右子树存在则删除
    if(c->rchild->rchild!=NULL)
        DeleteChild(c,Root(c).data,1);
    temp = Value(headp, e);   
    if(temp==NULL) return ERROR;
    if(LR==0){
        c->rchild->rchild=temp->lchild;
        temp->lchild=c->rchild;
        return OK;
    }
    else if(LR==1){
        c->rchild->rchild=temp->rchild;
        temp->rchild=c->rchild;
        return OK;
    }
    else{
        return ERROR;
    }
}//end of InsertChild
status DeleteChild(BiTree headp,ElemType e,int LR){    //16
    //初始条件是二叉树 T 存在, e 是 T 中的某个结点,LR 为 0 或 1
    //操作结果是根据 LR 为 0 或者 1,删除 c 为 T 中 p 所指结点的左或右子树
    BiTree temp=NULL;
    if(headp==NULL) return INFEASTABLE;
    temp = Value(headp,e);
    if(temp==NULL) return INFEASTABLE;
    if(LR==0){//删除左子树
        if(temp->lchild!=NULL){
            DestroyBiTree(&(temp->lchild));
            return OK;
        }
        return ERROR;
    }
    else if(LR==1){//删除右子树
        if(temp->rchild!=NULL){
            DestroyBiTree(&(temp->rchild));
            return OK;
        }
        return ERROR;
    }
    else{
        return ERROR;
    }
}//end of DeleteChild
void PreOrderTraverse(BiTree root){  //17
    //始条件是二叉树 T 存在,Visit 
    //操作结果:先序遍历 t,打印每个结点一次且一次
    if(root==NULL) return;
    printf("%c ",(*root).data);
    PreOrderTraverse((*root).lchild);
    PreOrderTraverse((*root).rchild);
}//end of PreOrderTraverse
void InOrderTraverse(BiTree root){  //18
    //始条件是二叉树 T 存在,Visit 
    //操作结果:中序遍历 t,打印每个结点一次且一次
    if(root==NULL) return;
    InOrderTraverse((*root).lchild);
    printf("%c ",(*root).data);
    InOrderTraverse((*root).rchild);
}//end of InOrderTraverse
void PostOrderTraverse(BiTree root){  //19
    //始条件是二叉树 T 存在,Visit 
    //操作结果:中序遍历 t,打印每个结点一次且一次
    if(root==NULL) return;
    PostOrderTraverse((*root).lchild);
    PostOrderTraverse((*root).rchild);
    printf("%c ",(*root).data);
}//end of InOrderTraverse
void LevelOrderTraverse(BiTree root){   //20
    //始条件是二叉树 T 存在,Visit 
    //操作结果:层序遍历 t,打印每个结点一次且一次
    BiTree e=NULL;
    if(root==NULL) return;
    LinkQueue Q;
    InitQueue(&Q);
    EnQueue(&Q,root);
    while(QueueEmpty(Q)!=TRUE){
        DeQueue(&Q,&e);
        printf("%c ",e->data);
        if(e->lchild!=NULL){
            EnQueue(&Q, e->lchild);
        }
        if(e->rchild!=NULL){
            EnQueue(&Q, e->rchild);
        }
    }
    DestroyQueue(&Q);
}//end of LevelOrderTraverse

//辅助函数
BiTree CreateNode(){
    //操作结果是创建一个新的节点，左右指针置空
    //返回指向这个节点的指针
    BiTree p;
    p = (BiTree)malloc(sizeof(BiTNode));
    if(!p) exit(OVERFLOW);
    (*p).lchild=NULL;
    (*p).rchild=NULL;
    return p;
}//end of CreateNode

//队列相关的函数
status InitQueue(LinkQueue *Q){
    //构造一个新队列
    (*Q).front = (*Q).rear = (QueuePtr)malloc(sizeof(BiTree));
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
status EnQueue(LinkQueue *Q, BiTree e){
    //插入元素e为Q的新的队尾元素
    QueuePtr p;
    p = (QueuePtr)malloc(sizeof(BiTree));
    if(!p) exit(INFEASTABLE);
    p->data=e;
    p->next=NULL;
    Q->rear->next=p;
    Q->rear=p;
    return OK;
}//end EnQueue
status DeQueue(LinkQueue *Q, BiTree *e){
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
