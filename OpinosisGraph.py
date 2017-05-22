fromA collections import namedtuple
import networkx as nx

WordUnit = namedtuple("WordUnit", ['token', 'pos'] )
OpinosisParamters = namedtuple("OpinosisParameters", ["redundancy", "summary_size", "gap", "valid_start_node"])
PRIEntry = namedtuple("PRIEntry", ['SID', 'PID'])

class OpinosisGraph:
    def __init__(self, sentences = [], parameters, well_formed_rules = None):
        ''' Initializes the graph utilizing the passed sentences. 
            
            Sentences should be formatted as a list of lists of tokenized terms.
        '''
        assert isinstance(parameters, OpinosisParameters), "parameters must be of type OpinosisParameters"
        self.clear()
        self.sentences = sentences
        self.parameters = parameters
        self.build_graph(sentences)
  
        # TODO: develop protocol to import well-formed rules

    def clear(self):
        self.graph = nx.DiGraph()
        self.pri = dict()
        self.sentences = []
        
        
    def build_graph(self):
        ''' Builds the  graph utilizing only sentences

            Sentences should be formatted as a list of lists of tokenized terms
        '''
        # Clear out the older graph

        for SID, sentence in enumerate(sentences):
            for PID, wordunit in enumerate(sentence):
                assert isinstance(wordunit, WordUnit), "sentences must be a list of list of word units"
                label = wordunit.token
                if self.graph.has_node(label):
                    self.pri[label].add(PRIEntry(SID, PID))
                else:
                    self.graph.add_node(label)
                    self.pri[label] = set(PRIEntry[(SID, PID)])
                # add edge to previous node 
                if PID != 0 and not self.graph.has_edge(sentence[PID-1].token, label):
                    self.graph.add_edge(sentence[PID-1].token, label)

    def is_VSN(self, label):
        ''' Returns true if the provided label corresponds to a valid start node

            A valid start node is one such that avg(PID) <= sigma_vsn where PID is the 
            position of occurrence for the node with provided label
        '''
        # TODO: space out better
        return self.graph.has_node(label) and sum([prientry.PID for prientry in self.pri[label]]) / len(self.pri[label]) <= self.paramaters.valid_start_node

    def is_VEN(self, label):
        ''' Returns true if the provided label corresponds to a valid end node
       
            A valid end node is one that naturally is terminating, i.e. it is punctuation or a 
            coordinating conjunction
        '''
        # TODO: define naturally for tweets
        pass

    def is_valid_path(self, path):
        ''' Returns true if the path, a list of labels, is a valid path

            A valid path is one such that is_VSN(path[0]) == True, is_VEN(path([-1]) == True and 
            the path is  well-formed
        '''
        
        if len(path) <= 0:
            return False # an empty path fails
        
        if not self.is_VSN(path[0]):
            return False # first node must be a start node

        if not self.is_VEN(path[-1]):
            return False # last node must be an end node

        return is_well_formed(path)

    def is_well_formed(self, path):
        ''' Returns true if the path obeys some predefined set of grammatical rules '''
        # TODO: define by importing rules and then validating for a given path
        pass
    
    def path_score(self, path, metric = "basic"):
        ''' Assigned score to a path '''
        # TODO: everything
        pass 

    def is_collapsible(self, label):
        ''' Returns true if the node with that label is collapsible

            Collapsible is defined as being a verb
        '''
        # TODO: is this definition still okay for twitter?
        for prientry in self.pri[label]:
            if self.sentences[prientry.SID][prientry.PID].pos == 'V':
                return True
        return False

    def build_summary(self):
        ''' Builds an opinosis summary from the graph. 
            The graph must already be built 
        '''
        summary = set()
        node_size = len(self.graph.nodes())
        for node in self.graph.nodes():
            if self.is_VSN(label):
                path_length = 1
                pri_overlap = self.pri[node]
                sentence = [node]
                score = 0
                self.traverse(summary, score, pri_overlap, sentence, path_length)
                
        # return only top entries in the summary
        final_summary = sorted(summary, key = lambda entry: -entry[1])[:self.parameters.summary_size]
        return final_summary
    
    def traverse(self, summary, node, score, pri_overlap, sentence, path_length):
        ''' Travel through the graph determining candidate summaries '''
        if len(pri_overlap) >= self.parameters.redundancy:
            # if a valid sentence has been found at it as a candidate summary
            if self.is_VEN(node) and self.is_valid_path(sentence): 
                final_score = score / path_length
                summary.add((sentence, final_score))

            for neighbor in self.graph.neighbors(node):
                pri_overlap_new = self._intersection(pri_overlap, self.pri[neighbor])
                redundancy = len(pri_overlap_new)
                new_sentence = sentence + [neighbor]
                new_path_length = path_length + 1

                new_score = self.path_score(new_sentence)
                # TODO: make the new score agree with the definition in the paper shown in comment below
                # new_score = score + self.path_score(redundancy, new_path_length)

                if self.is_collapsible(neighbor):
                    anchor = new_sentence
                    temp = set()
                    for vx in self.graph.neighbors(neighbor):
                        self.traverse(temp, vx, 0, pri_overlap_new, [vx], new_path_length)
                        temp_path_score = sum([self.path_score(path) for path in temp]) / len(temp)
                        final_score = new_score + temp_path_score
                        stiched_sentence = self.stitch(anchor, temp)
                        summary.add((stitched_sentence, final_score))

                else: # neighbor is not collapsible 
                    self.traverse(summary, neighbor, new_score, pri_overlap_new, new_sentence, new_path_length)
                    
    def _intersection(self, pri_1, pri_2):
        ''' Intersection between two position reference information dictionaries 

            This intersection is defined such that the distance between two PIDs must be less 
            than or equal to the gap parameter, sigma_gap in the original paper
        '''
        pri_overlap = set()
        for entry1 in pri_1:
            for entry2 in pri_2:
                if abs(entry1.PID - entry2.PID) < self.parameters.gap:
                    pri_overlap.add(entry1)
                    pri_overlap.add(entry2)
        return pri_overlap

    
                
    
                

