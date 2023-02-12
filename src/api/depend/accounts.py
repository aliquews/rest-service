from src.models.accounts import UserCreate


def validate_registration(user: UserCreate) -> None | int:
    props = [
        len(user.firstName.replace(" ", "")) if isinstance(user.firstName, str) else 0,
        len(user.lastName.replace(" ", "")) if isinstance(user.lastName, str) else 0,
        len(user.email.replace(" ", "")) if isinstance(user.email, str) else 0,
        len(user.password.replace(" ", "")) if isinstance(user.password, str) else 0,
    ]
    if not all(props):
        return 400
    return None