
class PlannedTransaction():
    def __init__(self, selected_outputs, amount, address, change_public_key, change_address, fee, tx):
        self.selected_outputs = selected_outputs
        self.amount = amount
        self.change_public_key = change_public_key
        self.address = address
        self.change_address = change_address
        self.fee = fee
        self.tx = tx
