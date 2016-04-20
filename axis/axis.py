"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, Dict, String
from xblock.fragment import Fragment

import logging
log = logging.getLogger(__name__)

import random
#NUMPY IS NOT IN XBLOCK'S REQUIREMENTS - MAY NOT BE AVAILABLE IN EDX ENVIRONMENT
import numpy
#not sure if operator is standard in 2.7, but i think it is.
import operator


class AxisXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    #TODO: make all user_state_summary scoped vars Dicts keyed on versionX
    count = Integer(
        default=0, scope=Scope.user_state, help="A simple counter, to show something happening")
    rating_v1 = Integer(
        default=0, scope=Scope.user_state, help="This user's rating for mooclet version 1")
    rating_v2 = Integer(
        default=0, scope=Scope.user_state, help="This user's rating for mooclet version 2")
    sum_rating_v1 = Integer(
        default=0, scope=Scope.user_state_summary, help="The sum rating of mooclet version 1 for all users (for calculating the mean)")
    count_rating_v1 = Integer(
        default=0, scope=Scope.user_state_summary, help="The number of users who have rated mooclet version 1. Helpful in calculating mean")
    successes_v1 = Integer(
        default=0, scope=Scope.user_state_summary, help="The number of successes mooclet version 1.")
    failures_v1 = Integer(
        default=0, scope=Scope.user_state_summary, help="The number of failures mooclet version 1.")
    sum_rating_v2 = Integer(
        default=0, scope=Scope.user_state_summary, help="The sum rating of mooclet version 2 for all users (for calculating the mean)")
    count_rating_v2 = Integer(
        default=0, scope=Scope.user_state_summary, help="The number of users who have rated mooclet version 2. Helpful in calculating mean")
    successes_v2 = Integer(
        default=0, scope=Scope.user_state_summary, help="The number of successes mooclet version 2.")
    failures_v2 = Integer(
        default=0, scope=Scope.user_state_summary, help="The number of failures mooclet version 2.")

    hints = Dict(default={'version1': 'Explanation 1', 'version2': 'Explanation 2'}, scope=Scope.content, help="the set of explanations.")

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the AxisXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/axis.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/axis.css"))
        frag.add_javascript(self.resource_string("static/js/src/axis.js"))
        frag.initialize_js('AxisXBlock')
        return frag

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def increment_count(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}

    @XBlock.json_handler
    def update_rating(self, data, suffix=''):
        #TODO: Make this version agnostic, but make sure that we are gettomg the correct version to update from the page
        
        if 'version1Rating' in data:
            rating = int(data['version1Rating']) 
            self.rating_v1 = rating 
            self.sum_rating_v1 += rating 
            self.count_rating_v1 += 1
            if rating >= 4:
                self.successes_v1 += 1
            else:
                self.failures_v1 += 1

            #return data['version1Rating']

            
        elif 'version2Rating' in data:
            rating = int(data['version2Rating'])
            self.rating_v2 = rating
            self.sum_rating_v2 += rating 
            
            self.count_rating_v2 += 1
            if rating >= 4:
                self.successes_v2 += 1
            else:
                self.failures_v2 += 1
            #return data['version2Rating']

        else:
            return data
        return {'ratingv1': self.rating_v1, 'count_rating_v1': self.count_rating_v1, 'ratingv2': self.rating_v2, 'count_rating_v2': self.count_rating_v2}


    @XBlock.json_handler
    def pick_version_random(self, data, suffix=''):
        #TODO add ratings (when we understand this)
        versions = ['version1','version2']
        version = random.choice(versions)
        return {"version": version}

    @XBlock.json_handler
    def pick_version_thompson(self, data, suffix=''):
        #TODO add ratings (when we understand this)
        versions = self.hints.keys()
        successes = [self.successes_v1, self.successes_v2]
        failures = [self.failures_v1, self.failures_v2]
        betas = {}
        for version in zip(versions, successes, failures):
            if version[1] > 0 and version[2] > 0:
                betas[version[0]] = (numpy.random.beta(version[1], version[2]))
            else:
                betas[version[0]] = random.random()
        

        version = max(betas.iteritems(), key=operator.itemgetter(1))[0]
        return {"version": self.hints[version]}



    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("AxisXBlock",
             """<axis/>
             """),
            ("Multiple AxisXBlock",
             """<vertical_demo>
                <axis/>
                <axis/>
                <axis/>
                </vertical_demo>
             """),
        ]
