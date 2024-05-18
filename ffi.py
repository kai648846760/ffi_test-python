import ctypes

class FFI:
    def __init__(self):
        self.lib = ctypes.CDLL("/usr/lib64/libpcre2-8.so") 

        self.lib.pcre2_compile_8.restype = ctypes.c_void_p
        self.lib.pcre2_compile_8.argtypes = [
            ctypes.POINTER(ctypes.c_ubyte),
            ctypes.c_size_t,
            ctypes.c_uint32,
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_size_t),
            ctypes.c_void_p,
        ]

        self.lib.pcre2_match_data_create_from_pattern_8.restype = ctypes.c_void_p
        self.lib.pcre2_match_data_create_from_pattern_8.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

        self.lib.pcre2_match_8.restype = ctypes.c_int
        self.lib.pcre2_match_8.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_ubyte),
            ctypes.c_size_t,
            ctypes.c_size_t,
            ctypes.c_uint32,
            ctypes.c_void_p,
            ctypes.c_void_p,
        ]

        self.lib.pcre2_get_ovector_pointer_8.restype = ctypes.POINTER(ctypes.c_size_t)
        self.lib.pcre2_get_ovector_pointer_8.argtypes = [ctypes.c_void_p]

        self.lib.pcre2_match_data_free_8.argtypes = [ctypes.c_void_p]
        self.lib.pcre2_match_data_free_8.restype = None

        self.lib.pcre2_code_free_8.argtypes = [ctypes.c_void_p]
        self.lib.pcre2_code_free_8.restype = None

    def pcre2_compile(self, pattern, options):
        pattern_bytes = pattern.encode("utf-8")
        pattern_ptr = (ctypes.c_ubyte * len(pattern_bytes))(*pattern_bytes)
        errorcode = ctypes.c_int(0)
        erroroffset = ctypes.c_size_t(0)
        code = self.lib.pcre2_compile_8(
            pattern_ptr, len(pattern_bytes), options,
            ctypes.byref(errorcode), ctypes.byref(erroroffset), None
        )
        if code is None:
            raise ValueError(
                f"Compilation failed at offset {erroroffset.value}: error code {errorcode.value}")
        return code

    def pcre2_match_data_create(self, code):
        return self.lib.pcre2_match_data_create_from_pattern_8(code, None)

    def pcre2_match(self, code, subject, match_data):
        subject_bytes = subject.encode("utf-8")
        subject_ptr = (ctypes.c_ubyte * len(subject_bytes))(*subject_bytes)
        result = self.lib.pcre2_match_8(
            code, subject_ptr, len(subject_bytes), 0, 0, match_data, None)
        return result

    def pcre2_get_ovector_pointer(self, match_data):
        return self.lib.pcre2_get_ovector_pointer_8(match_data)

    def pcre2_match_data_free(self, match_data):
        self.lib.pcre2_match_data_free_8(match_data)

    def pcre2_code_free(self, code):
        self.lib.pcre2_code_free_8(code)