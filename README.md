## Ami_Coding_Pari_Na
### Step 1 : 
  create venv and install all dependencies which have requirements.txt
### Step 2 :
  For Singup:Use http://54.64.242.242:8000/create_user/  Api endpoint
  For Singin: Use http://54.64.242.242:8000/token/ Api endpoint.This returns access and refresh token
### Step 3 :
  Search Api: http://54.64.242.242:8000/search/
  <br>This endpoint allowed POST,GET method
  <br><b>POST</b>: There have been two input fields input_values and search_value.
        Output Will be printed True if the search value is in the input values. Otherwise, print False.And The search will be stored in the database under the user who is search
  <br><b>GET</b>:You get only your all search input value. If use two query_param: start_datetime,end_datetime .you get all input value between this datetime range
  
  
  ## Thank You
