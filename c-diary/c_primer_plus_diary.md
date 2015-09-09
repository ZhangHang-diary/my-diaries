
[TOC]



####登陆过程
在用户验证后，系统会启动一个叫shell的进行，然后把用户交给这个进程，由这个进程处理用户的请求。
用户可在提示符后输入要运行的程序的名称，内核负责把用户的输入传给shell。

Unix不提供文件恢复删除的功能是因为，Unix是一个多用户系统，如果当前用户删除了一个文件，所占磁盘空间可能立即被分配给其他用户创建的文件，这样就覆写了那个位置。





####utmp.h
utmp结构中有一个成员ut_type 当其值为7（USER_PROCESS）时，表示这是一个已经登陆的用户。

UTMP_FILE      /var/run/utmp

```c
#include <stdio.h>
#include <stdlib.h>
#include <utmp.h>
#include <fcntl.h>
#include <unistd.h>
#include <time.h>

#define SHOWHOST

void show_info(struct utmp *);
void show_time(long int);


int main()
{
  struct utmp  current_record;
  int          utmpfd;
  int          reclen = sizeof(current_record);

  if ((utmpfd = open(UTMP_FILE, O_RDONLY)) == -1){
    perror(UTMP_FILE);   /* UTMP_FILE is in utmp.h */
    exit(1);
  }

  while (read(utmpfd, &current_record, reclen) == reclen)
    show_info(&current_record);
  close(utmpfd);
  return 0;
}


void show_info(struct utmp *utbufp)
{
  if (utbufp->ut_type != USER_PROCESS)
    return;

  printf("%-8.8s", utbufp->ut_name);
  printf(" ");
  printf("%-8.8s", utbufp->ut_line);
  printf(" ");
  show_time(utbufp->ut_time);
  //printf("%10d", utbufp->ut_time);
  printf(" ");

# ifdef SHOWHOST
  printf("%s", utbufp->ut_host);
# endif
  printf("\n");
}


void show_time(long int timeval)
{
  char * cp;
  cp = ctime(&timeval);
  
  printf("%12.12s", cp+4);
}


```



####time.h

`typeof long int time_t;`
定义了 time_t 数据类型，

`ctime(&time_t)` 函数接受一个指向time_t的指针，返回时间字符串类似以下格式：
`Wed Jun 30 21:49:08 2015\n` 
我们只需要从第4个字符开始的后面12个字符，因此`ctime(&time_t) +4` （见上文）



##类型基础


###short int

```
short nu = 200;
printf("%s", nu);
```

在32位的系统中，short类型有可能被转为int类型。
在short类型和int类型长度不同的系统中，16 <--> 32，使用int类型值进行参数传递的速度更快。



###char
char类型用于储存字母和标点符号子类的字符，但是其实char实现是整数类型，char储存的实际上是整数而不是字符，为了处理字符，计算机给出一种数字编码。老美使用ASCII码就可表示出字母和一些特殊字符了，许多IBM主机使用EBCDIC，其原理是一样的。

`ASCII 0～127`，只需7位就可表示，char类型通常定义为使用8位内存单元。

使用其他字符集的平台应使用16bit甚至32bit的char表示方法，C把一个byte定义为char类型使用的位（bit）数，所以在这样的系统上，C文档提到的是16为或32位，而不是8位。


单引号中的一个字符是C的一个字符常量，编译器遇到'A'时会转换其对应的字符码，双引号会被看做字符串。

因为字符实际上以数值形式存储，因此可以直接定义数字。但是不推荐此做法，应使用字符常量。
`char c = 64;`

令人奇怪的是，C将字符常量视为int类型而非char类型，如：在int类型为32位，char类型为8位的系统中。'B'作为数值66储存在一个32位单元中，而 'char ch='B';` 赋值后的ch则把66存储在一个8位单元中。
因此利用这个特性，一个字符常量'ABCD',将把4个独立的8位ASCII码储存在一个32位的单元中。然而，如果把字符常量赋值给一个char变量，那么只有最后8位起作用，因此为'E'。

一些实现把char当做有符号类型，其取值范围为 `-128~127` 。
另一些实现把char当做无符号类型，取值为 `0~255` 。



###_Bool类型
c99引入，0表示false, 1表示true。因为只需要0或1，所以1位的储存空间就够了。



###可移植类型 inttypes.h
C99提供一个可选的名字集合，包含在头文件 inttypes.h：
int16_t  表示一个16位有符号的整数类型。
uint32_t 表示一个32位无符号整数类型。



###浮点型
C标准规定，float类型必须至少能表示6位有效数字，取值范围至少 10^-37 ~ 10^+37
通常系统使用32位表示浮点数，其中8位用于表示指数以及符号，24位用于表示非指数部分（称尾数或有效数字）及其符号。

double和float具有相同的最小取值范围要求，但double必须至少能表示10位有效数字。一般double使用64位长度。

默认情况下，编译器将浮点常量当做double类型：
`float some = 4.0 * 2.0;`
4.0和2.0被储存为double类型，乘积运算时使用双精度，结果被转为正常的float类型，这能保证计算精度，但会减慢程序的执行。

2.3f
9.11E9F
l 或 L 后缀表示 long double
没有后缀的浮点常量为double类型


C99为表示浮点常量新添加了一种十六进制格式，前缀0x或0X：
`0xa.lfp10`   a是10，lf表示1/16加上15/256，p10表示2^10。




###复数和虚数类型
有三种基本的复试类型 float_Complex double_Complex long double_Complex
float_Complex 包含两个float值。，一个表示复数的实部，另一个表示复数的虚部。

三种虚数类型： float_Imaginary double_Imaginary long double_Imaginarg
如果包含头文件 complex.h 则可使用complex代替_Complex， 用imaginary代替_Imaginary， 用I表示 -1 的平方根。



##字符串

###scanf 

```c
char name[40];
int main(){
	scanf("%s", &name);
	prinf("%s", name);
}
```

如果输入Bob Lin，则只会输出Bob，因为scanf遇到空格、制表符、换行符等会停止读取。
C使用其他读取函数如gets()来处理一般的字符串。

字符串常量"c"和字符常量'c'不同，字符串输入派生类型（char数组），字符串实际由"c\0"组成。

###strlen和sizeof
sizeof运算符以字节为单位给出数据大小，strlen()函数以字符为单位给出字符串的长度。
因为1个字符占一个字节，看似两者相等，实则不然。
```c
char name[40];
name = Bob;
printf("%s usage, %s", strlen(name), sizeof name);
```
因为strlen知道遇到\0要停止，所以长度为3，sizeof为40。



##常量和C预处理器

###define
编译时代入法（compile time substitution）,明显常量（manifest constant）。
define不用分号是因为这是一种代替机制，而不是C语句。define语句也可以定义字符和字符串常量。注意，其是替代，因此下例经转换后会变成：

```
#define dig = 20;
int result = 42 + dig;
// result = 42 + = 20;
```

limits.h 和 float.h 定义了一些系统常量的取值范围。



###printf 和 scanf 的 * 修饰符

**printf**

```
#include <stdio.h>

int main(void){
	unsigned width, precision;
	int number = 350;
	double weight = 250.5;

	printf("What field width?\n");
	scanf("%d", &width);
	printf("The number is: %*d \n", width, number);
    
	printf("Now enter a width and a precision: \n");
	scanf("%d %d", &width, &precision);
	prinf("Weight= %*.*f\n", width, precision, weight);
}

```

What field width?
6
The number is: 350
Now enter a width and a precision:
4 3
Weight= 250.000

<hr />

**scanf**的*有截然不同的行为，放在%和说明符字母之间时，表示跳过。

```c
printf("Please enter three integers\n");
scanf("%*d %*d %s", &n);
printf("the last integer was %s\n", n);
```

Please enter three integers
2001 2002 2003
the last integer was 2003



##语句和表达式

###语句

`x = 6 + (y = 5);`

尽管一个语句（或至少是一个有作用的语句）是一条完整的指令，但不是所有的完整的指令都是语句。因此子表达式y=5是一个完整的指令，但它只是一个语句的一部分。

`int port` 去掉分号不是一个表达式，也没有值。


















