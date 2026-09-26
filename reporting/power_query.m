// Power Query (M) — Automobile dataset cleaning
//
// Usage: Power BI Desktop > Get Data > Blank Query > Advanced Editor > paste this,
// then set FilePath below to the local path of automobiles.csv.
//
// NOTE: automobiles.csv is not committed to this repository (see README).
// Add your own copy locally to use this script — the transformation logic
// below mirrors src/data.py exactly (same columns, same CAFE threshold,
// same origin mapping), so results match the Python notebook.

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

    // src/data.py: clean_data() drops missing rows first
    RemoveMissing = Table.SelectRows(Typed, each
        List.AllTrue(List.Transform(Table.ColumnNames(Typed), (col) => Record.Field(_, col) <> null))
    ),

    // src/data.py: ORIGIN_MAP = {1: 'USA', 2: 'Europe', 3: 'Japan'}
    AddOriginName = Table.AddColumn(RemoveMissing, "origin_name", each
        if [origin_country] = 1 then "USA"
        else if [origin_country] = 2 then "Europe"
        else if [origin_country] = 3 then "Japan"
        else null,
        type text
    ),

    // src/data.py: CAFE_THRESHOLD_MPG = 24
    AddMeetsCafe = Table.AddColumn(AddOriginName, "meets_cafe", each [miles_per_gallon] >= 24, type logical)
in
    AddMeetsCafe
