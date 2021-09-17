import numpy
import utils

class ProblemTwo(object):
    def synapse_position_from_gids(
            self, gids, direction='AFFERENT', filterGids=None,
            applyRotation=False, applyTranslation=False, projection=None):
        '''
        Get position in space of synapses on a number of cells
        INPUT: gids, an iterable holding the gids of cells in the current circuit
        OPTIONAL: direction - 'AFFERENT' or 'EFFERENT', self explanatory
            filterGids, an iterable of valid pre (if direction='AFFERENT') or
            postsynaptic gids. Synapses not from cells in the list will be ignored.
            applyRotation,
            applyTranslation,
        RETURNS: a list with one entry per synapse holding its x,y,z positions
        '''
        ## (EXAMPLE CODE REVIEW COMMENT): No need to have dead code
        # linear interpolator
        #lin_interp = lambda x, y, d: (1 - d) * x + d * y
        if filterGids is not None:
            if direction == 'AFFERENT':
                syns = utils.synapse_property_from_gids(
                    gids, [
                        0, 2, 3, 4], direction=direction, projection=projection)
            else:
                syns = utils.synapse_property_from_gids(
                    gids, [
                        0, 5, 6, 7], direction=direction, projection=projection)

            syns = [numpy.vstack([x for (x, y) in zip(
                syn[:, 1:], map(int, syn[:, 0])) if y in filterGids]) for syn in syns]
        else:
            if direction == 'AFFERENT':
                syns = utils.synapse_property_from_gids(
                    gids, [
                        2, 3, 4], direction=direction, projection=projection)
            else:
                syns = utils.synapse_property_from_gids(
                    gids, [
                        5, 6, 7], direction=direction, projection=projection)
        returnme = self.__synapse_position_worker(gids, syns)

        if applyRotation:
            returnme = self.__apply_rotation(gids)

        if applyTranslation:
            returnme = self.__apply_translation(gids)

        return returnme
    def synapse_secDist_from_gids(
            self, gids, direction='AFFERENT', filterGids=None):
        '''
        Get distance of synapses from start of the section on a number of cells
        INPUT: gids, an iterable holding the gids of cells in the current circuit
        OPTIONAL: direction - 'AFFERENT' or 'EFFERENT', self explanatory
            filterGids, an iterable of valid pre (if direction='AFFERENT') or
            postsynaptic gids. Synapses not from cells in the list will be ignored.
        RETURNS: a list with one entry per synapse holding its section distance
        '''
        if filterGids is not None:
            if direction == 'AFFERENT':
                syns = utils.synapse_property_from_gids(
                    gids, [
                        0, 2, 3, 4], direction=direction)
            else:
                syns = utils.synapse_property_from_gids(
                    gids, [
                        0, 5, 6, 7], direction=direction)

            syns = [[x for (x, y) in zip(
                syn[:, 1:], map(int, syn[:, 0])) if y in filterGids] for syn in syns]
        else:
            if direction == 'AFFERENT':
                syns = utils.synapse_property_from_gids(
                    gids, [
                        2, 3, 4], direction=direction)
            else:
                syns = utils.synapse_property_from_gids(
                    gids, [
                        5, 6, 7], direction=direction)

        syns = [[[int(y[0]), int(y[1]), y[2]] for y in x] for x in syns]

        seg_pds = self.segment_secDist_from_gids(gids)
        return [[pd[i[0]][i[1]] + i[2] for i in syn]
                for pd, syn in zip(seg_pds, syns)]

    def __apply_rotation(self, gids):
        """ Apply the rotation around the y axis that neurons have in the circuit """
        returnme = utils.rotation(gids)
        return returnme

    def __apply_translation(self, gids):
        """ Apply the translation that neurons have in the circuit """
        returnme = utils.translation(gids)
        return returnme

    def __synapse_position_worker(self, gids, syns):
        """ This only exists to avoid a pylint R0914 error """
        syn_morph_idx = [[[int(z) for z in y] for y in x[:, 0:2]] for x in syns]
        seg_pos = utils.segment_position_from_gids(gids)
        seg_lgth = [[
                numpy.sqrt(
                    numpy.sum(
                        numpy.power(
                            numpy.diff(
                                x,
                                axis=0),
                            2),
                        axis=1)) for x in seg] for seg in seg_pos]

        return utils.get_interpolation(seg_pos, syn_morph_idx, syns, seg_lgth)

    @staticmethod
    def find_segment_type(segments):
        '''Keep only segments whose value is above the threshold for the given type
         segments length is usually > 100k '''
        segment_type = [0, 1, 2, 3]
        threshold_by_type = [0.1, 0.03, 0.15, 0.2]
        result = list()
        for segment in segments:
            for type_, threshold in zip(segment_type, threshold_by_type):
                if segment.type == type_:
                    if segment.value > threshold:
                        result.append(segment)
                        break
        return result
