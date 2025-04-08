import tokzilla as tz

encoder_decoder = tz.Encoder(vocabSize=100)

text = "Hello, i'm using tokzilla module."

encoded = encoder_decoder.encode(text)
print(f"Encoded: {encoded}")

decoded = encoder_decoder.decode(encoded)
print(f"Decoded: {decoded}")
