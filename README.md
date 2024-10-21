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
# def user_inputs():
#     user_name = str(input('Enter the user name: ').strip() or "Vonavi")
#     user_tag_name = str(input('Enter the user tag: ').strip() or "EUNE")
#     number_of_matches = int(input('Numer of matches to run: ').strip() or '10')
#
#     return user_name, user_tag_name, number_of_matches



# user_name, user_tag_name, number_of_matches = user_inputs()
user_name = "Vonavi"   ADD YOUR USER_NAME HERE
user_tag_name = "EUNE"  ADD YOUR USER_TAG_NAME HERE
number_of_matches = 5

unique_combination = user_name + user_tag_name
last_run = pd.read_csv("last_run.csv", sep=",", index_col=False)

if unique_combination in last_run['unique_combination'].values:
    match_to_pull_from = last_run.last_pulled.iat[-1] + 1
    number_of_matches_to_pull = number_of_matches
    last_pulled = last_run.last_pulled.iat[-1] + number_of_matches
else:
    match_to_pull_from = 0
    number_of_matches_to_pull = number_of_matches
    last_pulled = number_of_matches

**3. Let the process run.**
