import plantix 

from urllib.error import HTTPError

# from collections import Counter

def test_version_can_be_read():
    '''This test is just to make sure the packaging is OK'''
    assert plantix.__version__ is not None

def test_plantix_expert_is_correctly_built():
    try: 
        result_0  = plantix.PlantixApiClient().get('0')
        
        assert result_0.uid is not None
        assert result_0.topics is not None and isinstance(result_0.topics, list)
        assert result_0.following is not None and isinstance(result_0.following, list)

    except HTTPError: 
        pass

def test_find_topics_works_ok_for_user_0():
    try: 
        topics_0 = plantix.PlantixApiClient().find_topics('0', 1)

        assert len(topics_0) == 1 
        crop, occurrences = topics_0[0][0], topics_0[0][1]
        assert crop == 'cucumber'
        assert occurrences == 5
        
    except HTTPError:
        pass

