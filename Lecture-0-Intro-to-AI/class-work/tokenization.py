import tiktoken

encoder = tiktoken.get_encoding("gpt-4o")

print("Vocab size: ", encoder.n_vocab)

text = "This is a test sentence. Let's see how it gets tokenized!"
tokens = encoder.encode(text)

print("Tokens: ", tokens) # random tokens: [444, 554, 6775, 34554, 355]
