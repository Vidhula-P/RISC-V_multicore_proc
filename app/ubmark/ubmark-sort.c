//========================================================================
// ubmark-sort
//========================================================================

#include "ece4750.h"
#include "ubmark-sort.h"

//------------------------------------------------------------------------
// ubmark_sort
//------------------------------------------------------------------------

//function to calculate log as math library can't be used
int my_log(long x) {
    int result = 0;
    while (x > 1) {
        x /= 2;
        result++;
    }
    return result;
}

// A utility function to swap the values pointed by the two pointers
void swapValue(int *a, int *b) 
{ 
    int temp = *a; 
    *a = *b; 
    *b = temp; 
} 

// Function to sort an array using insertion sort
void InsertionSort(int arr[], int *begin, int *end) 
{ 
    int left = (int)(begin - arr); 
    int right = (int)(end - arr); 

    for (int i = left + 1; i <= right; i++) 
    { 
        int key = arr[i]; 
        int j = i - 1;

        while (j >= left && arr[j] > key) 
        { 
            arr[j + 1] = arr[j]; 
            j--; 
        } 
        arr[j + 1] = key; 
    } 
} 

// Function to partition the array and return the partition point
int* Partition(int arr[], int low, int high) 
{ 
    int pivot = arr[high]; 
    int i = low - 1; 

    for (int j = low; j <= high - 1; j++) 
    { 
        if (arr[j] <= pivot) 
        { 
            i++; 
            swapValue(&arr[i], &arr[j]); 
        } 
    } 
    swapValue(&arr[i + 1], &arr[high]); 
    return &arr[i + 1]; 
} 

// Function to find the median of three elements
int *MedianOfThree(int *a, int *b, int *c) 
{ 
    if ((*a > *b) != (*a > *c))
        return a;
    else if ((*b > *a) != (*b > *c))
        return b;
    else
        return c;
}

// Heapify a subtree rooted at index i
void heapify(int arr[], int n, int i) 
{ 
    int largest = i; 
    int left = 2 * i + 1; 
    int right = 2 * i + 2; 

    if (left < n && arr[left] > arr[largest]) 
        largest = left; 

    if (right < n && arr[right] > arr[largest]) 
        largest = right; 

    if (largest != i) 
    { 
        swapValue(&arr[i], &arr[largest]); 
        heapify(arr, n, largest); 
    } 
} 

// Function to perform heap sort
void HeapSort(int arr[], int n) 
{ 
    for (int i = n / 2 - 1; i >= 0; i--) 
        heapify(arr, n, i); 

    for (int i = n - 1; i >= 0; i--) 
    { 
        swapValue(&arr[0], &arr[i]); 
        heapify(arr, i, 0); 
    } 
}

// Utility function to perform introsort
void IntrosortUtil(int arr[], int *begin, int *end, int depthLimit) 
{ 
    int size = (int)(end - begin + 1); 

    if (size < 16) 
    { 
        InsertionSort(arr, begin, end); 
        return; 
    } 

    if (depthLimit == 0) 
    { 
        HeapSort(begin, size); 
        return; 
    } 

    int *pivot = MedianOfThree(begin, begin + size / 2, end); 
    swapValue(pivot, end); 

    int *partitionPoint = Partition(arr, (int)(begin - arr), (int)(end - arr)); 
    IntrosortUtil(arr, begin, partitionPoint - 1, depthLimit - 1); 
    IntrosortUtil(arr, partitionPoint + 1, end, depthLimit - 1); 
}

// Implementation of introsort
void Introsort(int arr[], int *begin, int *end) 
{ 
    long size = (long)(end - begin) + 1;
    int depthLimit = 2 * (int)(my_log(size));
    IntrosortUtil(arr, begin, end, depthLimit); 
}

void ubmark_sort(int *x, int size) {
    Introsort(x, x, x + size - 1);
}