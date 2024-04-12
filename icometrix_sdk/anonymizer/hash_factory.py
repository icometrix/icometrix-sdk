import hashlib
from abc import abstractmethod
from typing import get_args

from icometrix_sdk.anonymizer.exceptions import HashAlgorithmException, HashSizeException
from icometrix_sdk.anonymizer.models import HashAlgo


class HashFactory:
    @staticmethod
    def create_hash_method(algo: HashAlgo, size=512, salt=None):
        if algo == "sha3":
            return SHA3(size)
        elif algo == "md5":
            return MD5()
        elif algo == "short_md5":
            return ShortMD5()
        else:
            supported = ", ".join(get_args(HashAlgo))
            raise HashAlgorithmException(f"No algorithm named {algo} is supported, valid values are {supported}")


class HashMethod:
    @abstractmethod
    def calculate_hash_from_bytes(self, input_obj: bytes) -> str:
        pass

    def calculate_hash(self, input_obj: str, encoding='utf-8') -> str:
        return self.calculate_hash_from_bytes(input_obj.encode(encoding))


class SHA3(HashMethod):
    def __init__(self, size=256):
        acceptable_capacities = [224, 256, 384, 512]
        if size not in acceptable_capacities:
            raise f"Invalid capacity for SHA3, should be any of {acceptable_capacities}"
        self.size = size

    def calculate_hash_from_bytes(self, input_obj: bytes):
        if self.size == 224:
            hash_obj = hashlib.sha3_224(input_obj)
        elif self.size == 256:
            hash_obj = hashlib.sha3_256(input_obj)
        elif self.size == 384:
            hash_obj = hashlib.sha3_384(input_obj)
        elif self.size == 512:
            hash_obj = hashlib.sha3_512(input_obj)
        else:
            raise HashSizeException(f"SHA3 does not support size {self.size}, "
                                    f"valid values are (224, 256, 384, 512)")

        digest = hash_obj.hexdigest()
        return digest


class MD5(HashMethod):
    def calculate_hash_from_bytes(self, input_obj: bytes):
        return hashlib.md5(input_obj, usedforsecurity=True).hexdigest()


class ShortMD5(HashMethod):
    """
    MD5 that is re-based to base10.
    """

    def calculate_hash(self, input_obj: str, encoding='utf-8') -> str:
        return self.calculate_hash_from_bytes(input_obj.encode(encoding))

    def calculate_hash_from_bytes(self, input_obj: bytes):
        md5_hash = MD5().calculate_hash_from_bytes(input_obj)
        return str(int(md5_hash, base=16))[:10]
