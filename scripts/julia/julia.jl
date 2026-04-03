# Julia Docs: https://docs.julialang.org

#=
Use the following commands in the Julia REPL to install packages for working with the NFI particle data. 
You only need to run these commands once to install the packages on your system. 
=#
using Pkg
Pkg.add("NeXLParticle")
Pkg.add("DataFrames")
Pkg.add("Parquet2")

# Now you can use the packages in your Julia code.
using NeXLParticle
using DataFrames
using Parquet2

#=
Steps for loading a Zeppelin (HDZ/PXZ pair)
=#

# Point to the .hdz file — the .pxz must be alongside it
# zep = Zeppelin("path/to/your/file.hdz")
zep = Zeppelin("C:\\tmp\\Chevy Caprise 422PC2 Front Passenger\\data.hdz")

# Load the particle data into a DataFrame
df = zep.data

# Optional sanity checks:
println("Number of particles: ", nrow(df))
println("Columns in the DataFrame: ", names(df))
println("Shape: ", size(df))
first(df, 5)  # Show the first 5 rows of the DataFrame

# Write raw data to Parquet
Parquet2.writefile("C:\\git\\datascience-capstone\\data\\raw\\NIST\\brakes_chevy_front_passenger\\data.parquet", df)

#=
NOTE: 
    DataFrame may contain data types that Parquet doesn't support.
    Convert all non-standard column types to strings before writing.
=#
for col in names(df)
    T = eltype(df[!, col])
    if !(T <: Union{Number, Missing, String, Bool})
        df[!, col] = string.(df[!, col])
    end
end