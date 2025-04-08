import tiktoken

encoder = tiktoken.encoding_for_model("gpt-4o")

print("Vocab size: ", encoder.n_vocab)

text = "This is a test sentence. Let's see how it gets tokenized!"
tokens = encoder.encode(text)

print("Tokens: ", tokens) # [2500, 382, 261, 1746, 21872, 13, 41021, 1921, 1495, 480, 8625, 6602, 2110, 0]

print("Decoded: ", encoder.decode(tokens)) # This is a test sentence. Let's see how it gets tokenized!
