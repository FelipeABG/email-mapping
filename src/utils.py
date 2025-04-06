from email import message_from_string


def parse_email(path: str) -> tuple[str, list[str]]:
    with open(path, "r") as f:
        email_string = f.read()
        parsed = message_from_string(email_string)
        sender = parsed["From"]
        receiver = parsed["To"]

        if receiver is None:
            return sender, []

        return sender.strip(), [x.strip() for x in receiver.split(",")]
