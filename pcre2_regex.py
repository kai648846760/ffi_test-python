from ffi import FFI

class Pcre2Regex:
    def __init__(self, pattern):
        self.pattern = pattern
        self.options = 0
        self.ffi = FFI()
        self.code = self.ffi.pcre2_compile(self.pattern, self.options)

    def match(self, subject):
        match_data = self.ffi.pcre2_match_data_create(self.code)
        result = self.ffi.pcre2_match(self.code, subject, match_data)
        self.ffi.pcre2_match_data_free(match_data)
        return result > 0

    def find_all_matches(self, subject):
        matches = []
        offset = 0
        subject_len = len(subject)
        while offset < subject_len:
            match_data = self.ffi.pcre2_match_data_create(self.code)
            result = self.ffi.pcre2_match(self.code, subject[offset:], match_data)
            if result > 0:
                ovector = self.ffi.pcre2_get_ovector_pointer(match_data)
                start = ovector[0]
                end = ovector[1]
                match_str = subject[offset + start:offset + end]
                matches.append(match_str)
                offset += end
            else:
                break
            self.ffi.pcre2_match_data_free(match_data)
        return matches