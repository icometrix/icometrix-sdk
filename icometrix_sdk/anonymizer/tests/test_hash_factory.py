from icometrix_sdk.anonymizer.hash_factory import HashFactory


def test_hash_string_hash_factory():
    # Input data
    data = 'Patient Name'

    # Expected SHA3-256 hash
    expected_hash = '95fa47c8fb19996e4bdeed2c3fa7cc35ab013737fd8b562a51335302773c4b29'

    # Calculate the SHA3-256 hash
    hash_factory = HashFactory()
    hash_method = hash_factory.create_hash_method("sha3", 256)
    hash_digest = hash_method.calculate_hash(data)  # anonymizer._hash(data)

    # Verify the calculated hash matches the expected hash
    assert expected_hash == hash_digest


def test_sha3():
    dataset = [('BART_TEST.', '3fb8369208'), ('BART_TEST ', '077979f009'), ]

    # Calculate the SHA3-512 hash
    hash_factory = HashFactory()
    hash_method = hash_factory.create_hash_method("sha3", 512)

    # Verify the calculated hashes match the expected hashes
    for data, expected_hash in dataset:
        hash_digest = hash_method.calculate_hash(data)[:10]
        assert expected_hash == hash_digest


def test_short_md5():
    dataset = [('BART_TEST ', '1080702796'), ('BART_TEST.', '2994824863')]

    # Calculate the icometrix MD5 hash (MD5 in decimal format)
    hash_factory = HashFactory()
    hash_method = hash_factory.create_hash_method("short_md5")

    # Verify the calculated hash matches the expected hash
    for data, expected_hash in dataset:
        hash_digest = hash_method.calculate_hash(data)
        assert expected_hash == hash_digest, 'hash verification failed'
