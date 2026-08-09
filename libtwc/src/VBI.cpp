#include <twc/VBI.hpp>
#include <cstdio>
#include <cstring>
#include <cstdint>

namespace twc {
namespace {

static const unsigned char vbi_cc_sine_data[128] = {
     17,0,0,0,  22,0,0,0,  29,0,0,0,  38,0,0,0,
     49,0,0,0,  61,0,0,0,  74,0,0,0,  87,0,0,0,
     99,0,0,0, 109,0,0,0, 117,0,0,0, 123,0,0,0,
    126,0,0,0, 126,0,0,0, 123,0,0,0, 117,0,0,0,
    109,0,0,0,  99,0,0,0,  87,0,0,0,  74,0,0,0,
     61,0,0,0,  49,0,0,0,  38,0,0,0,  29,0,0,0,
     22,0,0,0,  17,0,0,0,   0,0,0,0,   0,0,0,0,
      0,0,0,0,   0,0,0,0,   0,0,0,0,   0,0,0,0,
};

static void encodeClosedCaption(unsigned char* buf, const unsigned char* cc_data) {
    unsigned char* end = buf + 1439;

    for (int i = 0; i < 16; i++) { *buf++ = 0x80; *buf++ = 0x10; }
    for (int i = 0; i < 7; i++)
        for (int j = 0; j < 27; j++)
            { *buf++ = 0x80; *buf++ = vbi_cc_sine_data[4 * j]; }
    for (int i = 0; i < 54; i++) { *buf++ = 0x80; *buf++ = 0x10; }
    for (int i = 0; i < 27; i++) { *buf++ = 0x80; *buf++ = 0x7E; }

    int parity = 0;
    for (int i = 0; i < 7; i++) {
        unsigned char level = ((cc_data[0] >> i) & 1) ? 0x7E : 0x10;
        parity ^= ((cc_data[0] >> i) & 1);
        for (int j = 0; j < 27; j++) { *buf++ = 0x80; *buf++ = level; }
    }
    unsigned char level = static_cast<unsigned char>(parity ? 0x10 : 0x7E);
    for (int j = 0; j < 27; j++) { *buf++ = 0x80; *buf++ = level; }

    parity = 0;
    for (int i = 0; i < 7; i++) {
        level = ((cc_data[1] >> i) & 1) ? 0x7E : 0x10;
        parity ^= ((cc_data[1] >> i) & 1);
        for (int j = 0; j < 27; j++) { *buf++ = 0x80; *buf++ = level; }
    }
    level = static_cast<unsigned char>(parity ? 0x10 : 0x7E);
    for (int j = 0; j < 27; j++) { *buf++ = 0x80; *buf++ = level; }

    while (buf <= end) { *buf++ = 0x80; *buf++ = 0x10; }
}

static int vitcDecodeBit(unsigned char* data, int nbits_in) {
    int bit_pos = 7, acc_pos = 7, acc = 0, done = 0;
    if (!data || nbits_in <= 0) return -1;
    while (!done) {
        if (nbits_in <= 0) {
            *data += static_cast<unsigned char>(((acc >> acc_pos) & 1) << bit_pos);
            if (bit_pos) bit_pos--; else done = 1;
        } else {
            nbits_in--;
            acc = (((static_cast<int>(*data >> bit_pos) & 1) + 2 * acc));
            if (acc & 0x100) acc ^= 0x101;
        }
        if (bit_pos) bit_pos--; else { data++; bit_pos = 7; }
    }
    return acc;
}

static int vitcFormatData(unsigned char* raw, unsigned char* tc) {
    if (vitcDecodeBit(raw, 90)) return -1;
    tc[0] = 0;
    for (int i = 0; i <= 3; i++) { if ((32 >> i) & raw[0]) tc[0] += 1 << i; }
    for (int i = 0; i <= 1; i++) { if ((8 >> i) & raw[1]) tc[0] += 10 << i; }
    tc[1] = 0;
    for (int i = 0; i <= 1; i++) { if ((2 >> i) & raw[2]) tc[1] += 1 << i; }
    for (int i = 2; i <= 3; i++) { if ((512 >> i) & raw[3]) tc[1] += 1 << i; }
    for (int i = 0; i <= 2; i++) { if ((128 >> i) & raw[4]) tc[1] += 10 << i; }
    tc[2] = 0;
    for (int i = 0; i <= 3; i++) { if ((32 >> i) & raw[5]) tc[2] += 1 << i; }
    for (int i = 0; i <= 2; i++) { if ((8 >> i) & raw[6]) tc[2] += 10 << i; }
    tc[3] = 0;
    for (int i = 0; i <= 1; i++) { if ((2 >> i) & raw[7]) tc[3] += 1 << i; }
    for (int i = 2; i <= 3; i++) { if ((512 >> i) & raw[8]) tc[3] += 1 << i; }
    for (int i = 0; i <= 1; i++) { if ((128 >> i) & raw[9]) tc[3] += 10 << i; }
    return 0;
}

static int vitcDecodeLine(unsigned char* vbi_area, unsigned char* tc) {
    unsigned char raw[16];
    std::memset(raw, 0, sizeof(raw));
    unsigned char* scan = vbi_area + 1;
    unsigned char* peak = vbi_area;
    int byte_idx = 0, bit_pos = 7;
    unsigned char bit_val = 0;
    uintptr_t vbi_end = reinterpret_cast<uintptr_t>(vbi_area + 1440);

    while (*scan <= 0x26) { scan += 2; if (reinterpret_cast<uintptr_t>(scan) >= vbi_end) return -1; }

    for (int col = 0; col < 9; col++) {
        int clk = 16;
        while (*scan > 0x25) {
            if (*scan > *peak) peak = scan;
            scan += 2;
            if (reinterpret_cast<uintptr_t>(scan) >= vbi_end) return -1;
        }
        if (*peak <= 0x7D) return -1;
        bit_val = static_cast<unsigned char>(2 * bit_val + 1);
        scan = &peak[clk];
        peak = vbi_area;
        if (reinterpret_cast<uintptr_t>(scan) >= vbi_end) return -1;
        if (*scan > 0x7E) return -1;
        bit_val = static_cast<unsigned char>(2 * bit_val);
        if (++byte_idx == 8) { raw[col] = bit_val; bit_val = 0; byte_idx = 0; }
        for (int i = 0; i < 8; i++) {
            clk = (clk == 16) ? 14 : 16;
            scan += clk;
            if (reinterpret_cast<uintptr_t>(scan) >= vbi_end) return -1;
            if (*scan <= 0x7D) bit_val = static_cast<unsigned char>(bit_val * 2);
            else bit_val = static_cast<unsigned char>(2 * bit_val + 1);
            if (++byte_idx == 8) { raw[col] = bit_val; bit_val = 0; byte_idx = 0; }
        }
        if (col < 8) { scan += 14; if (reinterpret_cast<uintptr_t>(scan) >= vbi_end) return -1; }
    }
    raw[byte_idx] = static_cast<unsigned char>(bit_val << (8 - byte_idx));
    if (vitcFormatData(raw, tc) != -1) return 0;
    printf("FormatVITCData() failed.\n");
    return -1;
}

} // anonymous namespace

int VBIInject(uintptr_t frame, int field, int inject_type, const unsigned char* data) {
    if (!frame || !data) return -1;
    if (inject_type) return 0;
    encodeClosedCaption(reinterpret_cast<unsigned char*>(frame + (field << 11) + 1966080), data);
    return 0;
}

int VBIGetVITC(uintptr_t frame, unsigned char* tc) {
    if (!frame || !tc) return -1;
    if (!vitcDecodeLine(reinterpret_cast<unsigned char*>(frame + 1974272), tc)) return 0;
    if (!vitcDecodeLine(reinterpret_cast<unsigned char*>(frame + 2033664), tc)) return 0;
    printf("DecodeVITC() failed.\n");
    return -1;
}

} // namespace twc
