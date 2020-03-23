import pandas

source_docs = ["domestic-data.xlsx", "international-data.xlsx"]

for doc in source_docs:
    df = pandas.read_excel(doc)
    # throw away the rows we don't need
    df = df[["TypeOfGoods", "TypeOfGoods_Std"]]
    # remove null values
    df.dropna(inplace=True)
    # lowercase input, titlecase output
    df["TypeOfGoods"] = df["TypeOfGoods"].str.lower()
    df["TypeOfGoods_Std"] = df["TypeOfGoods_Std"].str.title()
    # remove rows where input is 'empty'
    df = df[df.TypeOfGoods != "empty"]

    seen_categories = {}

    def choose_ML_row_type(row):
        # assign row types to help AutoML create splits for
        # training, validation and testing, ensuring that there
        # is at least one row in each category
        # https://cloud.google.com/automl-tables/docs/prepare#split
        category = row["TypeOfGoods_Std"]
        if not seen_categories.get(category):
            seen_categories[category] = "validated"
            return "VALIDATE"
        elif seen_categories.get(category) == "validated":
            seen_categories[category] = "tested"
            return "TEST"
        elif seen_categories.get(category) in ["tested", "trained"]:
            seen_categories[category] = "trained"
            return "TRAIN"

    df["ML"] = df.apply(lambda row: choose_ML_row_type(row), axis=1)

    # remove any categories where we don't have a training value:
    for category, status in seen_categories.items():
        if status != "trained":
            print("removing category " + category)
            df = df[df.TypeOfGoods_Std != category]

    # export cleaned up CSV ready for analysis
    df.to_csv(
        doc.replace(".xlsx", ".csv"),
        index=False,
        header=["description", "category", "ML"],
    )
