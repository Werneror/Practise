#include<stdio.h>
#include <string.h>
void LCS_LENGTH(char const*, char const*);
void strRev(char *s);
int main(int argc, char const *argv[]) {
  if (argc<3) {
    printf("请以两个字符串作为参数\n");
  }
  else {
    LCS_LENGTH(argv[1], argv[2]);
  }
  return 0;
}
void LCS_LENGTH(char const*x, char const*y){
  int m,n;
  int i,j,k;
  int max;
  m = strlen(x);
  n = strlen(y);
  int c[m+1][n+1];
  char b[m+1][n+1];
  if (m>n) {
    max=m;
  }
  else {
    max=n;
  }
  char temp[max];
  for (i = 0; i < m+1; i++) {
    c[i][0]=0;
  }
  for (j = 0; j < n+1; j++) {
    c[0][j]=0;
  }
  for (i = 0; i < m+1; i++) {
    for (j = 0; j < n+1; j++) {
      b[i][j];
    }
  }
  for (i = 0; i < m+1; i++) {
    for (j = 0; j < n+1; j++) {
      b[i][j]=' ';
    }
  }
  for (i = 1; i < m+1; i++) {
    for (j = 1; j < n+1; j++) {
      if(x[i-1]==y[j-1]){
        c[i][j]=c[i-1][j-1]+1;
        b[i][j]='q';
      }
      else if(c[i-1][j]>=c[i][j-1]) {
        c[i][j]=c[i-1][j];
        b[i][j]='w';
      }
      else {
        c[i][j]=c[i][j-1];
        b[i][j]='a';
      }
    }
  }
  i=m, j=n, k=0;
  while (1) {
    if (b[i][j]=='w') {
      i--;
    }
    else if (b[i][j]=='a') {
      j--;
    }
    else if (b[i][j]=='q') {
      temp[k++]=x[i-1];
      i--;
      j--;
    }
    else {
      temp[k++]='\0';
      strRev(temp);
      printf("%s\n", temp);
      return;
    }
  }
}
void strRev(char *s) {
  //反转字符串
  char temp, *end = s + strlen(s) - 1;
  while( end > s)
  {
      temp = *s;
      *s = *end;
      *end = temp;
      --end;
      ++s;
  }
}
