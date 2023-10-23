import pytest
from typing import Optional 
import pandas as pd
from beartype import beartype

from pandabear import DataFrame, Series, DataFrameModel, Field, Index, check_schemas, check, dataframe_check, SeriesModel
from pandabear.exceptions import SchemaValidationError, MissingIndexError


class MySchemaMissingColumnC(DataFrameModel):
    column_a: int = Field(gt=0)
    column_b: str = Field(str_contains="foo")
    my_prefix_column: int = Field(alias="my_prefix.+", regex=True, ge=0)

    class Config:
        filter = True

df = pd.DataFrame(
    dict(
        column_a=[1, 2, 3],
        column_b=["foo", "foo-bar", "baz-foo"],
        column_c=[0.1, 0.2, 0.3],
        my_prefix_column_a=[1, 2, 3],
        my_prefix_column_b=[4, 5, 6],
    )
)

@check_schemas
def my_function(df: DataFrame[MySchemaMissingColumnC], *args):
    assert "column_c" not in df.columns
    assert args == ('lol', )

my_function(df, 'lol')


######################################


# fix this case
class MySchema(DataFrameModel):
    index: Index[bool] = Field(alias="index\d", regex=True)
    column_a: int = Field(ge=0)

    class Config:
        coerce = True

df = pd.DataFrame(
    data=dict(column_a=[1, 2, 3]),
    index=pd.MultiIndex.from_arrays([["foo", "bar", "foo"], [0, 1, 2]], names=["index0", "index1"]),
)

df_out = MySchema.validate(df)

assert df_out.index.get_level_values('index0').dtype == bool
assert df_out.index.get_level_values('index1').dtype == bool

# Define a custom dataframe schema
class PlatformPerformanceData(DataFrameModel):
    index: Optional[Index[str]] = Field(alias="days_.+", regex=True)
    weekday: Optional[str] = Field(str_contains="day")
    spend: float = Field(alias="spend___.+", regex=True, ge=0)
    clicks: int = Field(alias="clicks___.+", regex=True, ge=0)
    # impressions: int = Field(alias="impressions___.+", regex=True, ge=0)
    
    class Config:
        filter = True
        coerce = True

df = pd.DataFrame(
    dict(
        days_since=[0, 1, 2, 3, 4, 5, 6],
        weekday=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        spend___facebook=[1000.1, 2000.2, 3000.3, 4000.4, 5000.5, 6000.6, 7000.7],
        spend___google=[1000.1, 2000.2, 3000.3, 4000.4, 5000.5, 6000.6, 7000.7],
        clicks___facebook=[100, 200, 300, 400, 500, 600, 700],
        clicks___google=[100, 200, 300, 400, 500, 600, 700],
        impressions___facebook=[100, 200, 300, 400, 500, 600, 700],
        impressions___google=[100, 200, 300, 400, 500, 600, 700],
    )
)

df = df.set_index("days_since")

@check_schemas
def my_func(df: DataFrame[PlatformPerformanceData]) -> DataFrame[PlatformPerformanceData]:
    return df

my_func(df)



# # class MySchema(DataFrameModel):
# #     foobar: int = Field(alias=("foo", "bar"), gt=0)
# #     foobaz: str = Field(alias=("foo", "baz"))

# #     class Config:
# #         strict = True


# # # Define an example dataframe that follows this schema
# # df = pd.DataFrame(
# #     dict(
# #         column_b=["foo", "foo-bar", "baz-foo"],
# #         my_prefix_column_a=[1, 2, 3],
# #         my_prefix_column_b=[4, 5, 6],
# #         other_prefix_column_a=[1, 2, 3],
# #     )
# # )
# # df.index = [1, 2, 3]
# # df.index.name = "date"

df = pd.DataFrame(
    data={"column1": [1, 2, 3]},
    index=pd.MultiIndex.from_arrays(
        [["foo", "bar", "foo"], [0, 1,2 ]],
        names=["index0", "index1"]
    )
)

# df = pd.DataFrame({
#     ("foo", "bar"): [1, 2, 3],
#     ("foo", "baz"): ["a", "b", "c"],
# })

# class MySchema(DataFrameModel):
#     date: Index[int] = Field(gt=0)
#     column_b: str = Field(str_contains="foo")
#     my_prefix_column: int = Field(alias="my_prefix.+", regex=True, ge=0)
#     other_prefix_column: int = Field(alias="other_prefix.+", regex=True, ge=0)

#     @check('my_prefix.+', regex=True)
#     def custom_check(column: pd.Series) -> bool:
#         return column.sum() > 0
    
#     class Config:
#         strict = True

# @check_schemas
# def my_function(df: DataFrame[MySchema]) -> DataFrame[MySchema]:

#     return df


# my_function(df)

