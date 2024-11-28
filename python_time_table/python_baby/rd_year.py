def batcher():
    print("Enter your batch name")
    batches = ["CS51", "CS52", "CS53", "CS54", "CS55", "CS56", "CS57", "CS58", "CS59", "CS510", "CS511", "CS512",
               "EC51", "IT51", "IT52", "CE51", "BT51", "BI51", "CC51", "EM51"]
    for x in range(len(batches)):
        print(x + 1, ".  ", batches[x])
    print("21 .  Exit")
    while True:
        choice = input("Enter your choice (1-21): ")
        try:
            choice = int(choice)
            if 1 <= choice <= 20:

                batch = batches[choice - 1]
                print(f"You selected batch: {batch}")

                break
            elif choice == 21:
                print("Exiting...")
                exit(0)

                break
            else:
                print("Invalid input. Please enter a number between 1 and 30.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    return (batch)
