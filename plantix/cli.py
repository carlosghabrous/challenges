import sys
from plantix.sdk import PlantixApiClient


def main(start="0", n=4, client=PlantixApiClient):

    print(f"\nTop {n} topics in the network of {start}")
    print("----------------------------------")

    for topic, count in client().find_topics(start, n):
        print(f"  {count} {topic}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
