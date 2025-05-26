def main():
    while True:
        message = input(">> ")
        response = chat(message)
        print("BOT:", response)


if __name__ == "__main__":
    main()
