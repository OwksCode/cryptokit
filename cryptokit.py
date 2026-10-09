"""
cryptokit — cli entry point.

usage:
    python cryptokit.py caesar --encrypt "msg" --key 3
    python cryptokit.py crack-caesar "encrypted stuff"
    python cryptokit.py vigenere --encrypt "msg" --key "secret"
    python cryptokit.py steg-hide --image in.png --message "msg" --output out.png
    python cryptokit.py steg-reveal --image out.png
    python cryptokit.py rsa-keygen
    python cryptokit.py rsa-encrypt --pubkey rsa.pub --message "hello"
    python cryptokit.py rsa-decrypt --privkey rsa.priv --encrypted "123,456,789"
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
    p_hide.add_argument("--key", help="vigenere key to encrypt before hiding")
    p_hide.add_argument("--rsa-key", help="path to RSA public key for encryption")

    # steg reveal
    p_reveal = sub.add_parser("steg-reveal", help="extract a hidden message from a PNG image")
    p_reveal.add_argument("--image", required=True, help="path to the image")
    p_reveal.add_argument("--key", help="vigenere key to decrypt after extracting")
    p_reveal.add_argument("--rsa-key", help="path to RSA private key for decryption")

    # rsa keygen
    p_rkg = sub.add_parser("rsa-keygen", help="generate an RSA key pair")
    p_rkg.add_argument("--bits", type=int, default=16, help="bit length for prime generation")

    # rsa encrypt
    p_renc = sub.add_parser("rsa-encrypt", help="encrypt a message with RSA")
    p_renc.add_argument("--message", required=True, help="message to encrypt")
    p_renc.add_argument("--pubkey", required=True, help="path to the public key file")

    # rsa decrypt
    p_rdec = sub.add_parser("rsa-decrypt", help="decrypt a message with RSA")
    p_rdec.add_argument("--encrypted", required=True, help="comma-separated encrypted integers")
    p_rdec.add_argument("--privkey", required=True, help="path to the private key file")

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
        elif args.rsa_key:
            from crypto.rsa import encrypt, load_key
            key = load_key(args.rsa_key)
            pub = {"n": key["n"], "e": key["value"]}
            encrypted = encrypt(message, pub)
            message = ",".join(str(x) for x in encrypted)

        hide(args.image, message, args.output)
        print(f"message hidden in {args.output}")

    elif args.cmd == "steg-reveal":
        from steg.lsb import reveal

        message = reveal(args.image)
        if args.key:
            from crypto.vigenere import decrypt
            message = decrypt(message, args.key)
        elif args.rsa_key:
            from crypto.rsa import decrypt, load_key
            key = load_key(args.rsa_key)
            priv = {"n": key["n"], "d": key["value"]}
            numbers = [int(x) for x in message.split(",")]
            message = decrypt(numbers, priv)

        print(message)

    elif args.cmd == "rsa-keygen":
        from crypto.rsa import keygen, save_keys

        pub, priv = keygen(args.bits)
        save_keys(pub, priv, "rsa.pub", "rsa.priv")
        print("keys saved to rsa.pub and rsa.priv")

    elif args.cmd == "rsa-encrypt":
        from crypto.rsa import encrypt, load_key

        key = load_key(args.pubkey)
        pub = {"n": key["n"], "e": key["value"]}
        encrypted = encrypt(args.message, pub)
        print(",".join(str(x) for x in encrypted))

    elif args.cmd == "rsa-decrypt":
        from crypto.rsa import decrypt, load_key

        key = load_key(args.privkey)
        priv = {"n": key["n"], "d": key["value"]}
        numbers = [int(x) for x in args.encrypted.split(",")]
        print(decrypt(numbers, priv))


if __name__ == "__main__":
    main()