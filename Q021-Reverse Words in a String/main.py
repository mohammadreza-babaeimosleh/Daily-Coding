class Solution:
    def reverseWords(self, s: str) -> str:
        words = []
        i = len(s) - 1

        while i >= 0:
            while i >= 0 and s[i] == " ":
                i -= 1

            end = i

            while i >= 0 and s[i] != " ":
                i -= 1

            if end >= 0:
                words.append(s[i + 1:end + 1])

        return " ".join(words)


class Solution:
    def reverseWords(self, s: str) -> str:
        return " ".join(s.split()[::-1])
