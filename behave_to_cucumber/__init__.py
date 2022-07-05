'''
Copyright (c) 2016 Behalf Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
from loguru import logger


def convert(json_file, remove_background=False, duration_format=False, deduplicate=False):
    """
    remove_background:删除前置条件
    duration_format:持续时间格式化
    deduplicate:重复数据消除
    """
    # json_nodes are the scopes available in behave/cucumber json: Feature -> elements(Scnerios) -> Steps
    json_nodes = ['feature', 'elements', 'steps']
    # T这些字段在cucumber report中不存在，因此从behave转换时，我们需要删除这些字段
    # fields.
    fields_not_exist_in_cucumber_json = ['status', 'step_type']

    def format_level(tree, index=0, id_counter=0):
        for item in tree:
            # behave-json中的位置转换为uri和cumber-json中的行，拆分behave中elements中的location字段，拆分为功能文件uri，和element所在line
            uri, line_number = item.pop("location").split(":")
            item["line"] = int(line_number)
            for field in fields_not_exist_in_cucumber_json:
                if field in item:
                    item.pop(field)
            if 'tags' in item:
                # behave中的标记只是一个标记名列表，cucumber中的每个标记都有一个名称和行号。给没有@标记的tag，加上tag
                item['tags'] = [{"name": tag if tag.startswith('@') else '@' + tag, "line": item["line"] - 1} for tag in
                                item['tags']]
            if json_nodes[index] == 'steps':
                if 'result' in item:
                    # 由于长错误消息的几个问题，消息子串最多为2000个字符。
                    # TODO 需要对该bug进行修复，将",转换为"，/n/t
                    if 'error_message' in item["result"]:
                        error_msg = item["result"].pop('error_message')
                        logger.info(f'错误error_msg信息输出:{error_msg}')
                        for i in range(0, len(error_msg)):
                            if i == len(error_msg) - 1:
                                error_msg[i] = error_msg[i] + "\n"
                            else:
                                error_msg[i] = error_msg[i] + "\n\t"
                        # item["result"]["error_message"] = str((str(error_msg).replace("\"", "").replace("\\'", ""))[:2000]).split("[")[1].split("]")[0]
                        item["result"]["error_message"] = str((str(error_msg))[:len(error_msg)]).split("[")[1].split("]")[
                            0].replace("',", "").replace("'","")
                        print(item["result"]["error_message"])
                        logger.info(f'错误信息输出:{item["result"]["error_message"]}')
                    if 'duration' in item["result"] and duration_format:
                        item["result"]["duration"] = int(item["result"]["duration"] * 1000000000)
                else:
                    # 在behave中，跳过的测试在其json中没有结果对象，因此，当我们为每个跳过的测试生成Cucumber报告时，我们需要生成一个状态为skipped的新结果
                    item["result"] = {"status": "skipped", "duration": 0}
                if 'table' in item:
                    item['rows'] = []
                    t_line = 1
                    item['rows'].append({"cells": item['table']['headings'], "line": item["line"] + t_line})
                    for table_row in item['table']['rows']:
                        t_line += 1
                        item['rows'].append({"cells": table_row, "line": item["line"] + t_line})
            else:
                # uri is the name of the feature file the current item located
                # uri是当前项所在的功能文件的名称
                item["uri"] = uri
                item["description"] = ""
                item["id"] = id_counter
                id_counter += 1
            # If the scope is not "steps" proceed with the recursion
            # 如果范围不是“步骤”，则继续递归
            if index != 2 and json_nodes[index + 1] in item:
                item[json_nodes[index + 1]] = format_level(
                    item[json_nodes[index + 1]], index + 1, id_counter=id_counter
                )
        return tree

    # Option to remove background element because behave pushes it steps to all scenarios already
    # 删除背景元素的选项，因为behave将其推到所有场景中
    if remove_background:
        for feature in json_file:
            if feature['elements'][0]['type'] == 'background':
                feature['elements'].pop(0)

    if deduplicate:
        def check_dupe(current_feature, current_scenario, previous_scenario):
            if "autoretry" not in current_feature['tags'] and "autoretry" not in current_scenario['tags']:
                return False
            if previous_scenario['keyword'] != current_scenario['keyword']:
                return False
            elif previous_scenario['location'] != current_scenario['location']:
                return False
            elif previous_scenario['name'] != current_scenario['name']:
                return False
            elif previous_scenario['tags'] != current_scenario['tags']:
                return False
            elif previous_scenario['type'] != current_scenario['type']:
                return False
            else:
                return True

        for feature in json_file:
            # Create a working list
            scenarios = []

            # For each scenario in the feature
            for scenario in feature['elements']:
                # Append the scenario to the working list
                scenarios.append(scenario)

                # Check the previous scenario
                try:
                    # See if the previous scenario exists and matches
                    previous_scenario = scenarios[-2]
                    if check_dupe(feature, scenario, previous_scenario):
                        # Remove the earlier scenario from the working list
                        scenarios.pop(-2)
                except IndexError:
                    # If we're at the beginning of the list, don't do anything
                    pass

            # Replace the existing list with the working list
            feature['elements'] = scenarios

    # Begin the recursion
    return format_level(json_file)
