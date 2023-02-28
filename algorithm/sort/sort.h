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
        printf("%d", arr[i]);
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

void insert_sort(int arr[], size_t len, func_cmp cmp = less){

}

void merge_sort(int arr[], size_t len, func_cmp cmp = less){

}

void quick_sort(int arr[], size_t len, func_cmp cmp = less){

}
