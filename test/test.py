#!/user/bin/env python
# -*- coding: utf-8 -*-
import unittest
import behave_to_cucumber
import json
import os

BEHAVE_JSON = os.path.dirname(os.path.realpath(__file__)) + "/fixtures/behave.json"
EXPECTED_JSON = os.path.dirname(os.path.realpath(__file__)) + "/fixtures/expected.json"
AUTORETRY_BEHAVE_JSON = os.path.dirname(os.path.realpath(__file__)) + "/fixtures/autoretry.json"
AUTORETRY_EXPECTED_JSON = os.path.dirname(os.path.realpath(__file__)) + "/fixtures/autoretry_expected.json"
AUTORETRY_DEDUPE_JSON = os.path.dirname(os.path.realpath(__file__)) + "/fixtures/autoretry_dedupe.json"


class TestB2C(unittest.TestCase):
    def test_convert(self):
        with open("/Users/luozhongwen/persion_script/behave_to_cucumber/test/fixtures/test_behave.json") as f:
            converted = behave_to_cucumber.convert(json.load(f))
            # logger.info(converted)
        with open("/Users/luozhongwen/persion_script/behave_to_cucumber/test/fixtures/test.json", 'w') as f:
            json.dump(converted, f, indent=4, separators=(',', ': '))

        # with open(EXPECTED_JSON) as f:
        #     expected_result = json.load(f)
        #
        # assert (sorted(converted) == sorted(expected_result))

    def test_autoretry_convert(self):
        with open(AUTORETRY_BEHAVE_JSON) as f:
            converted = behave_to_cucumber.convert(json.load(f))

        with open(AUTORETRY_EXPECTED_JSON) as f:
            expected_result = json.load(f)

        assert (sorted(converted) == sorted(expected_result))

    def test_dedupe_convert(self):
        with open(AUTORETRY_BEHAVE_JSON) as f:
            converted = behave_to_cucumber.convert(json.load(f), deduplicate=True)

        with open(AUTORETRY_DEDUPE_JSON) as f:
            expected_result = json.load(f)

        assert (sorted(converted) == sorted(expected_result))

    def test_ids_are_unique(self):
        with open(BEHAVE_JSON) as f:
            converted = behave_to_cucumber.convert(json.load(f))
            ids = []
            for feature in converted:
                ids.append(feature['id'])
                for element in feature['elements']:
                    ids.append(element['id'])

        assert (len(set(ids)) == 5)

    def test_str(self):
        test1 = "['Traceback (most recent call last):\n\t', '  File /tmp/octopus/octopus_python/lib/python3.9/site-packages/behave/model.py, line 1329, in run\n\t', '    match.run(runner.context)\n\t', '  File /tmp/octopus/octopus_python/lib/python3.9/site-packages/behave/matchers.py, line 98, in run\n\t', '    self.func(context, *args, **kwargs)\n\t', '  File features/steps/check_hyperion_client_step.py, line 350, in step_impl\n\t', '    context.checker.check_equal(except_data=sorted(context.except_data), actual_data=sorted(context.actual_data))\n\t', '  File /sensorsdata/main/packages/sgx/firefly/framework/service/check_center/hyperion_client_checker.py, line 19, in check_equal\n\t', '    assert except_data == actual_data\n\t', 'AssertionError\n\t', '\n\t', 'Captured logging:\n\t', 'INFO:framework.config.logger:\n\t',  期望数据是: [[' infinity', ' mothership', ' polaris', ' qatest', ' sbp', ' sca', ' sdf', ' sm', "
        print(len(test1))


if __name__ == '__main__':
    unittest.main()
