#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define maxBitLong 100
#define maxVariableLong 100
#define variableNumber 100

void tenToTwo(int n,char* s);
int selectMax(int argc,char *argv[]);
int getMaxVariableLong(int argc,char *argv[]);
int isContiguous(char* a,char* b,int sLong);
int ifAllCover(struct Term *primeList, int  primeLimit, char **miniTerm, int miniTermLimit);
void necessaryTerm(struct Term *primeList, int  primeLimit, char **miniTerm, int miniTermLimit);
void mergeTerm(struct Term *oList, int oListLimit);
int includeFatherTerm(struct Term a, struct Term b);
void visualPrint(struct Term *oList, int oListLimit);
int noRepeatTerm(struct Term *oList, int oListLimit);
struct Term termMachine(struct Term a, struct Term b,int difference);
int isContiguous(char* a,char* b,int sLong);
int getMaxVariableLong(int argc,char *argv[]);

//声明一个结构体以存储数据，因其中含变长数组，故将其置于主函数中
struct Term	//T大写以表明它是数据类型而不是变量名
{
	char value[maxBitLong];	//该项的值
	int prime;			//该项是否为质项，1是，0否
	int oneNumber;	//该项中1的个数
	int fatherTermLimit;	//父项的个数
	char fatherTerm[variableNumber][maxVariableLong];	//该项的父项，若无父项，则是他本身
};
int main(int argc,char *argv[]){

	//申明一些struct Term型的数组及其长度
	struct Term originalList[variableNumber];	//此数组用于存储从输入参数转化而来的原始的项
	//开始时用一下
	struct Term primeList[variableNumber];		//此数组用于存储质蕴含项
	int primeLimit =0;		//此变量用于标志primeList中有效元素的个数
	//贯穿始终的数组，总后输出它
	struct Term necessaryList[variableNumber];	//此数组用于存储必要质蕴含项
	int necessaryLimit = 0;		//此变量用于标志necessaryList中有效元素的个数

/***********将输入的参数存储到结构体数组originalList中**********************/
	for(int i=0; i<variableNumber; i++)
		originalList[i] = originalTermMachine(argv[i+1],maxBitLong);
	printAllTerm("originalList:",originalList, variableNumber);		//打印数组originalList
/*****************************找出质蕴含项*******************************/
	mergeTerm(originalList, variableNumber);
	primeLimit = noRepeatTerm(primeList, primeLimit);		//除去primeList中的重复项
	printAllTerm("primeList:", primeList, primeLimit);		//打印数组primeList

/*************************************************为便于递归，将一下流程用一个函数封装********************************************/
int run(struct Term *primeList, int  primeLimit, char **miniTerm, int miniTermLimit)
	{
	/**************************找出必要质蕴含项*******************************/	
		printf("%s,",miniTerm[2]);
		printf("miniTermLimit=%d,",miniTermLimit);
		printf("miniTerm:");		
		for(int i=0; i<miniTermLimit; i++) printf("%s,",miniTerm[i]);
		printf("\n");
		necessaryTerm(primeList, primeLimit, miniTerm, miniTermLimit);
		printAllTerm("necessaryList:", necessaryList, necessaryLimit);		//打印数组necessaryList
	/**************************判断必要质蕴含项是否全覆盖*************************/
		if(ifAllCover(primeList, primeLimit, miniTerm, miniTermLimit))	//若已全部覆盖
		{
			visualPrint(necessaryList, necessaryLimit);	//输出necessaryList
			exit(0);	//结束程序
		};
	/**************************生成所需质蕴含项产生表*************************/
		//所需质蕴含项产生表由noCoverTerm[noCoverLimit]和leftoverList[leftoverLimit]描述
		char *noCoverTerm[miniTermLimit];
		int noCoverLimit = 0;
		struct Term leftoverList[miniTermLimit];	//此数组用于存储剩余质蕴含项
		int leftoverLimit = 0;		//此变量用于标志leftoverList中有效元素的个数
		int argvNecessary[miniTermLimit];
		//for(int i=0; i<
		for(int i=0 ; i<miniTermLimit; i++) argvNecessary[i] = -1;
		for(int i=0 ; i<miniTermLimit; i++)
			for(int j=0 ; j<necessaryLimit; j++)
				for(int k=0 ; k<necessaryList[j].fatherTermLimit; k++)
					if(strcmp(miniTerm[i],necessaryList[j].fatherTerm[k])==0)
						argvNecessary[i] = 0;
		for(int i=0 ; i<miniTermLimit; i++) 
			if(argvNecessary[i] != 0)
				noCoverTerm[noCoverLimit++] = miniTerm[i];		//等效于划去已覆盖项
		printf("noCoverTerm:\n");
		for(int i =0; i<noCoverLimit; i++) printf("%s\n",noCoverTerm[i]);
		printf("\n");

		for(int i=0; i<primeLimit; i++)
		{
			int flag = 0;		
			for(int j=0 ; j<necessaryLimit; j++)
				if(strcmp(primeList[i].value,necessaryList[j].value)==0)
				{
					flag = 1;
					break;
				};
			if(flag ==0)
				leftoverList[leftoverLimit++] = primeList[i];
		};
		//标记、移除出各元素的成员fatherTerm数组中已经覆盖的项
		for(int i=0; i<leftoverLimit; i++)
			for(int j=0 ; j<leftoverList[i].fatherTermLimit; j++)
			{
				int flag = 0;
				for(int k=0 ; k<noCoverLimit; k++)
					if(strcmp(noCoverTerm[k],leftoverList[i].fatherTerm[j])==0)
						flag = 1;
				if(flag == 0)
					strcpy(leftoverList[i].fatherTerm[j], leftoverList[i].fatherTerm[--leftoverList[i].fatherTermLimit]);
			};
		printAllTerm("leftoverList:", leftoverList, leftoverLimit);		//打印数组leftoverList
	/****************************行消去规则*******************************/
		int cancellation[leftoverLimit];
		for(int i=0; i<leftoverLimit; i++) cancellation[i] = -1;
		for(int i=0; i<leftoverLimit; i++)
			for(int j=0; j<leftoverLimit; j++)
			{
				if( (j !=i) && (cancellation[j] != 0) && (cancellation[i] != 0) )
					if(includeFatherTerm(leftoverList[j], leftoverList[i])==1)
						cancellation[i] = 0;
			};
		int temp = leftoverLimit;
		for(int i=0; i<temp; i++)
			if((cancellation[i] == 0)||(cancellation[i] == 1))	//等于0或1说明要消去
			{		
				if(cancellation[i] == 0) leftoverLimit--;
				int j = 1;
				while(((cancellation[i+j] == 0)||(cancellation[i+j] == 1)) && (i+j < temp)) j++;
				leftoverList[i] = leftoverList[i+j];
				cancellation[i+j] = 1;
			};
		printAllTerm("行消去leftoverList:", leftoverList, leftoverLimit);		//打印数组leftoverList
	/****************************列消去规则*******************************/
		//生成最小项关于质项的列表
		struct Term rank[noCoverLimit][leftoverLimit];
		int rankLimit[leftoverLimit];
		int strike[leftoverLimit];
		for(int i=0; i<leftoverLimit; i++) rankLimit[i] = 0,strike[i] = 0;
		for(int i=0; i<noCoverLimit; i++)
			for(int j=0; j<leftoverLimit; j++)
				for(int k=0; k<leftoverList[j].fatherTermLimit; k++)
					if(strcmp(leftoverList[j].fatherTerm[k],noCoverTerm[i])==0)
					{
						rank[i][rankLimit[i]++] = leftoverList[j];
						break;
					};

		for(int i=0; i<noCoverLimit; i++)
		{
			printf("%d\n",i);
			for(int j=0; j<rankLimit[i]; j++)
				printf("%s,",rank[i][j].value);
			printf("\n");
		};

		//消去多余列
		for(int i=0; i<noCoverLimit; i++)
			for(int j=0; j<noCoverLimit; j++)
				if((i != j)&&(strike[j] != -1)&&(strike[i] != -1))
				{
					printf("i=%d,j=%d\n",i,j);
					//int flag = -1;
					int BincludeA = 1;
					for(int k=0; k<rankLimit[i]; k++)
					{
						int flag = -1;
						for(int m=0; m<rankLimit[j]; m++)
							if(strcmp(rank[i][k].value, rank[j][m].value)==0)
							{
								flag =0;
								break;
							};
						if(flag == -1)
						{
							BincludeA = 0;
							break;
						};
					};
					if(BincludeA == 1)
						strike[j] = -1;	//标记为-1的是要消去的项
					printf("strike:\n");
					for(int i=0; i<leftoverLimit; i++) printf("%d,",strike[i]);
					printf("\n");
				};

		printf("strike:\n");
		for(int i=0; i<leftoverLimit; i++) printf("%d,",strike[i]);
		printf("\n");

		temp = noCoverLimit;
		for(int i=0; i<leftoverLimit; i++)
			if(strike[i] == -1)
			{
				int j = 1;
				while(((noCoverTerm[i+j] == 0)||(cancellation[i+j] == 1)) && (i+j <temp)) j++;
				noCoverTerm[i] = noCoverTerm[i+j];
				strike[i+j] = -1;
				noCoverLimit --;
			};

		printf("noCoverTerm:\n");
		for(int i =0; i<noCoverLimit; i++) printf("%s\n",noCoverTerm[i]);
		printf("\n");
		//for(int i =0; i<6; i++) printf("%s\n",noCoverTerm[i]);
		printf("\n");

		//移除各元素的成员fatherTerm数组中已经被消去项
		for(int i=0; i<leftoverLimit; i++)
			for(int j=0 ; j<leftoverList[i].fatherTermLimit; j++)
			{
				int flag = 0;
				for(int k=0 ; k<noCoverLimit; k++)
					if(strcmp(noCoverTerm[k],leftoverList[i].fatherTerm[j])==0)
					{
						flag = 1;
						break;
					};
				if(flag == 0)
					strcpy(leftoverList[i].fatherTerm[j], leftoverList[i].fatherTerm[--leftoverList[i].fatherTermLimit]);
			};
		printAllTerm("列消去后的leftoverList:", leftoverList, leftoverLimit);		//打印数组leftoverList
		if((leftoverLimit==primeLimit)&&(noCoverLimit==miniTermLimit))		//检查是否进行了有效化简，防止陷入死循环
		{
			visualPrint(leftoverList, leftoverLimit);	//输出necessaryList
			printf("注意：这可能不是最简表达式，行列化简法无法继续化简，否则将陷入死循环。\n");
			exit(0);	//结束程序
		};
		printf("递归！\n");
		run(leftoverList, leftoverLimit, noCoverTerm, noCoverLimit);		
		return 0;
	};
	run(primeList, primeLimit, &(argv[1]), variableNumber);	//运行封装部分
}



void tenToTwo(int n,char* s)
{
	//将十进制的整数n换算成二进制的整数字符串s，高位在左。
	int y;
	int l = sizeof(s)/sizeof(s[0]);
	int i=0;
	int j=0;
	char temp[l];
	if(n==0)
	{
		s[0] = '0';
		s[1] = '\0';
	}
	else
	{
		while(n>0){
			y = n%2;
			temp[i++] = y?'1':'0';
			n /= 2;
		};
		temp[i] = '\0';
		j = i;
		//颠倒s
		for(i = 0; i < j; i++ )
		{
			s[i] = temp[j-1-i];
		};
		s[i] = '\0';
	};
};

int selectMax(int argc,char *argv[])
{
	//返回列表化简法中输入的参数中的最大值
	if(argc==1)	exit(-1);
	int box[variableNumber];
	int temp=0;
	int i=0;
	for(i = 0; i < variableNumber; i++)
	{
		box[i] = atoi(argv[i+1]);
	};
	for(i=0; i<argc-2; i++)
	{
		if(box[i]>box[i+1])
			{
				temp = box[i];
				box[i] = box[i+1];
				box[i+1] = temp;
			};	
	};
	return box[argc-2];
};

int getMaxVariableLong(int argc,char *argv[])
{
	//返回输入的参数中最长的那个的长度
	int maxVariableLong = 0;
	int i;
	if(argc ==2)
		maxVariableLong = strlen(argv[1]);	//处理只有一个参数时的特殊情况
	for(i=1; i<variableNumber; i++)
	{
		if(strlen(argv[i]) > strlen(argv[i+1]))
			maxVariableLong = strlen(argv[i]);
		else
			maxVariableLong = strlen(argv[i+1]);
	};
	return maxVariableLong;
};

int isContiguous(char* a,char* b,int sLong)
{
	//判断两个长度均为sLong的字符串a和b是否相邻，若相邻，则返回不同的那一位的索引值，若不相邻或完全相同，则返回-1
	int j=-1;
	for(int i=0; i<sLong; i++)
	{
		//printf("i=%d\n",i);
		//printf("a[i]=%c\n",a[i]);
		//printf("b[i]=%c\n",b[i]);
		if(a[i] != b[i])
		{	
			if(j==-1) j=i;
			else return -1;
		};
	};
	return j;
};
struct Term originalTermMachine(char* name,int maxBitLong)
{
	//根据传入的参数s生成对应的结构体
	struct Term oneterm;
	char s[maxBitLong+1];
	int i,j;
	int oldLong =0;
	strcpy(oneterm.fatherTerm[0],name);
	oneterm.fatherTermLimit =1;
	tenToTwo(atoi(name), s);
	oldLong = strlen(s);
	for(i=0; i<maxBitLong-oldLong; i++)
	{
		oneterm.value[i] = '0';
	};
	for(j=0; j<maxBitLong; i++,j++)
	{
		oneterm.value[i] = s[j];	
	};
	oneterm.value[i] = '\0';
	oneterm.oneNumber = 0;
	for(i=0; i<oldLong; i++) if(s[i]=='1') oneterm.oneNumber++;
	oneterm.prime = 1;
	return oneterm;
};

struct Term termMachine(struct Term a, struct Term b,int difference)
{
//合并相邻的两项a和b,并修改a,b中的prime为0,参数difference是a,b中不同的那位的偏移量
	struct Term oneterm;
	int i,j;
	//初始化oneterm.fatherTerm数组
	for(i=0; i<variableNumber; i++) oneterm.fatherTerm[i][0] = 'X';	//此处要注意被初始化为X
	oneterm.prime = 1;
	a.prime = 0;
	b.prime = 0;
	strcpy(oneterm.value,a.value);
	oneterm.value[maxBitLong] = '\0';
	oneterm.value[difference] = '-';
	oneterm.oneNumber = 0;
	for(i=0; i<maxBitLong; i++) if(oneterm.value[i]=='1') oneterm.oneNumber++;
	j = 0;
	for(i=0; i<a.fatherTermLimit;i++)  strcpy(oneterm.fatherTerm[j++],a.fatherTerm[i]);
	for(i=0; i<b.fatherTermLimit;i++)  strcpy(oneterm.fatherTerm[j++],b.fatherTerm[i]);
	oneterm.fatherTermLimit = a.fatherTermLimit + b.fatherTermLimit ;
	return oneterm;
};

int noRepeatTerm(struct Term *oList, int oListLimit)
{
//除去oList中的重复元素，返回去重后的元素个数
	int temp = oListLimit;
	for(int i=0; i<temp-1; i++)	//将重复项的value标记为X
	{		
		for(int j=i+1; j<temp; j++)	//将重复项的value标记为X
		{
			if(strcmp(oList[i].value,oList[j].value) == 0)
			{
				oList[i].value[0] = 'X';
				oListLimit--;
				break;
			};
		};
	};
	for(int i=0; i<temp-1; i++)	//去掉标记项
		if(oList[i].value[0] == 'X')
			{				
				int j = 1;
				while(oList[i+j].value[0] == 'X' && i+j < temp-1) j++;
				oList[i] = oList[i+j];
				oList[i+j].value[0] = 'X';
			};
	return oListLimit;
};

void printAllTerm(char *s, struct Term *oList, int oListLimit)
{
//打印oList中的所有元素的各成员的值,字符串s是提示内容
	printf("%s\n\n",s);
	for(int i=0; i<oListLimit; i++){
		int j;
		printf("i=%d\n",i);
		printf("value=%s\n",oList[i].value);
		printf("prime=%d\n",oList[i].prime);
		printf("oneNumber=%d\n",oList[i].oneNumber);
		printf("fatherTerm:");
		for(j=0; j<oList[i].fatherTermLimit-1; j++)
			printf("%s,",oList[i].fatherTerm[j]);
		printf("%s\n",oList[i].fatherTerm[j]);
		printf("fatherTermLimit = %d\n\n",oList[i].fatherTermLimit);
	};
};

void visualPrint(struct Term *oList, int oListLimit)
{
//以可视化的方式打印oList中的所有元素的vaule
	int i;
	int flag = 1;
	printf("F = ");
	for(i=0; i<oListLimit-1; i++)
	{
		for(int j=0; j<maxBitLong; j++)
		{
			if(oList[i].value[j] == '0') printf("!%c",'A'+j), flag=0;
			if(oList[i].value[j] == '1') printf("%c",'A'+j), flag=0;
		};
		printf(" + ");
	};
	for(int j=0; j<maxBitLong; j++)
	{
		if(oList[i].value[j] == '0') printf("!%c",'A'+j), flag=0;
		if(oList[i].value[j] == '1') printf("%c",'A'+j), flag=0;
	};
	if(flag) printf("1");	//如果什么都没有打印，则打印1
	printf("\n");
};

int includeFatherTerm(struct Term a, struct Term b)
{
//判断两个项a和b的fatherTerm是否具有包含关系，若a包含b（包含相等），返回1，否则，返回0
	int AincludeB = 1;
	for(int i=0; i<b.fatherTermLimit; i++)
	{
		int flag = 0;
		for(int j=0; j<a.fatherTermLimit; j++)
			if(strcmp(a.fatherTerm[j], b.fatherTerm[i]) == 0)
			{
				flag = 1;
				break;
			};
		if(flag == 0)
		{
			AincludeB = 0;
			break;
		};
	};
	return AincludeB;
};

void mergeTerm(struct Term *oList, int oListLimit)
{
//合并相邻项，找出质蕴含项，注意用到了全局变量maxBitLong，改变了全局变量primeList和primeLimit
	//合并相邻项，并向primeList数组中添加质项
	int difference;
	int primeNumber = 0;		//此变量存储本次处理中找出的质项
	//按“1”的个数进行分组
	struct Term groupByOne[maxBitLong+1][variableNumber];	//存储按“1”的个数分组的项,有n个“1”则存储于groupByOne[n]中
	int groupLimit[maxBitLong+1];
	for(int i=0; i<maxBitLong+1; i++) groupLimit[i] = 0;	//对j进行初始化
	for(int i=0; i<oListLimit ;i++)
	{
		groupByOne[oList[i].oneNumber][groupLimit[oList[i].oneNumber]++] = oList[i];
	};
	//根据分组求出最大可能的合并后的项数
	int max =0;
	for(int i=0; i<maxBitLong; i++)
		max +=  groupLimit[i]* groupLimit[i+1];
	struct Term mList[oListLimit];	//存放合并后的项对应的Term结构体
	int mListLimit = 0;
	//按分组进行比较、合并
	for(int i=0; i<maxBitLong; i++)
		for(int j=0; j<groupLimit[i]; j++)
			for(int k=0; k<groupLimit[i+1]; k++)
				{
					difference = isContiguous(groupByOne[i][j].value, groupByOne[i+1][k].value, maxBitLong);
					if( difference != -1)
					{
						mList[mListLimit++] = termMachine(groupByOne[i][j], groupByOne[i+1][k], difference);
						groupByOne[i][j].prime = 0;
						groupByOne[i+1][k].prime = 0;
					};
				};
	//将质项添加到primeList中并刷新primeLimit
	for(int i=0; i<maxBitLong+1; i++)
		for(int j=0; j<groupLimit[i]; j++)
		{
			if(groupByOne[i][j].prime==1)
			{
				primeNumber++;
				primeList[primeLimit++] = groupByOne[i][j];
			};
		};
	
	//若不是全部都是质项，则进行递归
	if(primeNumber < oListLimit)
		mergeTerm(mList, mListLimit);
};

void necessaryTerm(struct Term *primeList, int  primeLimit, char **miniTerm, int miniTermLimit)
{
//从质项中找出必要质蕴含项，注意改变了全局变量necessaryList和necessaryLimit
	int argvNecessary[miniTermLimit];
	for(int i=0 ; i<miniTermLimit; i++) argvNecessary[i] = -1;
	for(int i=0 ; i<miniTermLimit; i++)
		for(int j=0 ; j<primeLimit; j++)
			for(int k=0 ; k<primeList[j].fatherTermLimit; k++)
				if(strcmp(miniTerm[i],primeList[j].fatherTerm[k])==0)
					if(argvNecessary[i] == -1)
						argvNecessary[i] = j;
					else
						argvNecessary[i] = -2;
	for(int i=0 ; i<miniTermLimit; i++) 
		if(argvNecessary[i] >= 0)
		{
			necessaryList[necessaryLimit++] = primeList[argvNecessary[i]];
		};
	necessaryLimit = noRepeatTerm(necessaryList, necessaryLimit);	//除去necessaryList中的重复项
};

int ifAllCover(struct Term *primeList, int  primeLimit, char **miniTerm, int miniTermLimit)
{
//判断primeList中元素的父项是否全部覆盖miniTerm，1是，0否
	int all = 1;
	int argvNecessary[miniTermLimit];
	for(int i=0 ; i<miniTermLimit; i++) argvNecessary[i] = -1;
	for(int i=0 ; i<miniTermLimit; i++)
		for(int j=0 ; j<necessaryLimit; j++)
			for(int k=0 ; k<necessaryList[j].fatherTermLimit; k++)
				if(strcmp(miniTerm[i],necessaryList[j].fatherTerm[k])==0)
					argvNecessary[i] = 0;
	for(int i=1 ; i<miniTermLimit; i++) 
		if(argvNecessary[i] != 0)
			all =0;
	return all;
};


