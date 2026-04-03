#= 
# hdz_to_parquet.jl
# Converts all HDZ/PXZ Zeppelin files in a source directory to Parquet.
#
# Usage:
#   julia hdz_to_parquet.jl <source_dir> <target_dir>
#
# Example:
#   julia hdz_to_parquet.jl "C:\tmp\Chevy Caprise 422PC2 Front Passenger\neQuant.hdz" "C:\git\datascience-capstone\data\raw\NIST\brakes_chevy_front_passenger\neQuant.parquet"

=#

using NeXLParticle
using DataFrames
using Parquet2

function sanitize_df!(df::DataFrame)
    """Convert non-standard column types (ZepClass, Element, CategoricalValue, etc.)
    to strings so Parquet2 can write them."""
    for col in names(df)
        T = nonmissingtype(eltype(df[!, col]))
        if !(T <: Union{Number, String, Bool})
            df[!, col] = [ismissing(v) ? missing : string(v) for v in df[!, col]]
        end
    end
end

function find_hdz_files(source_dir::String)::Vector{String}
    """Find all .hdz files directly in source_dir (non-recursive)."""
    return [joinpath(source_dir, f) for f in readdir(source_dir)
            if isfile(joinpath(source_dir, f)) && lowercase(splitext(f)[2]) == ".hdz"]
end

function convert_hdz_to_parquet(source_dir::String, target_dir::String)
    # Create target directory if it doesn't exist
    mkpath(target_dir)

    hdz_files = find_hdz_files(source_dir)

    if isempty(hdz_files)
        println("No .hdz files found in: $source_dir")
        return
    end

    println("Found $(length(hdz_files)) .hdz file(s) in: $source_dir\n")

    success = 0
    failed = 0

    for hdz_path in hdz_files
        filename = splitext(basename(hdz_path))[1]
        parquet_path = joinpath(target_dir, "$filename.parquet")

        print("Converting: $(basename(hdz_path)) ... ")

        try
            zep = Zeppelin(hdz_path)
            df = zep.data
            sanitize_df!(df)
            Parquet2.writefile(parquet_path, df)
            println("OK  ($(nrow(df)) particles, $(ncol(df)) columns)")
            success += 1
        catch e
            println("FAILED")
            println("  Error: $e\n")
            failed += 1
        end
    end

    println("\nDone. $success succeeded, $failed failed.")
end

# --- Main ---
if length(ARGS) < 2
    println("Usage: julia hdz_to_parquet.jl <source_dir> <target_dir>")
    println("Example: julia hdz_to_parquet.jl \"C:\\data\\zips\" \"C:\\data\\parquet\"")
    exit(1)
end

source_dir = ARGS[1]
target_dir = ARGS[2]

if !isdir(source_dir)
    println("Error: Source directory does not exist: $source_dir")
    exit(1)
end

convert_hdz_to_parquet(source_dir, target_dir)
