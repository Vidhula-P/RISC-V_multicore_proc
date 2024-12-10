//========================================================================
// Unit tests for mtbmark sort
//========================================================================

#include "ece4750.h"
#include "mtbmark-sort.h"
#include "ubmark-sort.dat"
//#include "stdlib.h"
#include "stdbool.h"

//------------------------------------------------------------------------
// is_sorted
//------------------------------------------------------------------------
// Helper function that returns 1 if sorted and 0 if unsorted

int is_sorted( int* x, int n )
{
  for ( int i = 0; i < n-1; i++ ) {
    if ( x[i] > x[i+1] )
      return 0;
  }
  return 1;
}

//------------------------------------------------------------------------
// test_case_1_sort_basic
//------------------------------------------------------------------------

void test_case_1_sort_basic()
{
  ECE4750_CHECK( L"test_case_1_sort_basic" );

  int a[]     = { 4, 1, 3, 66, 2, 5, 8, 7};
  int a_ref[] = { 1, 2, 3, 4, 5, 7, 8, 66};

  mtbmark_sort( a, 8 );

  for ( int i = 0; i < 8; i++ )
    ECE4750_CHECK_INT_EQ( a[i] , a_ref[i] );

  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// Test 2- Sort small negative integers
//------------------------------------------------------------------------

void test_case_2_sort_negative()
{
  ECE4750_CHECK( L"test_case_2_sort_negative" );

  int a[]     = { -4, -3, -6, -5, -23, -56, -101 };
  int a_ref[] = { -101, -56, -23, -6, -5, -4, -3 };

  mtbmark_sort( a, 7 );

  for ( int i = 0; i < 7; i++ )
    ECE4750_CHECK_INT_EQ( a[i] , a_ref[i] );
    
  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// Test 3- Sort small npositive and negative integers
//------------------------------------------------------------------------

void test_case_3_sort_combo()
{
  ECE4750_CHECK( L"test_case_3_sort_combo" );

  int a[]     = { -4,  3,  6, -5, 56, -101, 23 };
  int a_ref[] = { -101, -5, -4,  3,  6, 23, 56 };

  mtbmark_sort( a, 7 );

  for ( int i = 0; i < 7; i++ )
    ECE4750_CHECK_INT_EQ( a[i] , a_ref[i] );

  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// Test 4- Sort large posotive integers
//------------------------------------------------------------------------

void test_case_4_large_pos()
{
  ECE4750_CHECK( L"test_case_4_large_pos" );

  int a[]     = { 7643, 0, 27482, 56, 9572, 32767 };
  int a_ref[] = { 0, 56, 7643, 9572, 27482, 32767 };

  mtbmark_sort( a, 6 );

  for ( int i = 0; i < 6; i++ )
    ECE4750_CHECK_INT_EQ( a[i] , a_ref[i] );

  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// Test 5- Sort large negative integers
//------------------------------------------------------------------------

void test_case_5_large_neg()
{
  ECE4750_CHECK( L"test_case_5_large_neg" );

  int a[]     = { -7643, 0, -27482, -00056, -9572, -32767 };
  int a_ref[] = { -32767, -27482, -9572, -7643, -56, 0};

  mtbmark_sort( a, 6 );

  for ( int i = 0; i < 6; i++ )
    ECE4750_CHECK_INT_EQ( a[i] , a_ref[i] );

  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// Test 6- Sort large npositive and negative integers
//------------------------------------------------------------------------

void test_case_6_large_combo()
{
  ECE4750_CHECK( L"test_case_6_large_combo" );

  int a[]     = { 7643, 0, -27482, -56, -9572, 32767 };
  int a_ref[] = { -27482, -9572, -56, 0, 7643, 32767};

  mtbmark_sort( a, 6 );

  for ( int i = 0; i < 6; i++ )
    ECE4750_CHECK_INT_EQ( a[i] , a_ref[i] );

  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// Test 7- Sort integers sorted in opposite order
//------------------------------------------------------------------------

void test_case_7_sorted_desc()
{
  ECE4750_CHECK( L"test_case_7_sorted_desc" );

  int a[]     = { 32767, 7643, 450, 99, 8, -8, -56, -900, -9572, -27482};
  int a_ref[] = { -27482, -9572, -900, -56, -8, 8, 99, 450, 7643, 32767};

  mtbmark_sort( a, 10 );

  for ( int i = 0; i < 10; i++ )
    ECE4750_CHECK_INT_EQ( a[i] , a_ref[i] );

  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// Test 8- Sort integers already sorted in order
//------------------------------------------------------------------------

void test_case_8_sorted_asc()
{
  ECE4750_CHECK( L"test_case_8_sorted_asc" );

  int a[]     = { -27482, -9572, -900, -56, -8, 8, 99, 450, 7643, 32767};
  int a_ref[] = { -27482, -9572, -900, -56, -8, 8, 99, 450, 7643, 32767};

  mtbmark_sort( a, 10 );

  for ( int i = 0; i < 10; i++ )
    ECE4750_CHECK_INT_EQ( a[i] , a_ref[i] );

  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// Test 9- Sorting a large array
//------------------------------------------------------------------------

void test_case_9_very_long_dataset()
{
  ECE4750_CHECK( L"test_case_9_very_long_dataset" );

  int a[]     = { 2345, -8967, 12, -32768, 12345, 6789, -123, 34567, 56789, -4567, 0, 678, -999, 123, -12345, 456, 7890, -456, 21098, -1234, 3456, 78901, -789, 13579, -2345, 67890, -3456, 9876, -11111, 54321, -987, 987654, -123456, 7890, -23456, 3210, -56789, 123, -8765, 23456, 789012, -34567, 4321, 987, -12345, 65432, 123, 567, -98765, 2345, -1234, 123456, -9876, 6789, -4567, 3456, -7890, 234567, -5432, 765, 12345, -6789, 2345, -123, 78901, -45678, 234567, -78901, 123456, -98765, 54321, -1234, 4567, -7890, 23456, 789012, -34567, 9876, 5432, -5678, 78901, -4321, 56789, -8765, 12345};
  int a_ref[] = {-123456, -98765, -98765, -78901, -56789, -45678, -34567, -34567, -32768, -23456, -12345, -12345, -11111, -9876, -8967, -8765, -8765, -7890, -7890, -6789, -5678, -5432, -4567, -4567, -4321, -3456, -2345, -1234, -1234, -1234, -999, -987, -789, -456, -123, -123, 0, 12,123, 123, 123, 456, 567, 678, 765, 987, 2345, 2345, 2345, 3210, 3456, 3456, 4321, 4567, 5432, 6789, 6789, 7890, 7890, 9876, 9876, 12345, 12345, 12345, 13579, 21098, 23456, 23456, 34567, 54321, 54321, 56789, 56789, 65432, 67890, 78901, 78901, 78901, 123456, 123456, 234567, 234567, 789012, 789012, 987654};
  mtbmark_sort( a, 85 );

  for ( int i = 0; i < 85; i++ )
    ECE4750_CHECK_INT_EQ( a[i] , a_ref[i] );
  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// Test 10- Repeating sequence
//------------------------------------------------------------------------

void test_case_10_repeat()
{
  ECE4750_CHECK( L"test_case_10_repeat" );

  int a[]     = { 2, 2, 2, 2, 2 , 1};
  int a_ref[] = { 1, 2, 2, 2, 2 , 2};

  mtbmark_sort( a, 6 );

  for ( int i = 0; i < 6; i++ )
    ECE4750_CHECK_INT_EQ( a[i] , a_ref[i] );

  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// Test 11- random testing
//------------------------------------------------------------------------

//Generating a random array and pchecking if sorted

// void test_11_random_testing()
// {
//   ECE4750_CHECK( L"test_11_random_testing");
//   int a[10]; //An array with 10 elements

//   // bool test = true;

//   // Generate random values for the array
//   for (int i = 0; i < 10; i++) {
//     a[i] = rand() % 100; // Random numbers between 0 and 99
//   }
//   mtbmark_sort( a, 10 );

//   for (int i = 1; i < 10; i++) {
//     if(a[i] < a[i-1]){
//       ECE4750_CHECK_TRUE(false);
//       ece4750_wprintf(L"a[i] = %d", a[i]) ;
//     }
//     ECE4750_CHECK_TRUE(true);
//     ece4750_wprintf(L"a[i] = %d", a[i]) ;
//   }
//   ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
// }

//------------------------------------------------------------------------
// main
//------------------------------------------------------------------------

int main( int argc, char** argv )
{
  __n = ( argc == 1 ) ? 0 : ece4750_atoi( argv[1] );

  if ( (__n <= 0) || (__n == 1 ) ) test_case_1_sort_basic();
  else if ( __n == 2 ) test_case_2_sort_negative();
  else if ( __n == 3 ) test_case_3_sort_combo();
  else if ( __n == 4 ) test_case_4_large_pos();
  else if ( __n == 5 ) test_case_5_large_neg();
  else if ( __n == 6 ) test_case_6_large_combo();
  else if ( __n == 7 ) test_case_7_sorted_desc();
  else if ( __n == 8 ) test_case_8_sorted_asc();
  else if ( __n == 9 ) test_case_9_very_long_dataset();
  else if ( __n == 10) test_case_10_repeat();
  // else if ( __n == 11) test_11_random_testing();
  else ece4750_wprintf( L"Error: Invalid test case number %d!\nChoose between 1 and 11.", __n );

  ece4750_wprintf( L"\n\n" );
  return ece4750_check_status;
}
