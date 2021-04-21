from mrjob.job import MRJob
from mrjob.job import MRStep

import hw_base
from hw02_json_file import JSONFile
from hw03_resolve import Resolver

class MRFusion(MRJob):

    jsons = []

    TITLE_KEY = "Smartphone"

    def init(self):
        self.jsons.append(JSONFile(hw_base.ER_DATA_PATH + "/dns.json"))
        self.jsons.append(JSONFile(hw_base.ER_DATA_PATH + "/citilink.json"))

    def mapper_fuse(self, _, value):
        for json_file in self.jsons:
            characteristics = json_file.data.get(value)
            if characteristics is not None:
                yield value, characteristics

    def reducer_fuse_by(self, key, values):
        values = list(values)
        resolver = Resolver()
        if len(values) == 1:
            yield 1, MRFusion.fuse(values[0], values[0], resolver)
        else:
            result = values[0]
            for i in range(1, len(values)):
                result = MRFusion.fuse(result, values[i], resolver)
            yield 1, result

    def reducer_save(self, key, values):
        values = list(values)
        result = dict()
        for data in values:
            title = data.pop(self.TITLE_KEY)
            result.update({title : data})
        JSONFile.save(hw_base.FUSION_DATA_PATH, result)

    def steps(self):
        return [
            MRStep(mapper=self.mapper_fuse, reducer=self.reducer_fuse_by),
            MRStep(reducer=self.reducer_save)
        ]

    @staticmethod
    def fuse(data_1: dict, data_2: dict, resolver: Resolver) -> dict:
        result = dict()
        hw_base.debug(resolver)
        for characteristic, resolve_ch in resolver.resolve_dict.items():
            result.update({characteristic : resolve_ch(data_1.get(characteristic), data_2.get(characteristic))})
        return result
        

runner = MRFusion()
runner.init()
runner.run()
