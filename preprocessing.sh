cat Nat2019PublicUS.c20200506.r20200915.txt | cut -c 171-172,383,499-500 | sed -E "s/(..)(.)(..)/\1,\2,\3/" | sed '1s/^/n_previous_children,induction,gestation_weeks\n/' > births.csv
