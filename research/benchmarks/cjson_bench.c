#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <sys/resource.h>
#include "cJSON.h"
static double seconds(void) {
    struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t);
    return t.tv_sec+1e-9*t.tv_nsec;
}
static uint64_t tree_hash(const cJSON *n) {
    uint64_t h=0;
    for(;n;n=n->next) {
        h=h*131+(unsigned)n->type;
        if(n->string) for(const unsigned char *s=(const unsigned char*)n->string;*s;s++) h=h*33+*s;
        if(n->valuestring) for(const unsigned char *s=(const unsigned char*)n->valuestring;*s;s++) h=h*33+*s;
        if(n->child) h^=tree_hash(n->child);
    }
    return h;
}
static volatile uint64_t sink;
int main(int argc,char **argv) {
    if(argc!=2)return 2;
    char path[4096];
    if(snprintf(path,sizeof(path),"%s/%s.json",CORPUS_DIR,argv[1])>=(int)sizeof(path))return 2;
    FILE *f=fopen(path,"rb"); if(!f)return 3;
    fseek(f,0,SEEK_END);long length=ftell(f);rewind(f);if(length<=0)return 3;
    size_t n=(size_t)length;
    char *buf=malloc(n+1); if(!buf)return 3;
    if(fread(buf,1,n,f)!=n)return 3; fclose(f);buf[n]=0;
    cJSON *first=cJSON_ParseWithLength(buf,n+1); if(!first)return 4;
    uint64_t h=tree_hash(first);cJSON_Delete(first);
    size_t loops=(32u*1024u*1024u)/n;if(loops<1000)loops=1000;
    uint64_t check=0;
    double start=seconds();
    for(size_t i=0;i<loops;i++) {
        cJSON *v=cJSON_ParseWithLength(buf,n+1);if(!v)return 4;
        check+=(unsigned)v->type;cJSON_Delete(v);
    }
    double elapsed=seconds()-start;sink=check;
    struct rusage usage;getrusage(RUSAGE_SELF,&usage);
    printf("{\"seconds\":%.9f,\"checksum\":\"%llu:%llu\",\"peak_rss_kb\":%ld,\"bytes_per_call\":%zu,\"calls\":%zu}\n",elapsed,(unsigned long long)h,(unsigned long long)check,usage.ru_maxrss,n,loops);
    free(buf);return 0;
}
