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

        ## 1. The whole if/else with a nested if/else is not necessary and cumbersome. Makes the code difficult follow. 
        ## Paying a bit of attention to what happens in the different branches, all of them call the function 
        ## 'utils.synapse_property_from_gids' with the same arguments except the first one, the list of 'magic numbers' (eg. [0,2,3,4])
        ## One option could be to resolve the arguments first, and then pass them to the function. 
        ## For instance: 
        ## if filterGids is not None:
        ##     if direction == 'AFFERENT':
        ##         filter_list = [0, 2, 3, 4]
        ##      
        ##     else:
        ##         filter_list = [0, 5, 6, 7]
        ## Another option is to have the filter list previously stored in some sort of data structure. 
        ## For instance:
        ## filter_list_resolve = {'filterGids':{'AFFERENT':[0, 2, 3, 4], 'EFFERENT':[0, 5, 6, 7]}... }
        ## and then get the filter list from the dict like
        ## if filterGids is not None:
        ##     filter_list = filter_list_resolve['filterGids'].get(direction, some_default_value)

        ## 2. It is not checked whether the 'direction' argument can have not allowed values. For example, 'AFFERENT' is checked, but 
        ## not 'EFFERENT', there is just an 'else'. Maybe it makes sense, depending on the code's client. But using a dictionary like the one
        ## I suggested before solves the problem and checks for not-allowed values

        ## 3. Without knowing the context, it is just impossible to know what the 'magic numbers' mean. They should be coded using constants, 
        ## a class Enum or similar. 

        ## 4. Variables/arguments don't seem to follow the same naming convention. For instance, 'filterGids'. PEP8, as far as I recall, recommends
        ## to use this_naming_convention_for_variables_functions_and_arguments

        if filterGids is not None:
            if direction == 'AFFERENT':
                syns = utils.synapse_property_from_gids(
                    gids, [
                        0, 2, 3, 4], direction=direction, projection=projection)
            else:
                syns = utils.synapse_property_from_gids(
                    gids, [
                        0, 5, 6, 7], direction=direction, projection=projection)

            ## 5. It is not that it is impossible to understand, but there should be a balance between code 'compression' and 'clarity'. 
            ## I find this list comprehension difficult to understand at a first sight. 

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
        
        ## 6. A line break should have been included here
        returnme = self.__synapse_position_worker(gids, syns)

        if applyRotation:
            returnme = self.__apply_rotation(gids)

        if applyTranslation:
            returnme = self.__apply_translation(gids)

        return returnme

    ## 7. A line break should have been included here
    ## 8. The same comments that I wrote for function 'synapse_position_from_gids' can be applied here as well. 

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

        ## 9. Also, difficult to understand at first sight
        syns = [[[int(y[0]), int(y[1]), y[2]] for y in x] for x in syns]

        seg_pds = self.segment_secDist_from_gids(gids)

        ## 10. Also, difficult to understand at first sight
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
        ## 11. This doc string is very weird. What exists to avoid the pylint error? The doc string itself? Some part of the code? 
        ## If it is just the docstring, then include a docstring that makes sense, and that in turn explains what the operations
        ## this function does.

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

        ## 12. Later in the code, segment types are extracted from the 'segment' objects in 'segments' argument. 
        ## Why include it twice by creating the list 'segment_type' here? 
        ## It seems that 'segment_type' and 'threshold_by_type' should not be here, but in the segment object (class Segment?)
        ## Also, I would have encoded this with a dictionary: segment_type_to_threshold = {0:0.1, 1:0.03...}

        ## 13. If the goal is to be able to filter segments by 'segment_type' and 'threshold_by_type', maybe they could be arguments of the 
        ## function. Also, it seems what happens in the loops could be solved by applying a 'filter' function to the 'segments' list. 
        
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
