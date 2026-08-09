#ifndef TWC_AUDIOMIXER_HPP
#define TWC_AUDIOMIXER_HPP

#include <cstdint>
#include <cstdio>

namespace twc {

struct MixAud {
    int*   mem;
    int    file;
    int    count;
    float  level;
    int    stride;
};

class AudioMixer {
public:
    static void dump(const MixAud* ma);
    static unsigned int mix(MixAud** sources);
};

inline void AudioMixer::dump(const MixAud* ma) {
    printf("MIX_AUD @ 0x%p\n", (void*)ma);
    if (!ma) return;
    printf("\tmem = 0x%p\n", (void*)ma->mem);
    printf("\tfile = %d\n", ma->file);
    printf("\tcount = %d\n", ma->count);
    printf("\tlevel = %f\n", ma->level);
    printf("\tstride = %d\n", ma->stride);
}

} // namespace twc

#endif // TWC_AUDIOMIXER_HPP
