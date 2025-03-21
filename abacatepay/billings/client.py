from ..constants import (
    BASE_URL,
    BILLING_KINDS,
    BILLING_METHODS,
)
from ..products import Product
from .models import (
    BillingResponse,
    Customer,
)
from ..base.client import BaseClient
from logging import getLogger

logger = getLogger(__name__)


class BillingClient(BaseClient):
    def create(
        self,
        products: list[Product],
        returnURL: str,
        completionUrl: str,
        methods: list[BILLING_METHODS] = ["PIX"],
        frequency: BILLING_KINDS = "ONE_TIME",
        customerId: str | None = None,
        customer: Customer | None = None
    ) -> BillingResponse:


        """
        Create a new billing.

        Args:
            products: List of products to be billed.
            returnURL: The URL the user will be redirected to after the billing is completed.
            completionUrl: The URL the API will make a POST request after the billing is completed.
            methods: The payment methods to be accepted. Defaults to ["PIX"].
            frequency: The frequency of the billing. Defaults to "ONE_TIME".
            customerId: The ID of the customer. If provided, the customer information won't be required.
            customer: The customer information. If customerId is provided, this parameter is ignored.

        Returns:
            BillingResponse: The response with the billing data.
        """
        response = self._request(
            f"{BASE_URL}/billing/create",
            method="POST",
            json={
                "products": [product.model_dump() for product in products],
                "returnUrl": returnURL,
                "completionUrl": completionUrl,
                "methods": methods,
                "frequency": frequency,
                "customerId": customerId,
                **({"customer": customer.model_dump()} if customer is not None else {}),
            }
        )

        billing_data = BillingResponse(data=response.json()["data"])
        return billing_data

    def list(self) -> list[BillingResponse]:
        """
        List all bills.

        Returns:
            list[BillingResponse]: A list of billing responses.
        """
        logger.debug(f"Listing bills with URL: {BASE_URL}/billing/list")
        response = self._request(f"{BASE_URL}/billing/list", method="GET")
        return [BillingResponse(data=bill) for bill in response.json()["data"]]
