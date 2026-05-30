from typing import List

class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        res = []
        i = 0
        n = len(words)

        while i < n:
            # Pick as many words as fit in the current line
            line_len = len(words[i])
            j = i + 1

            while j < n and line_len + 1 + len(words[j]) <= maxWidth:
                line_len += 1 + len(words[j])
                j += 1

            line_words = words[i:j]
            num_words = len(line_words)

            # Last line or single-word line: left justify
            if j == n or num_words == 1:
                line = " ".join(line_words)
                line += " " * (maxWidth - len(line))
                res.append(line)

            else:
                # Fully justify
                total_word_len = sum(len(word) for word in line_words)
                total_spaces = maxWidth - total_word_len
                gaps = num_words - 1

                spaces_each = total_spaces // gaps
                extra_spaces = total_spaces % gaps

                line = ""

                for k in range(gaps):
                    line += line_words[k]
                    line += " " * spaces_each

                    # Left gaps get the extra spaces
                    if k < extra_spaces:
                        line += " "

                line += line_words[-1]
                res.append(line)

            i = j

        return res
