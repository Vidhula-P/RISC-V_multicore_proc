//========================================================================
// mtbmark-mfilt
//========================================================================
// This microbenchmark performancs a masked filter of a grayscale source
// image. The 3x3 filter is preset to be a blur like this:
//
//   0 6 0
//   6 8 6
//   0 6 0
//
// The filter is only applied if the corresponding pixel in the mask
// image is non-zero. The result is stored in the destination array.

#ifndef MTBMARK_MFILT_H
#define MTBMARK_MFILT_H

void mtbmark_mfilt( int* dest, int* mask, int* src, int size );

#endif /* MTBMARK_MFILT_H */

