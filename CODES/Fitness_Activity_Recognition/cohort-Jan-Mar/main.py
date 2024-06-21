import yaml
import pprint

# 1,1 means that every single frame is taken as a data point
config_num = str(0)
frames = 1
steps = 1
test_size = 0.25

if __name__ == '__main__':
    with open("config.yaml") as f:
        yaml_content = yaml.safe_load(f)

    print(yaml_content.get('remove_from_target_list'))
    # pprint.pprint(yaml_content['remove_from_target_list'][0])
