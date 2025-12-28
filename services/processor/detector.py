from config import HIGH_VALUE_THRESHOLD_WEI


def detect(tx: dict):
    """
    Detects whether a transaction should trigger an alert.
    Returns an alert dict or None.
    """
    value = int(tx.get("value_wei", 0))

    if value >= HIGH_VALUE_THRESHOLD_WEI:
        return {
            "type": "HIGH_VALUE_TRANSFER",
            "tx_hash": tx["tx_hash"],
            "from": tx["from"],
            "to": tx["to"],
            "value_wei": value,
            "block_number": tx["block_number"],
        }

    return None

