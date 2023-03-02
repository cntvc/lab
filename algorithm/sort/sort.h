#include<stdio.h>

template<typename T>
void swap(T &a, T &b){
    T t = a;
    a = b;
    b = t;
}

typedef bool (*func_cmp)(int, int);

template<typename T>
bool less(T a, T b){
    return a > b;
}

template<typename T>
bool greater(T a, T b){
    return a < b;
}

template<typename T>
void show(T arr[], size_t len){
    for(size_t i = 0; i < len; i++){
        printf("%d ", arr[i]);
    }
    printf("\n");
}

void bubble_sort(int arr[], size_t len, func_cmp cmp = less){
    for(size_t i = 0; i < len; i++){
        for (size_t j = 0; j < len - i - 1; j++)
        {
            if(cmp(arr[j], arr[j + 1])){
                swap(arr[j], arr[j + 1]);
            }
        }
    }
}

void select_sort(int arr[], size_t len, func_cmp cmp = less){
    for(size_t i = 0; i < len; i++){
        size_t max_index = len - i - 1;
        for(size_t j = 0; j < len - i - 1; j++){
            if (cmp(arr[j], arr[max_index])){
                max_index = j;
            }
        }
        swap(arr[max_index], arr[len - i - 1]);
    }
}

/**
 * 数组分为两部分，有序和无序
 * 以无序位置开始，依次取一个元素，向左遍历寻找可插入位置，然后移动数组放入其中
*/
void insert_sort(int arr[], size_t len, func_cmp cmp = less){
    for(size_t i = 1; i < len; i++){
        int tmp = arr[i];
        size_t j = i;
        while(j && cmp(arr[j - 1], tmp)){
            arr[j] = arr[j - 1];
            j--;
        }
        arr[j] = tmp;
    }
}

void __merge_partition(int arr[], int l, int mid, int r, func_cmp cmp){
    int *tmp = new int[r - l + 1];
    size_t k = 0;
    size_t i = l, j = mid + 1;
    while(i <= mid && j <= r){
        if(cmp(arr[i], arr[j])){
            tmp[k] = arr[i];
            i++;
        }else{
            tmp[k] = arr[j];
            j++;
        }
        k++;
    }
    while (i <= mid)
    {
        tmp[k++] = arr[i++];
    }
    while ( j <= r)
    {
        tmp[k++] = arr[j++];
    }
    for(size_t i = l, k = 0; i <= r; i++, k++){
        arr[i] = tmp[k];
    }
    delete []tmp;
}

void __partition(int arr[], size_t l, size_t r, func_cmp cmp){
    if(l >= r){
        return;
    }
    size_t mid = l + ((r - l) >> 1);
    __partition(arr, 0, mid, cmp);
    __partition(arr, mid + 1, r, cmp);
    __merge_partition(arr, l, mid, r, cmp);
}

/**
 * 将一个数组拆分若干份，直到最小，然后合并时保持分区有序。
*/
void merge_sort(int arr[], size_t len, func_cmp cmp = less){
    __partition(arr, 0, len - 1, cmp);
}
// 5
// 9 4 7 3 8 5
void __quick_sort(int arr[], size_t l, size_t r, func_cmp cmp){
    if (l >= r){
        return;
    }
    // 这里取区间末尾数字为分区点
    int tmp = arr[r];
    size_t k = l;
    for(size_t i = l; i <= r; i++){
        if(cmp(arr[i], tmp)){
            swap(arr[i], arr[k]);
            k++;
        }
    }
    swap(arr[k], arr[r]);
    if(k != 0){
        // size_t 类型 k - 1 可能会溢出
        __quick_sort(arr, l, k - 1, cmp);
    }
    __quick_sort(arr, k + 1, r, cmp);
}

/**
 * 选取一个标志位，然后遍历，将大于该元素和小于的分别移动到两边，如此往复
*/
void quick_sort(int arr[], size_t len, func_cmp cmp = less){
    __quick_sort(arr, 0, len - 1, cmp);
}


