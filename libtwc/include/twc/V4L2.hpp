#ifndef TWC_V4L2_HPP
#define TWC_V4L2_HPP

#include <wrs/v4l2wrap.h>

namespace twc {

class V4L2Device {
    int handle_;
public:
    V4L2Device() : handle_(-1) {}
    explicit V4L2Device(const char* device) : handle_(V4L2Open(const_cast<char*>(device))) {}
    ~V4L2Device() { if (handle_ >= 0) V4L2Close(handle_); }

    V4L2Device(const V4L2Device&) = delete;
    V4L2Device& operator=(const V4L2Device&) = delete;
    V4L2Device(V4L2Device&& other) noexcept : handle_(other.handle_) { other.handle_ = -1; }
    V4L2Device& operator=(V4L2Device&& other) noexcept {
        if (this != &other) {
            if (handle_ >= 0) V4L2Close(handle_);
            handle_ = other.handle_;
            other.handle_ = -1;
        }
        return *this;
    }

    bool valid() const { return handle_ >= 0; }
    int raw() const { return handle_; }
    int fd() const { return V4L2GetFd(handle_); }

    int open(const char* device) {
        if (handle_ >= 0) V4L2Close(handle_);
        handle_ = V4L2Open(const_cast<char*>(device));
        return handle_;
    }
    void close() {
        if (handle_ >= 0) { V4L2Close(handle_); handle_ = -1; }
    }

    int queryCapability(struct v4l2_capability* cap) { return V4L2QueryCapability(handle_, cap); }
    int enumImage(struct v4l2_fmtdesc* fmtdesc) { return V4L2EnumImage(handle_, fmtdesc); }
    int getImageFormat(struct v4l2_format* fmt) { return V4L2GetImageFormat(handle_, fmt); }
    int setImageFormat(struct v4l2_format* fmt) { return V4L2SetImageFormat(handle_, fmt); }
    int getInput() { return V4L2GetInput(handle_); }
    int setInput(int input) { return V4L2SetInput(handle_, input); }
    int getOutput() { return V4L2GetOutput(handle_); }
    int setOutput(int output) { return V4L2SetOutput(handle_, output); }
    int setAudioInput(int input) { return V4L2SetAudioInput(handle_, input); }
    int setControl(unsigned int id, int value) { return V4L2SetControl(handle_, id, value); }
    int stat(struct v4l2_performance* stats) { return V4L2Stat(handle_, stats); }
    int streamOn(int type) { return V4L2StreamOn(handle_, type); }
    int streamOff(int type) { return V4L2StreamOff(handle_, type); }
    int initBuffers(unsigned char* storage, int offset, int size, int numBuffers) {
        return V4L2InitBuffers(handle_, storage, offset, size, numBuffers);
    }
    TWC_TSBUF* dequeueBuffer(int block) { return V4L2DQBuf(handle_, block); }
    TWC_TSBUF* getBufferInfo(int index) { return V4L2GetBufInfo(handle_, index); }
    int queueBuffer(TWC_TSBUF* buf) { return V4L2QBuf(handle_, buf); }
};

} // namespace twc

#endif // TWC_V4L2_HPP
