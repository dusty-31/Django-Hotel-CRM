def change_status_customer(customer, status: bool) -> None:
    customer.is_inhabited = status
    customer.save()
