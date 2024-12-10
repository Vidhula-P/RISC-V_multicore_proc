#include "mtbmark-sort.h"
#include "ece4750.h"
#include "ubmark-sort.h"

// Argument structure (modified to fit sorting better)
typedef struct
{
  int* src;     // Pointer to the source array
  int* dst;     // Pointer to the destination subarray
  int first;    // First index this core should process
  int last;     // (One past) last index this core should process
} arg_t;

// InsertionSort function
void InsertionSort(int arr[], int left, int right)
{
  for (int i = left + 1; i <= right; i++)
  {
    int key = arr[i];
    int j = i - 1;

    // Shift elements to make space for key
    while (j >= left && arr[j] > key)
    {
      arr[j + 1] = arr[j];
      j--;
    }
    arr[j + 1] = key;
  }
}

// Worker function
void work(void* arg_vptr)
{
  // Cast void* to argument pointer
  arg_t* arg_ptr = (arg_t*)arg_vptr;

  // Extract fields
  int* src = arg_ptr->src;
  int* dst = arg_ptr->dst;
  int first = arg_ptr->first;
  int last = arg_ptr->last;

  // Perform sorting
  InsertionSort(src, first, last - 1); // `last - 1` since `last` is exclusive
  for (int i = first; i < last; i++) {
    dst[i - first] = src[i];
  }
}

//Mergesort algorithm

// Function to merge two sorted arrays
void mergeTwoArrays(int* arr1, int size1, int* arr2, int size2, int* mergedArray) {
  int i = 0, j = 0, k = 0;    
  // Merge elements from arr1 and arr2 in sorted order
  while (i < size1 && j < size2) {
    if (arr1[i] < arr2[j]) {
      mergedArray[k++] = arr1[i++];
    } else {
      mergedArray[k++] = arr2[j++];
    }
  }
  
  // Add remaining elements from arr1
  while (i < size1) {
    mergedArray[k++] = arr1[i++];
  }
  
  // Add remaining elements from arr2
  while (j < size2) {
    mergedArray[k++] = arr2[j++];
  }
}


int* mergesort(int* arr0, int size0, int* arr1, int size1, int* arr2, int size2, int* arr3, int size3, int* finalSize) {
  int* temp1 = ece4750_malloc((size0+size2)*(int)(sizeof(int)));
  int* temp2 = ece4750_malloc((size1+size3)*(int)(sizeof(int)));

  // Merge first two arrays
  mergeTwoArrays(arr0, size0, arr2, size2, temp1);  
  // Merge last two arrays
  mergeTwoArrays(arr1, size1, arr3, size3, temp2);

  *finalSize = size0 + size1 + size2 + size3;
  int* mergedArray = ece4750_malloc((*finalSize)*(int)(sizeof(int)));
  mergeTwoArrays(temp1, size0 + size2, temp2, size1 + size3, mergedArray);

  // Free temporary arrays
  ece4750_free(temp1);
  ece4750_free(temp2);


  return mergedArray;
}


// Main sorting function
void mtbmark_sort(int* x, int size)
{
  // if (f[0] == s){}
  // int x[]     = { 4, 1, 3, 6, 2, 5, 8, 7};
  // int size = 8;
  int block_size = (int)((int)(size/4));

  int size0 = block_size;
  int size1 = block_size;
  int size2 = block_size;
  int size3 = size - 3*block_size;

  int* arr0 = ece4750_malloc(size0*(int)(sizeof(int)));
  int* arr1 = ece4750_malloc(size1*(int)(sizeof(int)));
  int* arr2 = ece4750_malloc(size2*(int)(sizeof(int)));
  int* arr3 = ece4750_malloc(size3*(int)(sizeof(int))); // Last block may be larger if size isn't divisible by 4

  // Define argument for the single core
  arg_t arg0 = {x, arr0, 0, block_size};
  arg_t arg1 = {x, arr1, block_size, 2 * block_size};
  arg_t arg2 = {x, arr2, 2 * block_size, 3 * block_size};
  arg_t arg3 = {x, arr3, 3 * block_size, size}; 

  // Spawn work onto core 1, 2, and 3
  ece4750_bthread_spawn(1, &work, &arg1);
  ece4750_bthread_spawn(2, &work, &arg2);
  ece4750_bthread_spawn(3, &work, &arg3);

  // Perform the work
  work(&arg0);

  // Wait for cores
  ece4750_bthread_join(1);
  ece4750_bthread_join(2);
  ece4750_bthread_join(3);
  
  int finalSize;
  int* mergedArray = mergesort(arr0, size0,arr1, size1, arr2, size2, arr3, size3, &finalSize);
    
  for (int i = 0; i < size; i++)
  {
    x[i] = mergedArray[i];
  }

  ece4750_free(arr0);
  ece4750_free(arr1);
  ece4750_free(arr2);
  ece4750_free(arr3);
  ece4750_free(mergedArray);
}