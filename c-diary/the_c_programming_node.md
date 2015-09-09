main memory
Random Access Memory
Read-Only Memory 


`-45/7 == 45/-7 == -6`
`45/7 == -45/-7 == 64`

取模结果正负只和左操作数相关
`45%-7 = 3`
`-45%7 = -3`

```c
int expenditure = 75;
printf("Your balance has changed by %d", -expenditure);

/*Your balance has changed by -75      注意-expenditure不会改变变量的值*/
```


1byte can store integer limited -128 ~ 127 



char  signed -128 ~ 127
char  unsigned 0 ~ 255

```
char letter = 'A';
letter = letter + 3;
/* 结果为70 `A` 对应ASCII码数字为67 */
```



`*ip += 1  == ++*ip`  把ip指向的值取出自加1
`但是如果后缀则必须加括号(*ip)++  因为类似*和++这样的一元运算符遵循从右到左的结合顺序。`


###指针与函数参数
由于C中以传值方式将参数传递给被调用函数，So, 被调用函数不能直接修改主调函数中变量的值。
swap函数不会影响到它的例程中的变量a,b，该函数仅仅交换了a,b的副本的值。
```
void swap(int x, int y){   /*  error */
	int temp;
	temp = x;
  	x = y;
	y = temp;
}

main(){
	int a = 1;
	int b = 2;
	swap(a,b);
}
```

**how to implement that?**
```
void swap(int *px, int *py){
	int temp;
	temp = *px;
	*px = *py;
	*py = temp;
}

main(){
	swap(&a, &b);
}
```








