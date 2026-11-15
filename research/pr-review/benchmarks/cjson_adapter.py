from pathlib import Path
import subprocess
import sys

root=Path(__file__).resolve().parents[1]
src=Path(sys.argv[2]);build=Path(sys.argv[3])
def run(args,cwd=None):subprocess.run(list(map(str,args)),cwd=cwd,check=True,timeout=110)
tests=['parse_examples','parse_number','parse_hex4','parse_string','parse_array','parse_object','parse_value','print_string','print_number','print_array','print_object','print_value','misc_tests','parse_with_opts','compare_tests','cjson_add','readme_examples','json_patch_tests','old_utils_tests','misc_utils_tests']
if sys.argv[1]=='build':
    run(['gcc','-std=c99','-O3','-g','-fPIC','-shared',src/'cJSON.c','-o',build/'libcjson.so','-lm'])
    # A separate unmodified build is used only by the compatibility oracle, never by timings.
    run(['gcc','-std=c99','-O3','-fPIC','-shared',root/'repos/cJSON/cJSON.c','-o',build/'upstream.so','-lm'])
    run(['gcc','-std=c99','-O3','-g','-I',src,f'-DCORPUS_DIR="{root}/fixtures/cjson"',root/'benchmarks/cjson_bench.c','-L',build,'-lcjson',f'-Wl,-rpath,{build}','-o',build/'cjson_bench','-lm'])
    run(['gcc','-O0','-DUNITY_INCLUDE_DOUBLE','-c',src/'tests/unity/src/unity.c','-o',build/'unity.o'])
    for test in tests:
        extra=[src/'cJSON_Utils.c'] if test in tests[-3:] else []
        run(['gcc','-std=c99','-O0','-I',src,src/'tests'/f'{test}.c',build/'unity.o',*extra,'-o',build/test,'-lm'])
    run(['gcc','-std=c99','-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer','-I',src,src/'cJSON.c',root/'benchmarks/cjson_bounds.c','-o',build/'sanitizer-bounds','-lm'])
elif sys.argv[1]=='test':
    for test in tests:run([build/test],cwd=src/'tests')
    run([sys.executable,root/'benchmarks/cjson_validate.py',build/'libcjson.so',build/'upstream.so'])
    run([build/'sanitizer-bounds'])
else:raise ValueError(sys.argv[1])
