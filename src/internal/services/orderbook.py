from decimal import Decimal
import pandas as pd
import math

__all__ = ("aggregate_levels", )


def aggregate_levels(levels_df, agg_level  = Decimal("1"), side = "bid"):
    min_level = math.floor(Decimal(min(levels_df.price)) / agg_level - 1) * agg_level
    max_level = math.ceil(Decimal(max(levels_df.price)) / agg_level + 1) * agg_level

    level_bounds = [float(min_level + agg_level * x) for x in range(int((max_level - min_level) // agg_level) + 1)]

    levels_df["bin"] = pd.cut(levels_df.price, bins=level_bounds, precision=10, right=side != "bid")

    levels_df = levels_df.groupby("bin", observed=True).agg(quantity=("quantity", "sum")).reset_index()

    levels_df["price"] = levels_df.bin.apply(
        lambda x: x.left if side != "bid" else x.right
    )

    levels_df = levels_df[levels_df.quantity > 0]

    levels_df = levels_df[["price", "quantity"]]

    return levels_df

