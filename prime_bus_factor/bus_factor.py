from argparse import Namespace

import pandas
from pandas import DataFrame, Series


from args import busFactorArgs
from typing import List

def buildBusFactor(df: DataFrame, *, bin: int, alpha: float = 0.0, stor: str = "busFactor") -> DataFrame:

    day_key: str = "author_days_since_0"
    lastday: int = df[day_key].max() + bin
    bins: List[Series] = list(range(0, lastday, bin))

    df["commitBin"] = pandas.cut(df[day_key], bins=bins, include_lowest=True)
    bins = df["commitBin"].unique().tolist()

    match alpha:
        case x if x > 0:
            days_since_0 = bins.left.astype(int).clip(lower=0)

            abs_list = lambda l: [abs(item) for item in l]
            significance = alpha * df.groupby("commitBin")["dkloc"].apply(lambda x: sum(abs_list(x.to_list())))
    
            df["author_dloc"] = df.groupby(["commitBin", "author_email"])["dkloc"].transform(lambda x: sum(abs_list(x.tolist())))

            df["bf"] = (df.groupby(["commitBin", "author_email"])["author_dloc"].transform(lambda x: x.gt(significance).sum()).groupby("commitBin").sum())
            
            data = [{"days_since_0": d, stor: bf} for d, bf in zip(days_since_0, df.groupby("commitBin")["bf"].max())]
        case _:
            data = [{"days_since_0": d, stor: len(authors)} for d, authors in zip(days_since_0, df.groupby("commitBin")["author_email"].nunique())]

    return DataFrame(data)


# def buildBusFactor(
#     df: DataFrame, *, bin: int, alpha: float = 0.0, stor: str = "busFactor"
# ) -> DataFrame:
#     day_key = "author_days_since_0"
#     lastday = df[day_key].max() + bin
#     bins = list(range(0, lastday, bin))

#     df["commitBin"] = pandas.cut(df[day_key], bins=bins, include_lowest=True)
#     bins = df["commitBin"].unique().tolist()

#     data = []
#     # Vectorized 
#     for bin in bins:

#         item = {"days_since_0": int(bin.left) if bin.left > 0 else 0}

#         if alpha > 0:
#             temp = df[df["commitBin"] == bin]
#             abs_list = lambda l: [abs(item) for item in l]
#             significance = alpha * sum(abs_list(temp["dkloc"].tolist()))

#             bf = 0
#             authors = set(temp["author_email"].tolist())
#             for author in authors:
#                 author_dloc = sum(
#                     abs_list(temp[temp["author_email"] == author]["dkloc"].tolist())
#                 )
#                 if author_dloc > significance:
#                     bf += 1

#             temp = temp[temp["dkloc"] > significance]

#             item[stor] = bf
#         else:
#             item[stor] = len(df[df["commitBin"] == bin]["author_email"].unique())

#         data.append(item)

#     return DataFrame(data)


def main() -> None:

    args: Namespace = busFactorArgs()

    match (args.bin, args.alpha):
        case (x, y) if x < 1:
            print(f"Bin argument must be an integer greater than 0: {bin_value}")
            quit(1)
        case (x, y) if y > 1 or y < 0:
            print("Invalid alpha value. Must be alpha <= 1 and alpha >= 0")
            quit(2 if y > 1 else 3)



    df: DataFrame = pandas.read_json(args.input).T
    bf: DataFrame = buildBusFactor(df, bin=args.bin, alpha=args.alpha, stor="busFactor")
    cd: DataFrame = buildBusFactor(df, bin=args.bin, alpha=0, stor="developerCount")

    cdColumn = cd["developerCount"]
    bf.join(cdColumn).to_json(args.output, indent=4)


if __name__ == "__main__":
    main()
