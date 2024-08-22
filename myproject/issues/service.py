from users.models import User
from issues.models import Issue, IssueComment
from common.webCommon import ResponsObject
from repository.models import Project

class IssueService():
    userModel = User()
    issue = Issue()
    project = Project()
    issueComment = IssueComment()
    response = ResponsObject()

    def findIssue(self, trueOrFalse, user, params, id):
        issues = None
        if user != 'author':
            user = self.userModel.get_by_id(user)
            if user is None:
                return {"status": "FALSE", "message": "USER_NOT_FOUND"}

            if params != 'status':
                issues = self.issue.filter_issue_by_user_status(id, trueOrFalse, user)
            else:
                issues = self.issue.filter_issue_by_user(id, user)
        else:
            if params != 'status':
                issues = self.issue.filter_issue_by_status(id, trueOrFalse)
            else:
                issues = self.issue.filter_issue(id)
        
        if issues is None:
            return {"status": "FALSE", "message": "ISSUES_NOT_FOUND"}

        return self.response.issuesSerialize(issues)
    
    def createNewIssue(self, user, data):
        projectData = self.project.get_by_id(data['id'])
        if projectData is None:
            return {"status": "FALSE", "message": "PROJECT_NOT_FOUND"}

        userData = self.userModel.get_by_id(user['id'])
        if userData is None:
            return {"status": "FALSE", "message": "USER_NOT_FOUND"}

        issue = self.issue.create(data, projectData, userData)
        if issue is None:
            return {"status": "FALSE", "message": "ADD_NEW_ISSUE_FALSE"}

        return self.response.issueSerialize(issue)
    
    def createNewComment(self, user, data):
        issue = self.issue.get_by_id(data['id'])
        if issue is None:
            return {"status": "FALSE", "message": "ISSUE_NOT_FOUNE"}
        
        user1 = self.userModel.get_by_id(int(user['id']))
        if user1 is None:
            return {"status": "FALSE", "message": "USER_NOT_FOUND"}

        issueComment = self.issueComment.create(
            data['comment'], issue, user1, "COMMENT")

        return self.response.issueCommentSerialize(issueComment)
    
    def getCommentByIssue(self, id):
        issue = self.issue.get_by_id(id)
        if issue is None:
            return {"status": "FALSE", "message": "ISSUE_NOT_FOUNE"}
        
        issue_comment = self.issueComment.filterByIssue(issue)
        if issue_comment is None:
            return {"status": "FALSE", "message": "ISSUE_COMMENT_NOT_FOUND"}

        return self.response.issuesCommentSerialize(issue_comment)
    
    def assignedToIssue(self, user, data):
        issue = self.issue.get_by_id(data['id'])
        if issue is None:
            return {"status": "FALSE", "message": "ISSUE_NOT_FOUNE"}
        
        user1 = self.userModel.get_by_id(int(user['id']))
        if user1 is None:
            return {"status": "FALSE", "message": "USER_NOT_FOUNE"}

        issue.assigned.add(user1)
        issue.save()

        comment = user1.firstName + ' ' + user1.lastName + \
            ' assigned to issue #' + str(issue.id) + '.'

        issueComment = self.issueComment.create(
            comment, issue, user1, "AUTOGENERATE")

        return self.response.issueCommentSerialize(issueComment)
    
    def editIssue(self, user, data):
        issue = self.issue.get_by_id(data['id'])
        user1 = self.userService.getUserById(int(user['id']))

        issue.name = data['name']
        issue.description = data['description']
        issue.save()

        comment = user1.firstName + ' ' + user1.lastName + ' has edited this issue.'
        issueComment = self.issueComment.create(
            comment, issue, user1, "AUTOGENERATE")

        return {"message": "SUCCESS", "data": self.response.issueCommentSerialize(issueComment)}
    
    def closeIssue(self, idIssue, user):
        issue = self.issue.get_by_id(idIssue)
        if issue is None:
            return {"status": "FALSE", "message": "ISSUE_NOT_FOUND"}
    
        if issue.status == False:
            return {"message": "FALSE", "data": "ISSUE_IS_CLOSSE"}
    
        user1 = self.userModel.get_by_id(int(user['id']))
        if user1 is None:
            return {"status": "FALSE", "message": "USER_NOT_FOUND"}        

        issue.status = False
        issue.save()

        comment = user1.username + \
            ' has closed issue #' + str(idIssue) + '.'

        issueComment = self.issueComment.create(
            comment, issue, user1, "AUTOGENERATE")

        return self.response.issueCommentSerialize(issueComment)
    
    def updateLabels(self, issueId, label, user):
        issue = self.issue.get_by_id(issueId)
        user1 = self.userService.getUserById(int(user))
        issue.labels = label
        issue.save()

        comment = '<span style="color: green">' + user1.username + '</span>' \
            ' set labels to issue #' + str(issue.id) + '.'

        issueComment = self.issueComment.create(
            comment, issue, user1, "AUTOGENERATE")

        return {"message": "SUCCESS", "data": self.response.issueCommentSerialize(issueComment)}