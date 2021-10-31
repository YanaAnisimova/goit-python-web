from .models import TransactionCategory, Transaction


def create_category(name: str, user_id) -> TransactionCategory:
    category = TransactionCategory(
        name=name,
        user_id=user_id,
    )
    category.save()
    return category


def create_transaction(amount, categories, user, comment) -> Transaction:
    transaction = Transaction(
        amount=amount,
        categories=categories,
        user=user,
        comment=comment
    )
    transaction.save()
    return transaction

