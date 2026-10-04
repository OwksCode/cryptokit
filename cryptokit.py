"""
cryptokit — cli entry point.

usage:
    python cryptokit.py caesar --encrypt "msg" --key 3
    python cryptokit.py crack-caesar "encrypted stuff"
    python cryptokit.py vigenere --encrypt "msg" --key "secret"
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        prog="cryptokit",
        description="classical cryptography and steganography toolkit"
    )
    sub = parser.add_subparsers(dest="cmd")

    # caesar
    p_caesar = sub.add_parser("caesar", help="caesar cipher")
    g = p_caesar.add_mutually_exclusive_group(required=True)
    g.add_argument("--encrypt", metavar="MSG")
    g.add_argument("--decrypt", metavar="MSG")
    p_caesar.add_argument("--key", type=int, required=True, help="shift (0-25)")

    # crack caesar
    p_crack = sub.add_parser("crack-caesar", help="brute-force a caesar cipher")
    p_crack.add_argument("ciphertext")
    p_crack.add_argument("--lang", default="fr", choices=["fr", "en"])
    p_crack.add_argument("--top", type=int, default=5, help="how many results to show")

    # TODO: add vigenere subparser (day 3-4)
    # TODO: add steg subparsers (week 2)
    # TODO: add rsa subparsers (week 3)

    args = parser.parse_args()

    if not args.cmd:
        parser.print_help()
        sys.exit(1)

    if args.cmd == "caesar":
        from crypto.caesar import encrypt, decrypt

        if args.encrypt:
            print(encrypt(args.encrypt, args.key))
        else:
            print(decrypt(args.decrypt, args.key))

    elif args.cmd == "crack-caesar":
        from crypto.caesar import crack

        results = crack(args.ciphertext, lang=args.lang)
        print(f"\ntop {args.top} guesses:\n")
        for i, r in enumerate(results[:args.top]):
            print(f"  {i+1}. key={r['key']:2d}  (score {r['score']:.2f})  {r['preview']}")
        print()


if __name__ == "__main__":
    main()