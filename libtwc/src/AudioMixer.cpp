#include <twc/AudioMixer.hpp>
#include <cstdint>
#include <cstring>
#ifndef _WIN32
#include <unistd.h>
#else
#include <io.h>
#endif

namespace twc {
namespace {

static char temp_buf[128];
static MixAud mix_temp;

static void mixChannel(MixAud* dest, const MixAud* src) {
    int n = src->count;
    if (n > dest->count) n = dest->count;
    int i;
    for (i = 0; i < n; i++) {
        dest->mem[dest->stride * i] += static_cast<int>(*src->mem * src->level);
        const_cast<MixAud*>(src)->mem += src->stride;
    }
    const_cast<MixAud*>(src)->count -= i;
}

} // anonymous namespace

unsigned int AudioMixer::mix(MixAud** sources) {
    MixAud* dest = sources[0];
    MixAud* src  = sources[1];

    for (int i = 0; i < dest->stride * dest->count; i += dest->stride)
        dest->mem[i] = static_cast<int>(static_cast<long double>(dest->mem[i]) * dest->level);

    int idx = 2;
    while (src) {
        if (!src->mem) {
            mix_temp.count = src->count;
            if (static_cast<unsigned>(src->count) > static_cast<unsigned>(dest->count))
                mix_temp.count = dest->count;
            int bytes = mix_temp.count * 4 * src->stride;
            if (bytes > static_cast<int>(sizeof(temp_buf)))
                bytes = sizeof(temp_buf);
            read(src->file, temp_buf, static_cast<unsigned int>(bytes));
            src->count -= mix_temp.count;
            MixAud tmp{reinterpret_cast<int*>(temp_buf), 0, mix_temp.count, src->level, src->stride};
            mixChannel(dest, &tmp);
        } else {
            mixChannel(dest, src);
        }
        src = sources[idx++];
    }

    for (int i = 0; i < dest->stride * dest->count; i += dest->stride) {
        if (dest->mem[i] > 0x7FFFFF) dest->mem[i] = 0x7FFFFF;
        if (dest->mem[i] < -8388608) dest->mem[i] = -8388608;
    }

    return static_cast<unsigned>(dest->stride * dest->count);
}

} // namespace twc
