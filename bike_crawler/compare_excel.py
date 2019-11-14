import pandas as pd, sys

input1_val=sys.argv[1]
sheet1_name= sys.argv[2]
input2_val= sys.argv[3]
sheet2_name= sys.argv[4]
key_val= sys.argv[5]
output_val= sys.argv[6]

df1 = pd.read_excel(input1_val,sheet1_name)
df2 = pd.read_excel(input2_val,sheet2_name)

df_join= pd.merge(df1, df2, left_on=key_val, right_on=key_val, how='outer')
df_join['idx'] = ''
iter_join = df_join.iterrows()
print(type(iter_join))
for i,j in iter_join:
    if (df_join.Rent_name_x[i] != df_join.Rent_name_y[i]):
        df_join.idx[i] = df_join.idx[i]+'U'

    if (df_join.latitude_x[i] != df_join.latitude_y[i]):
        df_join.idx[i] = df_join.idx[i]+'X'

    if (df_join.logitude_x[i] != df_join.logitude_y[i]):
        df_join.idx[i] = df_join.idx[i]+'Y'

    if (isinstance(df_join.Rent_name_x [i], str) == False ):
        df_join.idx[i] = 'New'    
    if (isinstance(df_join.Rent_name_y [i], str) == False ):
        df_join.idx[i] = 'Del' 

df_join.to_excel(output_val)

