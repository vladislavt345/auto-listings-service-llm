from src.core.password import hash_password, verify_password


def test_hash_and_verify_password() -> None:
    password = "test-password"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong-password", hashed) is False
