#ifndef TWC_VBI_HPP
#define TWC_VBI_HPP

#include <cstdint>

namespace twc {

int VBIInject(uintptr_t frame, int field, int inject_type, const unsigned char* data);
int VBIGetVITC(uintptr_t frame, unsigned char* tc);

} // namespace twc

#endif // TWC_VBI_HPP
