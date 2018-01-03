#include<stdio.h>
typedef struct Point{
   int id;  //节点id
   int x;   //节点横坐标
   int y;   //节点纵坐标
}Point;
typedef struct PonitPairs{
    Point point1;   //第一个点
    Point point2;   //另一个点
    long range;     //两点之间距离的平方
}PonitPairs;
PonitPairs NearestPointPair(Point*, int);
PonitPairs Strip(Point *, Point *, int);
long dist(Point, Point);
void quickSort(Point a[], int, int, int);
int partition( Point a[], int, int, int);

int main(){
    PonitPairs length;
    Point set[]={{0,0,0},{1,3,4},{2,12,5},{3,3,14},{4,-3,6},{5,-4,-4},{6,4,-5},{7,7,6}};
    length = NearestPointPair(set,sizeof(set)/sizeof(set[0]));   //将数组长度作为参数传入
    printf("最近的是%d号点和%d号点，其距离的平方为%ld。\n",length.point1.id,length.point2.id,length.range);
    return 0;
}
PonitPairs NearestPointPair(Point *set, int n){
    int i=0;
    Point Ptable[n];
    Point Qtable[n];
    //获得分别按x坐标和y坐标排序的表
    for(i=0;i<n;i++){
        Ptable[i]=set[i];
        Qtable[i]=set[i];
    }
    quickSort(Ptable, 0, n-1, 0);
    quickSort(Qtable, 0, n-1, 1);
    //调用递归过程
    return Strip(Ptable, Qtable, n);
}
PonitPairs Strip(Point *P, Point *Q, int n){
    //Ptable已按x坐标排好序, Qtable已按y坐标排好序,n是点的个数
    int middle=n/2;
    int i=0, j=0, k=0;
    int ve=0;
    int num=0;     //处于strip中点的个数
    PonitPairs dl;     //dl :PL中的最近点对;
    PonitPairs dr;     //dr :PR中的最近点对;
    PonitPairs dc;     //dc :跨区最近的点对；
    PonitPairs min;
    PonitPairs temp;
    Point PL[middle];
    Point QL[middle];
    Point PR[n-middle];
    Point QR[n-middle];
    Point Pf[n];
    Point Qf[n];
    if(n<4){
        min.point1=P[0];
        min.point2=P[1];
        min.range=dist(P[0],P[1]);
        for(i=0;i<n-1;i++){
            for(j=i+1;j<n;j++){
                temp.point1=P[i];
                temp.point2=P[j];
                temp.range=dist(P[i],P[j]);
                if(min.range>temp.range) min=temp;
            }
        }
        return min;
    }
    //当n较大时进行分治
    for(i=0;i<middle;i++){
        PL[i]=P[i];
    }
    for(i=middle;i<n;i++){
        PR[i-middle]=P[i];
    }
    k=0;
    for(i=0;i<n;i++){
        ve=0;
        for(j=0;j<middle;j++)
            if(Q[i].id==PR[j].id){
                ve=1;
                break;
            };
        if(ve==1){
            QR[k++]=Q[i];
        }
    }
    k=0;
    for(i=0;i<n;i++){
        ve=0;
        for(j=0;j<n-middle;j++)
            if(Q[i].id==PL[j].id){
                ve=1;
                break;
            };
        if(ve==1){
            QL[k++]=Q[i];
        }
    }
    dl = Strip(PL, QL, middle);
    dr = Strip(PR, QR, n-middle);
    if(dl.range>dr.range) min=dr;
    else min=dl;
    //筛选出处于strip中的点
    k=0;
    for(i=middle-1;i>=0;i--){
        if((P[middle].x-PL[i].x)*(P[middle].x-PL[i].x)<min.range){
            Pf[k++]=PL[i];
        }
        else{
            break;
        }
    }
    for(i=0;i<n-middle;i++){
        if((P[middle].x-PR[i].x)*(P[middle].x-PR[i].x)<min.range){
            Pf[k++]=PR[i];
        }
        else{
            break;
        }
    }
    num=k;
    k=0;
    for(i=0;i<n;i++){
        ve=0;
        for(j=0;j<num;j++)
            if(Q[i].id==Pf[j].id){
                ve=1;
                break;
            };
        if(ve==1){
            Qf[k++]=Pf[j];
        }
    }
    for(i=0;i<num-1;i++){
        for(j=i+1;j<num;j++){
            if((Qf[i].y-Qf[j].y)*(Qf[i].y-Qf[j].y)<min.range){
                temp.point1=Qf[i];
                temp.point2=Qf[j];
                temp.range=dist(Qf[i],Qf[j]);
                if(temp.range<min.range){
                    min=temp;
                }
            }
            else{
                break;
            }
        }
    }
    return min;
}
long dist(Point a, Point b){
    //返回a,b两点之间的距离的平方
    return (a.x-b.x)*(a.x-b.x)+(a.y-b.y)*(a.y-b.y);
}
//快排部分
void quickSort(Point a[], int l, int r, int flag){
   //快排，flag=0，按x坐标排序；flag=1，按y坐标排序
   int j;
   if(l<r){
       j = partition( a, l, r, flag);
       quickSort( a, l, j-1, flag);
       quickSort( a, j+1, r, flag);
   }
}
int partition( Point a[], int l, int r, int flag) {
   //flag=0，按x坐标排序；flag=1，按y坐标排序
   Point  t;
   int i, j, pivot;
   if(flag==0){
       pivot = a[l].x;
   }
   else{
       pivot = a[l].y;
   }
   i = l; j = r+1;
   while(1){
        if(flag==0){
            do ++i; while( a[i].x <= pivot && i <= r );
    	    do --j; while( a[j].x > pivot );
        }
        else{
            do ++i; while( a[i].y <= pivot && i <= r );
    	    do --j; while( a[j].y > pivot );
        }
   	    if( i >= j ) break;
   	    t = a[i]; a[i] = a[j]; a[j] = t;
   }
   t = a[l]; a[l] = a[j]; a[j] = t;
   return j;
}
