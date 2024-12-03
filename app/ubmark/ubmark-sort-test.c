//========================================================================
// Unit tests for ubmark sort
//========================================================================

#include "ece4750.h"
#include "ubmark-sort.h"
#include "ubmark-sort.dat"

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
// Test1- Basic
//------------------------------------------------------------------------

void test_case_1_sort_basic()
{
  ECE4750_CHECK( L"test_case_1_sort_basic" );

  int a[]     = { 4, 3, 6, 5 };
  int a_ref[] = { 3, 4, 5, 6 };

  ubmark_sort( a, 4 );

  for ( int i = 0; i < 4; i++ )
    ECE4750_CHECK_INT_EQ( a[i] , a_ref[i] );

  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// Test 2- Sort small negative integers
//------------------------------------------------------------------------

void test_case_2_sort_negative()
{
  ECE4750_CHECK( L"test_case_2_sort_negative" );

  int a[]     = { -4, -3, -6, -5 };
  int a_ref[] = { -6, -5, -4, -3 };

  ubmark_sort( a, 4 );

  for ( int i = 0; i < 4; i++ )
    ECE4750_CHECK_INT_EQ( a[i] , a_ref[i] );

  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// Test 3- Sort small npositive and negative integers
//------------------------------------------------------------------------

void test_case_3_sort_combo()
{
  ECE4750_CHECK( L"test_case_3_sort_combo" );

  int a[]     = { -4,  3,  6, -5 };
  int a_ref[] = { -5, -4,  3,  6 };

  ubmark_sort( a, 4 );

  for ( int i = 0; i < 4; i++ )
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

  ubmark_sort( a, 6 );

  for ( int i = 0; i < 4; i++ )
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

  ubmark_sort( a, 6 );

  for ( int i = 0; i < 4; i++ )
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

  ubmark_sort( a, 6 );

  for ( int i = 0; i < 4; i++ )
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

  ubmark_sort( a, 10 );

  for ( int i = 0; i < 4; i++ )
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

  ubmark_sort( a, 10 );

  for ( int i = 0; i < 4; i++ )
    ECE4750_CHECK_INT_EQ( a[i] , a_ref[i] );

  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

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
  else ece4750_wprintf( L"Error: Invalid test case number %d!\nChoose between 1 and 8.", __n );

  ece4750_wprintf( L"\n\n" );
  return ece4750_check_status;
}
