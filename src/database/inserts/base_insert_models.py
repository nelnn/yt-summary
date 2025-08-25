"""Base insert models."""

from pydantic import BaseModel, Field, field_validator


class SQLInsertModel(BaseModel):
    """Base model for SQL insert operations.

    Critical: The order of fields in the model must match the order of parameters in the SQL template.

    Attributes:
        template (str): The SQL insert template.
        params (tuple): A tuple of parameters to be used in the SQL template.

    """

    template: str
    params: tuple = Field(default_factory=tuple)

    def model_post_init(self, __context: dict | None = None) -> None:
        """Return values in declared field order."""
        self.params = tuple(
            getattr(self, name) for name in type(self).model_fields if name not in {"template", "params"}
        )


# TODO: FIX list tuple.
class SQLInertManyModel(BaseModel):
    """Base model for SQL insert many operations.

    Critical: The order of fields in the model must match the order of parameters in the SQL template.

    Attributes:
        template (str): The SQL insert many template.
        params (list[tuple]): A list of tuples, each containing parameters for the SQL template.

    """

    template: str
    params: list[tuple] = Field(default_factory=list)

    def model_post_init(self, __context: dict | None = None) -> None:
        """Return values in declared field order."""
        self.params = [
            tuple(getattr(self, name) for name in type(self).model_fields if name not in {"template", "params"})
        ]
