from ...subject.models import Subject, TaskSolve, TestSolve, Task, Content
import datetime
import time
import json
from ...extensions import db



def get_user_task(user, subject, number, count):
    #First we get all user's tasks solve that know what tasks he already solved
    query = db.session.query(Subject, Task, TaskSolve, Content).filter(Subject.codename == subject.codename)
    query = query.join(Task).filter(Task.number == number, Task.open == 1)
    query = query.join(TaskSolve).filter(TaskSolve.solve == 1, TaskSolve.user_id == user.id)
    query = query.order_by(TaskSolve.alltime.asc()).all()
    task_solved_id = []
    for s, t, ts, c in query:
        task_solved_id.append(ts.task_id)
    user_future_task = db.session.query(Subject, Task, TaskSolve, Content).filter(Subject.codename == subject.codename)
    user_future_task = user_future_task.join(Task).filter(Task.number == number, Task.open == 1, ~Task.id.in_(task_solved_id)).limit(count).all()
    if len(user_future_task) < count:
        for i in range(count-len(query)):
            if len(query) > i:
                user_future_task.append(query[i])
    final = []
    for s, t, ts, c in user_future_task:
        final.append({
            "id": t.id,
            "number": t.number,
            "content": json.loads(c.content)
        })
    return final
