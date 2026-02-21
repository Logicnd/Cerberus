import base64
import binascii


class Decoder:
    def base64_decode(self, s):
        try:
            return base64.b64decode(s).decode("utf-8", errors="ignore")
        except Exception:
            return ""

    def hex_decode(self, s):
        try:
            return bytes.fromhex(s).decode("utf-8", errors="ignore")
        except Exception:
            try:
                return binascii.unhexlify(s).decode("utf-8", errors="ignore")
            except Exception:
                return ""

    def rot13(self, s):
        tbl = str.maketrans(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
            "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm",
        )
        return s.translate(tbl)

    def xor_decode(self, data, key):
        if not key:
            return ""
        out = []
        kb = key.encode("utf-8")
        db = data.encode("utf-8")
        for i in range(len(db)):
            out.append(db[i] ^ kb[i % len(kb)])
        try:
            return bytes(out).decode("utf-8", errors="ignore")
        except Exception:
            return ""

    def auto(self, s):
        h = self.hex_decode(s)
        if h:
            return {"type": "hex", "decoded": h}
        b = self.base64_decode(s)
        if b:
            return {"type": "base64", "decoded": b}
        return {"type": "raw", "decoded": s}
