import yaml
# class Config():
#     def __init__(self):
#         self.channelid_global_announcements 

with open("config.yaml","r") as f:
    config = yaml.safe_load(f)
    # channelid_global_announcements = 
# test = [i[1] for i in enumerate(config["announcements"])] 
test = [i for i in config["announcements"]] 
print(config["announcements"])
print(test)