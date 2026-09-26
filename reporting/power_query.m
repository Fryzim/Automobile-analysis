// Power Query (M) — Automobile dataset cleaning
//
// Usage: Power BI Desktop > Get Data > Blank Query > Advanced Editor > paste this,
// then point FilePath at your local copy of automobiles.csv (the file is
// committed at the root of this repo).
//
// Same cleaning rules as the Python notebook: drop rows with missing values,
// map origin_country (1/2/3) to a readable label, and flag CAFE compliance
// at the 24 mpg threshold.

let
    FilePath = "C:\Path\To\Automobile-analysis\automobiles.csv",

    Source = Csv.Document(
        File.Contents(FilePath),
        [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),

    Typed = Table.TransformColumnTypes(PromotedHeaders, {
        {"miles_per_gallon", type number},
        {"cylinders", Int64.Type},
        {"displacement", type number},
        {"horsepower", type number},
        {"weight_lbs", type number},
        {"acceleration", type number},
        {"model_year", Int64.Type},
        {"origin_country", Int64.Type}
    }),

    RemoveMissing = Table.SelectRows(Typed, each
        List.AllTrue(List.Transform(Table.ColumnNames(Typed), (col) => Record.Field(_, col) <> null))
    ),

    AddOriginName = Table.AddColumn(RemoveMissing, "origin_name", each
        if [origin_country] = 1 then "USA"
        else if [origin_country] = 2 then "Europe"
        else if [origin_country] = 3 then "Japan"
        else null,
        type text
    ),

    // CAFE (Corporate Average Fuel Economy) threshold used throughout the analysis
    AddMeetsCafe = Table.AddColumn(AddOriginName, "meets_cafe", each [miles_per_gallon] >= 24, type logical)
in
    AddMeetsCafe
