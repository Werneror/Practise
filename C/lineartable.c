/* Linear Table On Sequence Structure */
#include <stdio.h>
#include <malloc.h>
#include <stdlib.h>

/*---------page 10 on textbook ---------*/
#define TRUE 1
#define FALSE 0
#define OK 1
#define ERROR 0
#define INFEASTABLE -1
#define OVERFLOW -2

typedef int status;
typedef int ElemType; //数据元素类型定义

/*-------page 22 on textbook -------*/
#define LIST_INIT_SIZE 100
#define LISTINCREMENT  10
#define LONG 100    //最多管理LONG个线性表
typedef struct{  //顺序表（顺序结构）的定义
	ElemType * elem;    //存储空间基址
	int length;         //当前长度
	int listsize;       //当前分配的存储容量
}SqList;
/*-----page 19 on textbook ---------*/
status IntiaList(SqList *L);
status DestroyList(SqList *L);
status ClearList(SqList *L);
status ListEmpty(SqList L);
int ListLength(SqList L);
status GetElem(SqList L,int i,ElemType *e);
int LocateElem(SqList L,ElemType e, status compare(ElemType a, ElemType b));
status PriorElem(SqList L,ElemType cur,ElemType *pre_e);
status NextElem(SqList L,ElemType cur,ElemType * next_e);
status ListInsert(SqList *L,int i,ElemType e);
status ListDelete(SqList *L,int i,ElemType *e);
status ListTrabverse(SqList L, status visit(ElemType e));
status LoadListFromFile(SqList *L, char* filename);
status ExportListToFile(SqList L, char* filename);
status SaveProject(SqList Ls[], char* projiectname);
status OpenProject(SqList Ls[], char* projiectname);
status equal(ElemType a, ElemType b);
status print(ElemType e);
/*--------------------------------------------*/
int main(){
  SqList *L;
  SqList Ls[LONG];    //为管理多个列表创建数组
  ElemType e;   // 用做实参
  ElemType d;   // 用做实参
  short flag=0;   //用作标志变量
  int tail=0;   //总是Ls列表的最后一个元素的下一个元素的下标
  int op=1;
  int id=1; //该变量存储线用户输入的ID，其实质是Ls数组下表
  int st;   //存储函数返回值或作为循环变量计数
  int i;    //用做实参
  char a;
  char filename[30];
  char projiectname[30]="";
  for(st=0;st<LONG;++st){
    Ls[st].elem=NULL;
    Ls[st].length=0;
    Ls[st].listsize=0;
  }
  while(op){
    system("clear");
    printf("\n");
	printf("      Menu for Linear Table On Sequence Structure \n");
	printf("-------------------------------------------------\n");
	printf("   0. Exit	              9. NextElem\n");
	printf("   1. IntiaList    	      10. ListInsert\n");
	printf("   2. DestroyList  	      11. ListDelete\n");
	printf("   3. ClearList    	      12. ListTrabverse\n");
	printf("   4. ListEmpty    	      13. ShowAllList\n");
	printf("   5. ListLength   	      14. ExportListToFile\n");
	printf("   6. GetElem      	      15. LoadListFromFile\n");
	printf("   7. LocateElem              16. OpenProject\n");
    printf("   8. PriorElem               17. SaveProject\n");
    printf("-------------------------------------------------\n");
	printf("    请选择你的操作[0-16]:");
	scanf("%d",&op);
	if(op>1 && op<15 && op!=13){
        printf("请指定要操作的线性表ID（用13查看已有的线性表）：");
        scanf("%d",&id);
        printf("\n");
        if(Ls[id].elem==NULL){
             printf("线性表不存在！\n");
             getchar();getchar();
             continue;
        }
        L = &Ls[id];
	}
    switch(op){
	   case 1:  //IntiaList
         if(tail>=LONG){
            printf("可管理的线性表已达上线，新建失败！\n");
            break;
         }
	     L = &Ls[tail];
         st = IntiaList(L);
		 if(st==OK){
            printf("线性表创建成功，ID=%d\n", tail);
            tail++;
         }
		 else if(st==INFEASTABLE){
            printf("线性表已存在！\n");
         }
		 else{
            printf("线性表创建失败！\n");
         }
		 getchar();getchar();
		 break;
	   case 2:  //DestroyList
         st = DestroyList(L);
		 if(st==OK){
            printf("线性表销毁成功！\n");
         }
		 else if(st==INFEASTABLE){
            printf("线性表不存在！\n");
         }
         else{
            printf("线性表销毁失败！\n");
         }
		 getchar();getchar();
		 break;
	   case 3:  //ClearList
         st = ClearList(L);
		 if(st==OK){
            printf("线性表清空成功！\n");
         }
		 else if(st==INFEASTABLE){
            printf("线性表不存在！\n");
         }
		 else printf("线性表清空失败！\n");
		 getchar();getchar();
		 break;
	   case 4:  //ListEmpty
         st = ListEmpty(*L);
		 if(st==TRUE){
            printf("线性表为空！\n");
         }
		 else if(st==INFEASTABLE){
            printf("线性表不存在！\n");
         }
		 else printf("线性表非空！\n");
		 getchar();getchar();
		 break;
	   case 5:  //ListLength
         st = ListLength(*L);
		 if(st==INFEASTABLE){
            printf("线性表不存在！\n");
         }
         else{
            printf("表长为：%d", st);
         }
		 getchar();getchar();
		 break;
	   case 6:  //GetElem
         printf("请输入将要取其值的元素的位置:");
         scanf("%d",&i);
         st = GetElem(*L, i, &e);
		 if(st==INFEASTABLE){
            printf("线性表不存在！\n");
         }
         else if(st==ERROR){
            printf("参数i非法，请检查表长！\n");
         }
         else if(st==OK){
            printf("取值成功，其值为%d！\n", e);
         }
         else{
            printf("未知错误！");
         }
		 getchar();getchar();
		 break;
	   case 7:  //LocateElem
         printf("请输入想要查询的元素的值:");
         scanf("%d",&e);
         st = LocateElem(*L, e, equal);
		 if(st==INFEASTABLE){
            printf("线性表不存在！\n");
         }
         else if(st==0){
            printf("未匹配到该元素。");
         }
         else{
            printf("该元素第一次出现是在位序为%d处。",st);
         }
		 getchar();getchar();
		 break;
	   case 8:  //PriorElem
         printf("请输入目标元素的值:");
         scanf("%d",&e);
         st = PriorElem(*L, e, &d);
		 if(st==INFEASTABLE){
            printf("线性表不存在！\n");
         }
         else if(st==ERROR){
            printf("前驱节点不存在！");
         }
         else if(st==OK){
            printf("该元素前驱节点的值是：%d。", d);
         }
         else{
            printf("未知错误！");
         }
		 getchar();getchar();
		 break;
	   case 9:  //NextElem
         printf("请输入目标元素的值:");
         scanf("%d",&e);
         st = NextElem(*L, e, &d);
		 if(st==INFEASTABLE){
            printf("线性表不存在！\n");
         }
         else if(st==ERROR){
            printf("后继节点不存在！");
         }
         else if(st==OK){
            printf("该元素后继节点的值是：%d。", d);
         }
         else{
            printf("未知错误！");
         }
		 getchar();getchar();
		 break;
	   case 10: //ListInsert
         printf("请输入将要插入的元素的位置:");
         scanf("%d",&i);
         printf("\n请输入将要插入的元素的值:");
         scanf("%d",&e);
         st = ListInsert(L, i, e);
		 if(st==INFEASTABLE){
            printf("线性表不存在！\n");
         }
         else if(st==ERROR){
            printf("参数i非法，请检查表长！\n");
         }
         else if(st==OK){
            printf("插入元素成功！\n");
         }
         else{
            printf("未知错误！\n");
         }
		 getchar();getchar();
		 break;
	   case 11: //ListDelete
         printf("请输入要删除元素的位置:\n");
         scanf("%d",&i);
         st = ListDelete(L, i, &e);
		 if(st==INFEASTABLE){
            printf("线性表不存在！\n");
         }
         else if(st==ERROR){
            printf("参数i非法，请检查表长！\n");
         }
         else if(st==OK){
            printf("删除元素成功，被删除的元素是%d！\n", e);
         }
         else{
            printf("未知错误！\n");
         }
		 getchar();getchar();
		 break;
	   case 12: //ListTrabverse
         printf("\n-----------all elements -----------------------\n");
         st = ListTrabverse(*L, print);
         printf("\n------------------ end ------------------------\n");
		 if(st==INFEASTABLE){
            printf("线性表不存在！\n");
         }
		 if(st==0){
            printf("线性表是空表！\n");
         }
		 getchar();getchar();
		 break;
	   case 13: //ShowAllList
         flag=1;
         printf("已有的线性表ID是：\n");
         for(st=0;st<LONG;++st){
            if(Ls[st].elem!=NULL){
                printf("%d  ", st);
                flag = 0;
            }
         }
         printf("\n");
         if(flag) printf("目前还没有一个线性表。\n");
		 getchar();getchar();
		 break;
	   case 14: //ExportListToFile
         printf("请指定文件名：");
         scanf("%s",filename);
         st = ExportListToFile(*L, filename);
		 if(st==INFEASTABLE){
            printf("线性表不存在，保存失败！\n");
         }
		 else if(st==ERROR){
            printf("文件打开错误，保存失败！\n ");
         }
         else if(st==OK){
            printf("线性表已成功保存到文件%s！",filename);
         }
         else{
            printf("未知错误！");
         }
		 getchar();getchar();
		 break;
	   case 15: //LoadListFromFile
         if(tail>=LONG){
            printf("可管理的线性表已达上线，无法载入新的线性表！\n");
            break;
         }
         printf("请指定文件名：");
         scanf("%s",filename);
	     L = &Ls[tail];
         st = LoadListFromFile(L, filename);
		 if(st==ERROR){
            printf("线性表载入失败！\n");
         }
         else if(st==OK){
            printf("已从文件%s成功载入线性表，ID=%d",filename,tail);
            tail++;
         }
         else{
            printf("未知错误！");
         }
		 getchar();getchar();
		 break;
	   case 16: //OpenProject
         flag=1;
         for(st=0;st<LONG;++st){
            if(Ls[st].elem!=NULL){
                flag = 0;
            }
         }
         if(flag==0){
            printf("是否保存当前项目？y/n\n");
            getchar();
            scanf("%c",&a);
            if(a=='y' || a=='Y'){
                 if(projiectname[0]=='\0'){    //若尚未指定项目名称
                    printf("本项目尚未命名，请指定项目名（一旦指定，不可修改）：");
                    scanf("%s",projiectname);
                    printf("项目命名成功!\n");
                 }
                 st = SaveProject(Ls, projiectname);
                 if(st==ERROR){
                    printf("文件打开错误，项目保存失败！\n ");
                 }
                 else if(st==OK){
                    printf("项目%s已成功保存！", projiectname);
                 }
                 else{
                    printf("未知错误！");
                 }
            }
         }
         printf("请输入想要打开的项目的名称：");
         scanf("%s",projiectname);
         st = OpenProject(Ls, projiectname);
         if(st==INFEASTABLE){
            printf("项目打开失败，请确认项目名。\n ");
         }
         else{
            tail = st;
            printf("项目%s已成功打开！", projiectname);
         }
		 getchar();getchar();
		 break;
	   case 17: //SaveProject
         if(projiectname[0]=='\0'){    //若尚未指定项目名称
            printf("本项目尚未命名，请指定项目名（一旦指定，不可修改）：");
            scanf("%s",projiectname);
            printf("项目命名成功!\n");
         }
         st = SaveProject(Ls, projiectname);
		 if(st==ERROR){
            printf("文件操作错误，项目保存失败！\n ");
         }
         else if(st==OK){
            printf("项目%s已成功保存！", projiectname);
         }
         else{
            printf("未知错误！");
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
/*--------page 23 on textbook --------------------*/
status IntiaList(SqList *L){
    //初始条件是线性表 L 不存在
    //操作结果是构造一个空的线性表
    if((*L).elem!=NULL) return INFEASTABLE;
	(*L).elem = (ElemType *)malloc( LIST_INIT_SIZE * sizeof (ElemType));
    if(!(*L).elem) exit(OVERFLOW);
	(*L).length=0;
    (*L).listsize=LIST_INIT_SIZE;
	return OK;
}//end of IntiaList
status DestroyList(SqList *L){
    //初始条件是线性表L已存在
    //操作结果是销毁线性表L
    if((*L).elem==NULL) return INFEASTABLE;
    free((*L).elem);
    (*L).elem = NULL;
    (*L).length = 0;
    (*L).listsize = 0;
    return OK;
}//end of DestroyList
status ClearList(SqList *L){
    //初始条件是线性表L已存在
    //操作结果是将L重置为空表
    if((*L).elem==NULL) return INFEASTABLE;
    (*L).length = 0;
    return OK;
}//end of ClearList
status ListEmpty(SqList L){
    //初始条件是线性表L已存在
    //操作结果是若L为空表则返回TRUE,否则返回FALSE
    if(L.elem==NULL) return INFEASTABLE;
    if(L.length==0) return TRUE;
    else return FALSE;
}//end of ListEmpty
int ListLength(SqList L){
    //初始条件是线性表已存在
    //操作结果是返回L中数据元素的个数
    if(L.elem==NULL) return INFEASTABLE;
    return L.length;
}//end of ListLength
status GetElem(SqList L,int i,ElemType *e){
   //初始条件是线性表已存在,1≤i≤L.length
   //操作结果是用e返回L中第i个数据元素的值
    if(L.elem==NULL) return INFEASTABLE;
    if(i<1 || i>L.length) return ERROR;
    (*e) = L.elem[i-1];
    return OK;
}//end of GetElem
int LocateElem(SqList L,ElemType e, status compare(ElemType a, ElemType b)){
    //始条件是线性表已存在
    //操作结果是返回L中第1个与e满足关系compare()关系的数据元素的位序
    //若这样的数据元素不存在,则返回值为0
    int i;
    if(L.elem==NULL) return INFEASTABLE;
    for(i=0;i<L.length;++i){
        if(compare(e, L.elem[i])==TRUE) return i+1;
    }
    return 0;
}//end of LocateElem
status PriorElem(SqList L,ElemType cur,ElemType *pre_e){
    //初始条件是线性表L已存在
    //操作结果是若cur_e是L的数据元素,且不是第一个
    //则用pre_e返回它的前驱,否则操作失败,pre_e无定义
    int pos;    //存放cur的位序
    if(L.elem==NULL) return INFEASTABLE;
    pos = LocateElem(L, cur, equal);
    if(pos==0||pos==1) return ERROR;
    else{
        (*pre_e) = L.elem[pos-2];
        return OK;
    }
}//end of PriorElem
status NextElem(SqList L,ElemType cur,ElemType *next_e){
    //初始条件是线性表L已存在
    //操作结果是若cur_e是L的数据元素,且不是最后一个
    //则用next_e返回它的后继,否则操作失败,next_e无定义
    int pos;    //存放cur的位序
    if(L.elem==NULL) return INFEASTABLE;
    pos = LocateElem(L, cur, equal);
    if(pos==0||pos==ListLength(L)) return ERROR;
    else{
        (*next_e) = L.elem[pos];
        return OK;
    }
}//end of NextElem
status ListInsert(SqList *L,int i,ElemType e){
    //初始条件是线性表L已存在,1≤i≤L.length+1
    //操作结果是在L的第i个位置之前插入新的数据元素e
    int j;
    if((*L).elem==NULL) return INFEASTABLE;
    if(i<1||i>(*L).length+1) return ERROR;
    if((*L).length>=(*L).listsize){ //列表已经存满，需扩大空间
        (*L).elem = (ElemType*)realloc((*L).elem, ((*L).listsize+LISTINCREMENT)*sizeof(ElemType));
        if(!(*L).elem) exit(OVERFLOW);
        (*L).listsize += LISTINCREMENT;
    }
    for(j=(*L).length;j>=i;j--){ //把从第i个位置起的元素都向后移一位
        (*L).elem[j]=(*L).elem[j-1];
    }
    (*L).elem[i-1] = e;
    ++(*L).length;  //表长加1
    return OK;
}//end of ListInsert
status ListDelete(SqList *L,int i,ElemType *e){
    //初始条件是线性表L已存在且非空,1≤i≤ListLength(L)
    //操作结果:删除L的第i个数据元素,用e返回其值
    int j;
    if((*L).elem==NULL) return INFEASTABLE;
    if((*L).length==0 || i<1 || i>(*L).length) return ERROR;
    (*e) = (*L).elem[i-1];
    for(j=i-1;j<(*L).length-1;j++){ //把要删除元素后的各元素向前移动一位
        (*L).elem[j]=(*L).elem[j+1];
    }
    --(*L).length;
    return OK;
}//end of ListDelete
status ListTrabverse(SqList L, status visit(ElemType e)){
    //初始条件是线性表L已存在
    //操作结果是依次对L的每个数据元素调用函数visit()
    //一旦visit()失败，则操作失败
    int i;
    if(L.elem==NULL) return INFEASTABLE;
    for(i=0;i<L.length;i++){
        if(visit(L.elem[i])==ERROR) return ERROR;
    }
    return L.length;
}//end of ListTrabverse
status LoadListFromFile(SqList *L, char* filename){
    //操作结果是将以filename为名的文件中线性表载入到线性表L
    //若线性表L以存在，将会被覆盖，若L不存在，则会新建一个
    FILE *fp;
    ElemType temp;
    char a;
    if((fp=fopen(filename,"r"))==NULL) return ERROR;
    if((*L).elem==NULL){    //线性表不存在，则创建一个
        IntiaList(L);
    }
    else{
        printf("线性表已存在，此举将覆盖已有数据，是否继续？y/n\n");
        getchar();
        scanf("%c",&a);
        if(a!='y' && a!='Y') return ERROR;
    }
    if(ClearList(L)==INFEASTABLE) return ERROR;   //清空线性表
    while(fread(&temp, sizeof(ElemType), 1, fp)){
        ListInsert(L,(*L).length+1,temp);
    }
    fclose(fp);
    return OK;
}//end of LoadListFromFile
status ExportListToFile(SqList L, char* filename){
    //初始条件是线性表L存在
    //操作结果是保存线性表L到以filename为名的文件中
    FILE *fp;
    if(L.elem==NULL) return INFEASTABLE;
    if((fp=fopen(filename,"w"))==NULL) return ERROR;
    //顺序存储的线性表物理地址相邻，所以选择简单的一次写入文件
    fwrite(L.elem,sizeof(ElemType),L.length,fp);
    fclose(fp);
    return OK;
}//end of ExportListToFile
status SaveProject(SqList Ls[], char* projietname){
    //初始条件是项目中至少有一个列表
    //操作结果是将整个项目保存到文件
    FILE *fp;
    int st=0;
    if((fp=fopen(projietname,"w"))==NULL) return ERROR;
    for(st=0;st<LONG;++st){
        if(Ls[st].elem!=NULL){
                fwrite(&Ls[st].length, sizeof(int), 1, fp);
                fwrite(Ls[st].elem,sizeof(ElemType),Ls[st].length,fp);
         }
    }
    return OK;
}//end of SaveProject
status OpenProject(SqList Ls[], char* projiectname){
    //初始条件是projiectname对应的文件存在且正确
    //操作结果是保存线性表L到以filename为名的文件中
    int st;
    int id=0;
    int tail=0;
    int length;
    FILE *fp;
    ElemType temp;
    if((fp=fopen(projiectname,"r"))==NULL) return INFEASTABLE;
    for(st=0;st<LONG;++st){ //清空Ls
        Ls[st].elem=NULL;
        Ls[st].length=0;
        Ls[st].listsize=0;
    }
    while(fread(&temp, sizeof(ElemType), 1, fp)){
        length = temp;
        IntiaList(&Ls[id]);
        for(st=0;st<length;++st){
            fread(&temp, sizeof(ElemType), 1, fp);
            ListInsert(&Ls[id],Ls[id].length+1,temp);
        }
        ++id;
        ++tail;
        if(id>=LONG){
            printf("可管理的线性表已达上线，不在载入！\n");
            break;
        }
    }
    fclose(fp);
    return tail;
}//end of OpenListToFile
status equal(ElemType a, ElemType b){
    //比较元素a和b是否相等，相等返回TRUE，否则返回FALSE
    if(a==b) return TRUE;
    else return FALSE;
}//end of equal
status print(ElemType e){
    //打印元素e的值
    printf("\t%d", e);
    return OK;
}//end of print
