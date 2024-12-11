#include "mtbmark-sort.h"
#include "ece4750.h"
#include "ubmark-sort.h"

// Argument structure (modified to fit sorting better)
typedef struct
{
  int* src;     // Pointer to the source array
  int first;    // First index this core should process
  int last;     // (One past) last index this core should process
} arg_t;

typedef struct
{
  int* arr1;
  int size1;
  int* arr2;
  int size2;
  int* mergedArray;
} arg_t_merge_two_arrays;


// Worker function
void work(void* arg_vptr)
{
  // Cast void* to argument pointer
  arg_t* arg_ptr = (arg_t*)arg_vptr;

  // Extract fields
  int* src = arg_ptr->src;
  int first = arg_ptr->first;
  int last = arg_ptr->last;

  // Perform sorting
  ubmark_sort(src, last - first);

}

//Mergesort algorithm

// Function to merge two sorted arrays
void mergeTwoArrays(void* arg_vptr){
  arg_t_merge_two_arrays* arg_ptr = (arg_t_merge_two_arrays*)arg_vptr;

  int* arr1 = arg_ptr->arr1;
  int size1 = arg_ptr->size1;
  int* arr2 = arg_ptr->arr2;
  int size2 = arg_ptr->size2;
  int* mergedArray = arg_ptr->mergedArray;


  int i = 0, j = 0, k = 0;
  // Merge elements from arr1 and arr2 in sorted order
  while (i < size1 && j < size2) {
    if (arr1[i] < arr2[j]) {
      mergedArray[k] = arr1[i];
      i++;

    } else {
      mergedArray[k] = arr2[j];
      j++;
    }
      k++;
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

// Main sorting function
void mtbmark_sort(int* x, int size)
{
  int block_size = (int)((int)(size/4));

  int size0 = block_size;
  int size1 = block_size;
  int size2 = block_size;
  int size3 = size - 3*block_size;

  arg_t arg0 = {x, 0, block_size};
  arg_t arg1 = {x+block_size, block_size, 2 * block_size};
  arg_t arg2 = {x+ 2*block_size, 2 * block_size, 3 * block_size};
  arg_t arg3 = {x+ 3*block_size, 3 * block_size, size};

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

  int* temp1 = ece4750_malloc((size0+size1)*(int)(sizeof(int)));
  int* temp2 = ece4750_malloc((size2+size3)*(int)(sizeof(int)));
  int* temp3 = ece4750_malloc((size)*(int)(sizeof(int)));

  arg_t_merge_two_arrays arg4 = {x, size0, x+block_size, size1, temp1};
  arg_t_merge_two_arrays arg5 = {x+ size0+size1, size2, x+ 3*block_size, size3, temp2};
  arg_t_merge_two_arrays arg6 = {temp1, size0+size1, temp2, size2+size3, temp3};

  ece4750_bthread_spawn(2, &mergeTwoArrays, &arg5);
  ece4750_bthread_spawn(1, &mergeTwoArrays, &arg4);

  ece4750_bthread_join(1);
  ece4750_bthread_join(2);

  mergeTwoArrays(&arg6);


  for (int i = 0; i < size; i++)
  {
    x[i] = temp3[i];
  }

  ece4750_free(temp1);
  ece4750_free(temp2);
  ece4750_free(temp3);
}