########################
# # 1
########################
class Encoder:
    def __init__(self, vocabSize=10000):
        self.vocabSize = vocabSize

    def encode(self, text):
        tokens = text.split()
        encodedTokens = []

        for token in tokens:
            asciiVal = "".join(
                str(ord(char)) for char in token
            )  # joins the ascii values in the empty string, ord() converts the char to ascii value

            encodedToken = int(asciiVal)
            encodedTokens.append(encodedToken)
        return encodedTokens

    def decode(self, encodedTokens):
        decodedTokens = []

        for number in encodedTokens:
            digits = str(number)
            i = 0
            token = ""

            while i < len(digits):
                if (
                    i + 3 <= len(digits) and 32 <= int(digits[i : i + 3]) <= 126
                ):  # first it'll check for 3 valid diigts acc to the ascii table, if not then 2
                    token += chr(int(digits[i : i + 3]))
                    i += 3
                elif i + 2 <= len(digits) and 32 <= int(digits[i : i + 2]) <= 126:
                    token += chr(int(digits[i : i + 2]))
                    i += 2
                else:
                    token += "<UNK>"
                    break

            decodedTokens.append(token)
        return " ".join(decodedTokens)


def main():
    encoder = Encoder()
    text = "Hey! Ravi this side."

    encoded = encoder.encode(text)
    print(f"Encoded: {encoded}")

    decoded = encoder.decode(encoded)
    print(f"Decoded: {decoded}")


if (
    __name__ == "__main__"
):  # useful ---> if the file if imported in another file, this code won't run, so main() won't be run in that case
    main()
