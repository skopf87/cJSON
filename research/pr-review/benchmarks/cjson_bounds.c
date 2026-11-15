#define _GNU_SOURCE
#include <sys/mman.h>
#include <unistd.h>
#include <assert.h>
#include <string.h>
#include <stdio.h>
#include "cJSON.h"
int main(void) {
    size_t p=(size_t)sysconf(_SC_PAGESIZE);
    char *mem=mmap(NULL,2*p,PROT_READ|PROT_WRITE,MAP_ANONYMOUS|MAP_PRIVATE,-1,0);
    assert(mem!=MAP_FAILED);assert(mprotect(mem+p,p,PROT_NONE)==0);
    for(size_t n=2;n<512;n++) {
        char *s=mem+p-n;memset(s,'a',n);s[0]='"';s[n-1]='"';
        cJSON *v=cJSON_ParseWithLength(s,n);assert(v);assert(strlen(v->valuestring)==n-2);cJSON_Delete(v);
        s[n-1]='a';v=cJSON_ParseWithLength(s,n);assert(!v);
        s[n-1]='\\';v=cJSON_ParseWithLength(s,n);assert(!v);
    }
    munmap(mem,2*p);puts("1530 protected-page exact-boundary cases passed");return 0;
}
