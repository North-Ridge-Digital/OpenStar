#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>

#ifndef _WIN32
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/select.h>
#include <sys/ioctl.h>
#else
#include <windows.h>
#include <io.h>
#include <fcntl.h>
// Undefine winsock's conflicting _IO/_IOR/_IOW/_IOWR macros
#undef _IO
#undef _IOR
#undef _IOW
#undef _IOWR
#endif

// Ioctl encoding macros (Linux <asm-generic/ioctl.h> style)
#define _IOC_NRBITS   8
#define _IOC_TYPEBITS 8
#define _IOC_SIZEBITS 14
#define _IOC_DIRBITS  2
#define _IOC_NRSHIFT   0
#define _IOC_TYPESHIFT (_IOC_NRSHIFT + _IOC_NRBITS)
#define _IOC_SIZESHIFT (_IOC_TYPESHIFT + _IOC_TYPEBITS)
#define _IOC_DIRSHIFT  (_IOC_SIZESHIFT + _IOC_SIZEBITS)
#define _IOC_NONE   0U
#define _IOC_WRITE  1U
#define _IOC_READ   2U
#define _IOC(dir,type,nr,size) \
    (((dir)<<_IOC_DIRSHIFT)|((type)<<_IOC_TYPESHIFT)|((nr)<<_IOC_NRSHIFT)|((size)<<_IOC_SIZESHIFT))
#define _IO(type,nr)        _IOC(_IOC_NONE, (type), (nr), 0)
#define _IOR(type,nr,size)  _IOC(_IOC_READ, (type), (nr), sizeof(size))
#define _IOW(type,nr,size)  _IOC(_IOC_WRITE, (type), (nr), sizeof(size))
#define _IOWR(type,nr,size) _IOC(_IOC_READ|_IOC_WRITE, (type), (nr), sizeof(size))

#include <wrs/v4l2wrap.h>
#include <wrs/videodev.h>

namespace {

struct v4l2_handle {
    int       fd;
    int       count;
    TWC_TSBUF* buffers;
};

#ifndef _WIN32
static int do_ioctl(int fd, unsigned long cmd, void* arg) {
    return ioctl(fd, cmd, arg);
}
#else
static int do_ioctl(int, unsigned long, void*) {
    return -1; // soon:tm:
}
#endif

} // anonymous namespace

int V4L2Open(char* device) {
    auto* h = (v4l2_handle*)calloc(1, sizeof(v4l2_handle));
    if (!h) return -1;
#ifndef _WIN32
    h->fd = open(device, O_RDWR);
#else
    h->fd = -1;
#endif
    if (h->fd < 0) { free(h); return -1; }
    h->count = 0;
    h->buffers = nullptr;
    return (int)(intptr_t)h;
}

int V4L2Close(int handle) {
    auto* h = (v4l2_handle*)(intptr_t)handle;
#ifndef _WIN32
    close(h->fd);
#endif
    if (h->buffers) free(h->buffers);
    free(h);
    return 0;
}

int V4L2GetFd(int handle) {
    return ((v4l2_handle*)(intptr_t)handle)->fd;
}

int V4L2QueryCapability(int handle, struct v4l2_capability* cap) {
    return do_ioctl(((v4l2_handle*)(intptr_t)handle)->fd, VIDIOC_QUERYCAP, cap);
}

int V4L2EnumImage(int handle, struct v4l2_fmtdesc* fmtdesc) {
    return do_ioctl(((v4l2_handle*)(intptr_t)handle)->fd, VIDIOC_ENUM_PIXFMT, fmtdesc);
}

int V4L2GetImageFormat(int handle, struct v4l2_format* fmt) {
    return do_ioctl(((v4l2_handle*)(intptr_t)handle)->fd, VIDIOC_G_FMT, fmt);
}

int V4L2SetImageFormat(int handle, struct v4l2_format* fmt) {
    return do_ioctl(((v4l2_handle*)(intptr_t)handle)->fd, VIDIOC_S_FMT, fmt);
}

int V4L2GetInput(int handle) {
    auto* h = (v4l2_handle*)(intptr_t)handle;
    int input;
    if (do_ioctl(h->fd, VIDIOC_G_INPUT, &input)) return -1;
    return input;
}

int V4L2SetInput(int handle, int input) {
    return do_ioctl(((v4l2_handle*)(intptr_t)handle)->fd, VIDIOC_S_INPUT, &input);
}

int V4L2GetOutput(int handle) {
    auto* h = (v4l2_handle*)(intptr_t)handle;
    int output;
    if (do_ioctl(h->fd, VIDIOC_G_OUTPUT, &output)) return -1;
    return output;
}

int V4L2SetOutput(int handle, int output) {
    return do_ioctl(((v4l2_handle*)(intptr_t)handle)->fd, VIDIOC_S_OUTPUT, &output);
}

int V4L2SetAudioInput(int handle, int input) {
    auto* h = (v4l2_handle*)(intptr_t)handle;
    struct v4l2_audio audio;
    memset(&audio, 0, sizeof(audio));
    audio.audio = input;
    return do_ioctl(h->fd, VIDIOC_S_AUDIO, &audio);
}

int V4L2SetControl(int handle, unsigned int id, int value) {
    auto* h = (v4l2_handle*)(intptr_t)handle;
    struct v4l2_control ctrl;
    ctrl.id = id;
    ctrl.value = value;
    return do_ioctl(h->fd, VIDIOC_S_CTRL, &ctrl);
}

int V4L2Stat(int handle, struct v4l2_performance* stats) {
    return do_ioctl(((v4l2_handle*)(intptr_t)handle)->fd, VIDIOC_G_PERF, stats);
}

int V4L2StreamOn(int handle, int type) {
    return do_ioctl(((v4l2_handle*)(intptr_t)handle)->fd, VIDIOC_STREAMON, &type);
}

int V4L2StreamOff(int handle, int type) {
    return do_ioctl(((v4l2_handle*)(intptr_t)handle)->fd, VIDIOC_STREAMOFF, &type);
}

int V4L2InitBuffers(int handle, unsigned char* storage, int offset, int size, int numBuffers) {
    auto* h = (v4l2_handle*)(intptr_t)handle;
    struct v4l2_agpinfo agp;
    struct v4l2_requestbuffers req;
    agp.offset = offset;
    agp.space = size;
    int ret = do_ioctl(h->fd, VIDIOC_S_AGP, &agp);
    if (ret) { printf("Failed to set agp info\n"); return ret; }
    req.count = numBuffers;
    ret = do_ioctl(h->fd, VIDIOC_REQBUFS, &req);
    if (ret) { printf("Failed in reqbufs\n"); return ret; }
    h->count = req.count;
    h->buffers = (TWC_TSBUF*)calloc(h->count, sizeof(TWC_TSBUF));
    if (!h->buffers) { printf("Failed in calloc\n"); return 0; }
    for (int i = 0; i < h->count; i++) {
        TWC_TSBUF* buf = &h->buffers[i];
        buf->v4l2buf.index = i;
        buf->v4l2buf.type = V4L2_BUF_TYPE_CAP_PLAY;
        ret = do_ioctl(h->fd, VIDIOC_QUERYBUF, &buf->v4l2buf);
        if (ret) return ret;
        if (storage) {
            buf->video = (TSH_FRAME*)(buf->v4l2buf.length * i + (uintptr_t)storage);
        } else {
#ifdef _WIN32
            buf->video = (TSH_FRAME*)VirtualAlloc(nullptr, buf->v4l2buf.length, MEM_COMMIT, PAGE_READWRITE);
#else
            buf->video = (TSH_FRAME*)mmap(nullptr, buf->v4l2buf.length, PROT_READ | PROT_WRITE, MAP_SHARED, h->fd, buf->v4l2buf.offset);
#endif
        }
        do_ioctl(h->fd, VIDIOC_QBUF, &buf->v4l2buf);
    }
    return h->count;
}

TWC_TSBUF* V4L2DQBuf(int handle, int block) {
    auto* h = (v4l2_handle*)(intptr_t)handle;
    struct v4l2_buffer vb;
    int ret = do_ioctl(h->fd, VIDIOC_DQBUF, &vb);
    if (block) {
#ifndef _WIN32
        fd_set fds;
        while (ret == -1) {
            FD_ZERO(&fds);
            FD_SET(h->fd, &fds);
            select(h->fd + 1, &fds, nullptr, nullptr, nullptr);
            ret = do_ioctl(h->fd, VIDIOC_DQBUF, &vb);
        }
#endif
    }
    memcpy(&h->buffers[vb.index].v4l2buf, &vb, sizeof(vb));
    return &h->buffers[vb.index];
}

TWC_TSBUF* V4L2GetBufInfo(int handle, int index) {
    auto* h = (v4l2_handle*)(intptr_t)handle;
    if (index < h->count) return &h->buffers[index];
    return nullptr;
}

int V4L2QBuf(int handle, TWC_TSBUF* buf) {
    return do_ioctl(((v4l2_handle*)(intptr_t)handle)->fd, VIDIOC_QBUF, &buf->v4l2buf);
}
