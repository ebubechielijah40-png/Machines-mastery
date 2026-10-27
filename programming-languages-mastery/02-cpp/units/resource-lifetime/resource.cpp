// Original C++17 ownership mechanism: one resource, explicit deep copy and move.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstddef>
#include <iostream>
#include <stdexcept>
#include <utility>

struct Audit {
    static inline int live = 0;
    static inline int next_id = 0;
    static inline std::array<int, 64> released{};
    static inline std::size_t release_count = 0;
    static void release(int id) noexcept {
        assert(release_count < released.size());
        released[release_count++] = id;
    }
};

class Buffer {
    std::size_t size_;
    int* data_;
    int id_;
public:
    explicit Buffer(std::size_t size):size_(size),data_(size?new int[size]{}:nullptr),id_(++Audit::next_id) {
        if(data_)++Audit::live;
    }
    ~Buffer() noexcept {
        if(data_){delete[] data_;--Audit::live;Audit::release(id_);}
    }
    Buffer(const Buffer& other):Buffer(other.size_) {
        if(size_)std::copy(other.data_,other.data_+size_,data_);
    }
    Buffer(Buffer&& other) noexcept: size_(other.size_),data_(other.data_),id_(other.id_) {
        other.size_=0;other.data_=nullptr;other.id_=0;
    }
    friend void swap(Buffer& a,Buffer& b) noexcept {
        using std::swap;swap(a.size_,b.size_);swap(a.data_,b.data_);swap(a.id_,b.id_);
    }
    // Copy-and-swap: allocation/copy occurs before changing *this.
    Buffer& operator=(Buffer other) noexcept {swap(*this,other);return *this;}
    std::size_t size() const noexcept{return size_;}
    int id() const noexcept{return id_;}
    int& at(std::size_t i){if(i>=size_)throw std::out_of_range("buffer index");return data_[i];}
    const int& at(std::size_t i)const{if(i>=size_)throw std::out_of_range("buffer index");return data_[i];}
};

int main(){
    assert(Audit::live==0);
    {
        Buffer a(2);a.at(0)=7;
        Buffer b=a;b.at(0)=9;
        assert(a.at(0)==7 && b.at(0)==9 && Audit::live==2);
        int transferred=b.id();Buffer c=std::move(b);
        assert(c.id()==transferred && b.size()==0 && c.at(0)==9 && Audit::live==2);
        a=a;assert(a.at(0)==7 && Audit::live==2);
        a=c;assert(a.at(0)==9 && Audit::live==2);
        Buffer& alias=a;a=std::move(alias);assert(a.at(0)==9 && Audit::live==2);
        bool bounds=false;try{c.at(2)=1;}catch(const std::out_of_range&){bounds=true;}assert(bounds);
        Buffer empty(0);Buffer empty_copy=empty;assert(empty_copy.size()==0);
    }
    assert(Audit::live==0);
    std::size_t before=Audit::release_count;int first=0,second=0;
    try{
        Buffer one(1);first=one.id();Buffer two(1);second=two.id();
        throw std::runtime_error("controlled failure");
    }catch(const std::runtime_error&){}
    assert(Audit::live==0 && Audit::release_count==before+2);
    assert(Audit::released[before]==second && Audit::released[before+1]==first);
    std::cout<<"deep-copy independence: PASS\nmove leaves source empty: PASS\nself assignment: PASS\nreverse exception cleanup: PASS\nlive allocations: "<<Audit::live<<"\n";
}
