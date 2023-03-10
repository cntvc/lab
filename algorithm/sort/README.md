# 复杂度分析

## 冒泡排序

对于n个元素的数组，有n!种排列方式，用数组有序度和逆序度来分析。    

**有序度**：数组中有有序关系的元素对对的个数   
```
有序元素对：a[i] <= a[j], 如果i < j。

逆序元素对：a[i] > a[j], 如果i < j。
```
对于一个完全倒序的数组[6,5,4,3,2,1]，有序度为0    
对于一个完全有序的数组[1,2,3,4,5,6]，有序度为 $(n-1) * n/2$，称为**满有序度**

**逆序度 = 满有序度 - 有序度**

**时间复杂度：** 
有长度为n的数组中，每次确定一个最小（大）的值交换到未排序末尾，交换次数为 $n+(n-1)+(n-2)+...+2+1$ = $(n+1)*n/2$

- 最好时间复杂度：在优化后，如果数组原本有序，那么只需要遍历一次，复杂度 $O(N)$

- 最坏时间复杂度：数组在完全无序，逆序度最大情况下，需要遍历 $(n+1)*n/2$ 次，时间复杂度 $O(n^2)$

- 平均时间复杂度：冒泡排序包含两个原子操作，**比较**和**交换**。每交换一次，有序度+1。对于一个确定的数组，有序度确定，交换次数也就是确定的，即数组的逆序度    
    对于包含 n 个元素的数组，最坏情况下，有序度为0，那么交换次数为 $(n-1)*n/2$，最好情况下不需要交换，可以取平均值表示一般情况，那么交换次数为 $(n-1)*n/4$，比较次数一定比交换次数多，最多不超过 $O(n^2)$， 因此平均时间复杂度 $O(n^2)$

**空间复杂度：** 
    原地排序，空间复杂度 $O(1)$

**是否稳定：** 
    只涉及到前后位置互换，整体相对位置未改变，是稳定排序的

## 选择排序

* **时间复杂度：** 
    - 最坏情况下，每次交换需要遍历后面所有元素，时间复杂度 O(N^2)
    - 最好情况下，数组已经有序，依然需要遍历所有元素，时间复杂度O(N^2)
    - 平均时间复杂度：O(N^2)

* **空间复杂度：** 
    遍历过程中使用常数级额外空间，空间复杂度为O(1)

## 插入排序

**时间复杂度：** 
- 最坏情况下，每次插入一个元素需要遍历前面所有元素，时间复杂度 O(N^2)
- 最好情况下，数组已经有序，插入时间复杂度O(1),整体时间复杂度O(N)
- 平均时间复杂度：在数组中每次插入一个元素平均时间复杂度O(N)，对于插入排序而言，每次都相当于在数组插入元素，那么平均时间按复杂度为O(N^2)

**空间复杂度：** 
遍历过程中使用常数级额外空间，空间复杂度为O(1)

## 归并排序
**时间复杂度：** 

O(Nlog(N)) N 为数组个数

拆解为N个数组，两两合并Log(N),整体时间复杂度O(Nlog(N))

递推场景中，问题a可以拆分为子问题b，c。 k表示将b，c合并为a的操作时间

那么我们可以得到这样关系式`T(a) = T(b) + T(c) + k`

我们将排序过程分解为两个操作: T(n/2) 表示拆分数组的时间， n表示合并需要的时机

在二路归并排序时，可以得到这样的公式： 
```
T(1) = C ;              n=1 C表示常数级时间
T(n) = 2*T(n/2) + n ;   n>1
```
```C
T(n) = 2*T(n/2) + n
    = 2*(2*T(n/4)+n/2)+n = 4*T(n/4)+2*n
    = 2*(2*(2*T(n/8)+n/4)+n/2)+n = 8*T(n/8) + 3*n
    = ...
    = 2^k * T(n/(2^K)) + k*n
```
当 T(n/(2^K)) = T(1) 时，k=log_2(n)

带入上述公式：
```
T(n) = n + n*log_2(n)
```
因此归并排序时间复杂度O(Nlog(N))
  


**空间复杂度：** 
O(N) N为数组个数
- 在任意时刻，只有一个函数运行，因此最多临时空间大小为 N


## 快速排序
**时间复杂度：** 
- 最好情况下：推导类似归并排序，在每次恰好选取到数组中点时，时间复杂度O(Nlog(N))
- 最坏情况下：每次选取点都是剩余中最大或者最小的，每次需要遍历的元素个数是n,n-1,n-2...2,1，这样时间复杂度为O(n^2)

**空间复杂度：** 空间复杂度为O(1)