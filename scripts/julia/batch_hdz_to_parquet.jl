# batch_hdz_to_parquet.jl
# Converts HDZ/PXZ Zeppelin files to Parquet for multiple sample directories.
# Packages are loaded once, then all directory pairs are processed sequentially.
#
# Usage:
#   julia batch_hdz_to_parquet.jl
#
# Configuration:
#   Edit the `jobs` tuple below to define (source_dir, target_dir) pairs.

using NeXLParticle
using DataFrames
using Parquet2

# ============================================================
# CONFIGURE DIRECTORY PAIRS HERE
# Each entry is (source_dir, target_dir)
# ============================================================
jobs = [
    # --- Brakes: Chevy Caprise 422PC2 ---
    (raw"C:\tmp\Chevy Caprise 422PC2 Front Driver",
     raw"C:\git\datascience-capstone\data\raw\NIST\brakes_chevy_front_driver"),

    (raw"C:\tmp\Chevy Caprise 422PC2 Front Passenger",
     raw"C:\git\datascience-capstone\data\raw\NIST\brakes_chevy_front_passenger"),

    (raw"C:\tmp\Chevy Caprise 422PC2 Rear Driver",
     raw"C:\git\datascience-capstone\data\raw\NIST\brakes_chevy_rear_driver"),

    (raw"C:\tmp\Chevy Caprise 422PC2 Rear Passenger",
     raw"C:\git\datascience-capstone\data\raw\NIST\brakes_chevy_rear_passenger"),

    # --- Brakes: Ford Explorer A213 ---
    (raw"C:\tmp\Ford Explorer A213 Front Driver",
     raw"C:\git\datascience-capstone\data\raw\NIST\brakes_ford_a213_front_driver"),

    (raw"C:\tmp\Ford Explorer A213 Front Passenger",
     raw"C:\git\datascience-capstone\data\raw\NIST\brakes_ford_a213_front_passenger"),

    (raw"C:\tmp\Ford Explorer A213 Rear Driver",
     raw"C:\git\datascience-capstone\data\raw\NIST\brakes_ford_a213_rear_driver"),

    (raw"C:\tmp\Ford Explorer A213 Rear Passenger",
     raw"C:\git\datascience-capstone\data\raw\NIST\brakes_ford_a213_rear_passenger"),

    # --- Brakes: Ford Explorer B297 ---
    (raw"C:\tmp\Ford Explorer B297 Front Driver",
     raw"C:\git\datascience-capstone\data\raw\NIST\brakes_ford_b297_front_driver"),

    (raw"C:\tmp\Ford Explorer B297 Front Passenger",
     raw"C:\git\datascience-capstone\data\raw\NIST\brakes_ford_b297_front_passenger"),

    (raw"C:\tmp\Ford Explorer B297 Rear Driver",
     raw"C:\git\datascience-capstone\data\raw\NIST\brakes_ford_b297_rear_driver"),

    (raw"C:\tmp\Ford Explorer B297 Rear Passenger",
     raw"C:\git\datascience-capstone\data\raw\NIST\brakes_ford_b297_rear_passenger"),

    # --- Fireworks: Roman Candles ---
    (raw"C:\tmp\RomanCandles - Debris",
     raw"C:\git\datascience-capstone\data\raw\NIST\fireworks_romancandles_debris"),

    (raw"C:\tmp\RomanCandles - Post Cleanup",
     raw"C:\git\datascience-capstone\data\raw\NIST\fireworks_romancandles_postcleanup"),

    (raw"C:\tmp\RomanCandles - Post Handling Pre Ignition",
     raw"C:\git\datascience-capstone\data\raw\NIST\fireworks_romancandles_posthandle_preignite"),

    # --- Fireworks: Sparklers ---
    (raw"C:\tmp\Sparklers - Burning",
     raw"C:\git\datascience-capstone\data\raw\NIST\fireworks_sparklers_burning"),

    (raw"C:\tmp\Sparklers - Debris",
     raw"C:\git\datascience-capstone\data\raw\NIST\fireworks_sparklers_debris"),

    (raw"C:\tmp\Sparklers - Post Handling Post Burn",
     raw"C:\git\datascience-capstone\data\raw\NIST\fireworks_sparklers_posthandling_postburn"),

    # --- Fireworks: Spinners ---
    (raw"C:\tmp\Spinners - Debris",
     raw"C:\git\datascience-capstone\data\raw\NIST\fireworks_spinners_debris"),

    (raw"C:\tmp\Spinners - Post Cleanup",
     raw"C:\git\datascience-capstone\data\raw\NIST\fireworks_spinners_postcleanup"),

    (raw"C:\tmp\Spinners - Post Handling Pre Ignition",
     raw"C:\git\datascience-capstone\data\raw\NIST\fireworks_spinners_posthandling_preignite"),

    (raw"C:\tmp\Spinners - Post Ignition",
     raw"C:\git\datascience-capstone\data\raw\NIST\fireworks_spinners_postignite"),

    # --- Shooters ---
    (raw"C:\tmp\Shooter 1",
     raw"C:\git\datascience-capstone\data\raw\NIST\shooter_1"),

    (raw"C:\tmp\Shooter 2",
     raw"C:\git\datascience-capstone\data\raw\NIST\shooter_2"),

    (raw"C:\tmp\Shooter 3 L",
     raw"C:\git\datascience-capstone\data\raw\NIST\shooter_3L"),

    (raw"C:\tmp\Shooter 3 R",
     raw"C:\git\datascience-capstone\data\raw\NIST\shooter_3R"),

    (raw"C:\tmp\Shooter 4 L",
     raw"C:\git\datascience-capstone\data\raw\NIST\shooter_4L"),

    (raw"C:\tmp\Shooter 4 R",
     raw"C:\git\datascience-capstone\data\raw\NIST\shooter_4R"),

    (raw"C:\tmp\Shooter 5 L",
     raw"C:\git\datascience-capstone\data\raw\NIST\shooter_5L"),

    (raw"C:\tmp\Shooter 5 R",
     raw"C:\git\datascience-capstone\data\raw\NIST\shooter_5R"),
]

# ============================================================
# PROCESSING LOGIC — no need to modify below this line
# ============================================================

function sanitize_df!(df::DataFrame)
    for col in names(df)
        T = nonmissingtype(eltype(df[!, col]))
        if !(T <: Union{Number, String, Bool})
            df[!, col] = [ismissing(v) ? missing : string(v) for v in df[!, col]]
        end
    end
end

function find_hdz_files(source_dir::String)::Vector{String}
    return [joinpath(source_dir, f) for f in readdir(source_dir)
            if isfile(joinpath(source_dir, f)) && lowercase(splitext(f)[2]) == ".hdz"]
end

function convert_hdz_to_parquet(source_dir::String, target_dir::String)
    mkpath(target_dir)

    hdz_files = find_hdz_files(source_dir)

    if isempty(hdz_files)
        println("  No .hdz files found — skipping.")
        return (0, 0)
    end

    println("  Found $(length(hdz_files)) .hdz file(s)")

    success = 0
    failed = 0

    for hdz_path in hdz_files
        filename = splitext(basename(hdz_path))[1]
        parquet_path = joinpath(target_dir, "$filename.parquet")

        print("    $(basename(hdz_path)) -> $(filename).parquet ... ")

        try
            zep = Zeppelin(hdz_path)
            df = zep.data
            sanitize_df!(df)
            Parquet2.writefile(parquet_path, df)
            println("OK  ($(nrow(df)) particles, $(ncol(df)) columns)")
            success += 1
        catch e
            println("FAILED")
            println("      Error: $e")
            failed += 1
        end
    end

    return (success, failed)
end

# --- Run all jobs ---
println("Processing $(length(jobs)) job(s)...\n")

total_success = 0
total_failed = 0

for (i, (src, tgt)) in enumerate(jobs)
    println("[$i/$(length(jobs))] $(basename(src))")
    println("  Source: $src")
    println("  Target: $tgt")

    if !isdir(src)
        println("  ERROR: Source directory does not exist — skipping.")
        continue
    end

    s, f = convert_hdz_to_parquet(src, tgt)
    global total_success += s
    global total_failed += f
    println()
end

println("All done. $total_success file(s) converted, $total_failed failed.")
