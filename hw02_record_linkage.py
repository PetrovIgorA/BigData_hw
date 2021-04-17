from mrjob.job import MRJob
from mrjob.job import MRStep

import os
import numpy as np

import hw_base
from hw02_json_file import JSONFile

class MRRecordLinkage(MRJob):

    __FIRST_SHOP = 0
    __SECOND_SHOP = 1

    __SHOPS = ["dns", "citilink"]
    jsons = []

    def init(self):
        self.jsons.append(JSONFile.preparse_smartphones(self.__SHOPS[self.__FIRST_SHOP]))
        self.jsons.append(JSONFile.preparse_smartphones(self.__SHOPS[self.__SECOND_SHOP]))

    def cancel(self):
        pass

    def er_mapper(self, _, value):
        first_id = self.jsons[self.__FIRST_SHOP].get_id(value)
        second_id = MRRecordLinkage.record_linkage(value, self.jsons[self.__FIRST_SHOP].characteristics(value), self.jsons[self.__SECOND_SHOP])
        unique_id = MRRecordLinkage.make_unique_id(first_id, second_id)
        yield self.__FIRST_SHOP, (first_id, unique_id)
        yield self.__SECOND_SHOP, (second_id, unique_id)

    def er_reducer(self, key, values):
        list_ids = list(values)
        for first_id, unique_id in list_ids:
            yield key, (unique_id, self.make_data(self.jsons[key], first_id))

    def save_reducer(self, key, values):
        values = list(values)
        result = dict()
        for unique_id, data in values:
            result.update({unique_id : data})
        JSONFile.save(hw_base.ER_DATA_PATH + '/' + self.__SHOPS[key] + ".json", result)


    def steps(self):
        return [
            MRStep(mapper=self.er_mapper, reducer=self.er_reducer),
            MRStep(reducer=self.save_reducer)
        ]

    def make_data(self, json_file: JSONFile, id: int) -> dict:
        title = json_file.get_title_by_id(id)
        result_characteristics = json_file.characteristics(title).copy()
        result_characteristics.pop(JSONFile.INTERNAL_ID_STR)
        result_characteristics.update({JSONFile.SMARTPHONE_STR : title})
        return result_characteristics

    @staticmethod
    def record_linkage(first_title: str, first_characteristics: dict, second_smartphones) -> int:
        min_dists = [(1000000000000, {})]
        for title, characteristics in second_smartphones.data.items():
            current_dist = MRRecordLinkage.levenshtein_distance(first_title.lower(), title.lower())
            #hw_base.debug(current_dist, first_title, title)
            if min_dists[0][0] > current_dist:
                min_dists = [(current_dist, characteristics)]
            elif min_dists[0][0] == current_dist:
                min_dists.append((current_dist, characteristics))
        if len(min_dists) == 1:
            return min_dists[0][1].get(JSONFile.INTERNAL_ID_STR)
        second_characteristics = [chars for dist, chars in min_dists]
        # Resolve duplicates by characteristics for many same distances
        return MRRecordLinkage.resolve_duplicates(first_characteristics, second_characteristics)

    @staticmethod
    def levenshtein_distance(str1: str, str2: str) -> int:
        dist_matrix = np.zeros((len(str1) + 1, len(str2) + 1))

        for i in range(dist_matrix.shape[0]):
            dist_matrix[i, 0] = i
        for j in range(1, dist_matrix.shape[1]):
            dist_matrix[0, j] = j

        for i in range(1, dist_matrix.shape[0]):
            for j in range(1, dist_matrix.shape[1]):
                if str1[i - 1] != str2[j - 1]:
                    dist_matrix[i, j] = min(
                        dist_matrix[i - 1, j - 1],
                        dist_matrix[i, j - 1],
                        dist_matrix[i - 1, j]
                    ) + 1
                else:
                    dist_matrix[i, j] = min(
                        dist_matrix[i - 1, j - 1],
                        dist_matrix[i, j - 1] + 1,
                        dist_matrix[i - 1, j] + 1
                    )
        
        return dist_matrix[dist_matrix.shape[0] - 1, dist_matrix.shape[1] - 1]

    @staticmethod
    def resolve_duplicates(first_characteristics: dict, second_characteristics: list) -> int:
        for characteristic in second_characteristics:
            if first_characteristics.get(JSONFile.MEMORY_STR) == characteristic.get(JSONFile.MEMORY_STR):
                if first_characteristics.get(JSONFile.SCREEN_STR) == characteristic.get(JSONFile.SCREEN_STR):
                    return characteristic.get(JSONFile.INTERNAL_ID_STR)
        return -1

    @staticmethod
    def make_unique_id(first_id: int, second_id: int):
        return str(first_id) + "-" + str(second_id)

runner = MRRecordLinkage()

runner.init()
runner.run()
runner.cancel()
