import json

from collections import Counter
from dataclasses import dataclass
from http.client import HTTPResponse
from typing import List, Tuple
from urllib.request import Request, urlopen as send_request

from plantix.service import ADDRESS, PORT


@dataclass
class PlantExpert(object):
    """Represents a plantix community expert.
    
    Each expert has a unique id, a list of plants
    they can give advice on and a list of other
    expert uid-s they follow.
    """	
    uid: str
    topics: Tuple[str]
    following: Tuple[str]


class PlantixApiClient(object):
    """SDK for our Plantix Community REST API.
    """
    API_ENDPOINT = f"http://{ADDRESS}:{PORT}/community"

    def _fetch(self, method: str, resource: str) -> HTTPResponse:
        """Fetch a resource from the service endpoint over HTTP

        @param method: HTTP verb
        @param resource: Resource path
        """
        return send_request(
            Request(f"{self.API_ENDPOINT}{resource}", method=method)
        )

    def get(self, uid: str) -> PlantExpert:
        """Get a community plant expert by uid.

        @param uid: ID of the expert to fetch
        """
        response = self._fetch("GET", f"/experts/{uid}")
        topics, following = json.load(response)

        return PlantExpert(uid, topics, following)

    def find_topics(self, start: str, n: int) -> List:
        '''Returns a sorted list of the n most frequent topics 
        for user uid=start and her/his connections

        Args:
            start (str): User's uid
            n (int): Number of topics to return, sorted by frequency in decreasing order

        Returns:
            List: n first tuples of a list containing the topic and number of references to each topic
        '''

        response = self.get(start)
        topics, connections = response.topics, response.following

        # If the response is successful, let's create these structures to keep track 
        # of the connections already examined (visited dictionary), and the topics found along 
        # with their occurrence number across users (ranked_topics Counter)
        visited = dict({response.uid:True})
        ranked_topics = Counter(topics)

        self._visit_connections(connections, visited, ranked_topics)

        return ranked_topics.most_common()[:n]

    def _visit_connections(self, connections: List, visited: dict, ranked_topics: Counter) -> None:
        '''Visits all connections for the initial user, recording their topics

        This method interprets the users connected as a graph, and uses something similar to 
        a depth first search algorithm to visit all nodes of interest. 

        Args:
            connections (List): List of strings, each item representing a user connected to the 'start' user
            visited (dict): Dictionary used as a set, containing the users that have already been visited
            ranked_topics (Counter): Keeps track of the topics found and their occurrences
        '''
        for connection in connections:  
            if not visited.get(connection, 0):
                response = self.get(connection)
                ranked_topics.update(response.topics)
                visited.update({connection:True})
                self._visit_connections(response.following, visited, ranked_topics)

