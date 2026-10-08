"""
cryptokit — cli entry point.

usage:
    python cryptokit.py caesar --encrypt "msg" --key 3
    python cryptokit.py crack-caesar "encrypted stuff"
    python cryptokit.py vigenere --encrypt "msg" --key "secret"
    python cryptokit.py steg-hide --image in.png --message "msg" --output out.png
    python cryptokit.py steg-reveal --image out.png
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
    g.add_argument("--encrypt", metavar="MSG", help="message to encrypt")
    g.add_argument("--decrypt", metavar="MSG", help="message to decrypt")
    p_caesar.add_argument("--key", type=int, required=True, help="shift (0-25)")

    # crack caesar
    p_crack = sub.add_parser("crack-caesar", help="brute-force a caesar cipher")
    p_crack.add_argument("ciphertext", help="the encrypted message")
    p_crack.add_argument("--lang", default="fr", choices=["fr", "en"], help="language to match against")
    p_crack.add_argument("--top", type=int, default=5, help="number of results to show")

    # vigenere
    p_vig = sub.add_parser("vigenere", help="vigenere cipher")
    gv = p_vig.add_mutually_exclusive_group(required=True)
    gv.add_argument("--encrypt", metavar="MSG", help="message to encrypt")
    gv.add_argument("--decrypt", metavar="MSG", help="message to decrypt")
    p_vig.add_argument("--key", required=True, help="keyword for the cipher")

    # steg hide
    p_hide = sub.add_parser("steg-hide", help="hide a message inside a PNG image")
    p_hide.add_argument("--image", required=True, help="path to the input image")
    p_hide.add_argument("--message", required=True, help="message to hide")
    p_hide.add_argument("--output", required=True, help="path for the output image")
    p_hide.add_argument("--key", help="optional vigenere key to encrypt before hiding")

    # steg reveal
    p_reveal = sub.add_parser("steg-reveal", help="extract a hidden message from a PNG image")
    p_reveal.add_argument("--image", required=True, help="path to the image")
    p_reveal.add_argument("--key", help="optional vigenere key to decrypt after extracting")

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

    elif args.cmd == "vigenere":
        from crypto.vigenere import encrypt, decrypt

        if args.encrypt:
            print(encrypt(args.encrypt, args.key))
        else:
            print(decrypt(args.decrypt, args.key))

    elif args.cmd == "steg-hide":
        from steg.lsb import hide

        message = args.message
        if args.key:
            from crypto.vigenere import encrypt
            message = encrypt(message, args.key)

        hide(args.image, message, args.output)
        print(f"message hidden in {args.output}")

    elif args.cmd == "steg-reveal":
        from steg.lsb import reveal

        message = reveal(args.image)
        if args.key:
            from crypto.vigenere import decrypt
            message = decrypt(message, args.key)

        print(message)


if __name__ == "__main__":
    main()