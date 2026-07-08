import os

def run(cmd):
    print(f"\n>> {cmd}")
    code = os.system(cmd)
    if code != 0:
        print("\nERROR! Pipeline stopped.")
        exit(1)

print("=" * 40)
print("TXN v0.3")
print("=" * 40)

print("\n1. Full Pipeline")
print("2. Fetch Only")
print("3. Normalize Only")
print("4. Export Cryptact")
print("5. Export Koinly")
print("6. Export Both")
print("0. Exit")

choice = input("\nSelect: ").strip()

if choice == "1":
    run("python fetch.py")
    run("python normalize.py")
    run("python exporters/cryptact.py")
    run("python exporters/koinly.py")
    print("\n✅ Done!")
    print("Files are in output/")

elif choice == "2":
    run("python fetch.py")

elif choice == "3":
    run("python normalize.py")

elif choice == "4":
    run("python exporters/cryptact.py")

elif choice == "5":
    run("python exporters/koinly.py")

elif choice == "6":
    run("python exporters/cryptact.py")
    run("python exporters/koinly.py")
    print("\n✅ Done!")
    print("Files are in output/")

elif choice == "0":
    print("Bye!")

else:
    print("Invalid option.")
