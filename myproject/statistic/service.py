from common.webCommon import ResponsObject
from repository.models import Project
from issues.models import Issue
from statistic.models import Statistic
import json

class StatisticService():
    responseObject = ResponsObject()
    project = Project()
    issue = Issue()
    staticsti = Statistic()

    def getStatistic(self, id):
        project1 = self.project.get_by_id(id)
        if project1 is None:
            return {"status": "FALSE", "message": "PROJECT_NOT_FOUND"}
        
        staticstic1 = self.staticsti.findByProjct(project1)
        if staticstic1 is None:
            return {"status": "FALSE", "message": "STATISTIC_NOT_FOUND_PROJECT"}
        
        issues1 = self.issue.filter_issue(project1)
        if issues1 is None:
            return {"status": "FALSE", "message": "STATISTIC_NOT_FOUND_ISSUE"}

        count_of_ammount = []
        number_of_mounts = 12
        for i in range(number_of_mounts):
            count = staticstic1.filter(dateCreate__month=str(i+1))
            count_of_ammount.append(len(count))
        
        count_of_issues = []
        count_true = 0
        count_false = 0
        for i in issues1:
            if i.status == True:
                count_false += 1
            if i.status == False:
                count_true += 1
        
        count_of_issues.append(count_false)
        count_of_issues.append(count_true)

        dataRes = '{"count_of_ammount": ' + str(count_of_ammount) + \
            ', "count_of_issues": ' + str(count_of_issues) + '}'
        
        return json.loads(dataRes)