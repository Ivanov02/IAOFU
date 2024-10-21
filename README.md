# IAOFU

1. set the git:
  check the documentation if needed: https://www.jetbrains.com/help/pycharm/github.html#register-existing-account

2. imports of packages:
  in cmd (as administrator) type: 
    python -m pip install requests

3. you should create a python file named api_connection with a variable named api_key = "your_key". This is done to not expose the api_key.

How to mine the data:

**1. add this code in main:**
i = 0
while True:
    dict_source = get_match_details()
    dict_source_df = pd.DataFrame.from_dict(dict_source)

    dict_source_df.to_csv("YOUR_FILE_NAME.csv", sep=",", header=False, index=False, mode="a")
    time.sleep(120)
    print(f"RunNumer: {i}")
    i +=1

**2. add this code in constant and parameters**

Comment def_user_input and his call. Add below the following:

user_name = "Vonavi"   ADD YOUR USER_NAME HERE
user_tag_name = "EUNE"  ADD YOUR USER_TAG_NAME HERE
number_of_matches = 5

**3. Let the process run.**
