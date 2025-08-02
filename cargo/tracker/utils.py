def increment_alpha(prefix):
    n = len(prefix)
    new_chars = list(prefix)
    carry = 1
    for i in range(n - 1, -1, -1):
        c = new_chars[i]
        num = ord(c) - ord('A')
        new_num = num + carry
        carry = new_num // 26
        new_num %= 26
        new_char = chr(ord('A') + new_num)
        new_chars[i] = new_char
        if carry == 0:
            break

    if carry:
        return None

    new_prefix = ''.join(new_chars)
    if new_prefix[0] < 'C':
        return None
    return new_prefix


def next_key(s):
    n = len(s)
    i = 0
    while i < n and s[i].isalpha():
        i += 1
    prefix = s[:i]
    suffix = s[i:]

    if suffix:
        num_val = int(suffix) if suffix else 0
        max_num_val = (10 ** len(suffix)) - 1

        if num_val < max_num_val:
            next_num = num_val + 1
            new_suffix = str(next_num).zfill(len(suffix))
            return prefix + new_suffix
        else:
            if prefix == "C" and len(prefix) == 1:
                return "CA001"
            else:
                new_prefix = increment_alpha(prefix)
                if new_prefix is None:
                    new_prefix = "C" + "A" * len(prefix)
                    new_suffix_length = 5 - len(new_prefix)
                    if new_suffix_length > 0:
                        new_suffix = "1".zfill(new_suffix_length)
                    else:
                        new_suffix = ""
                    return new_prefix + new_suffix
                else:
                    new_suffix_length = 5 - len(new_prefix)
                    if new_suffix_length > 0:
                        new_suffix = "1".zfill(new_suffix_length)
                    else:
                        new_suffix = ""
                    return new_prefix + new_suffix
    else:
        new_prefix = increment_alpha(prefix)
        if new_prefix is None:
            return None
        return new_prefix


# Пример использования:
key = "C0001"
for _ in range(10000):
    print(key)
    key = next_key(key)