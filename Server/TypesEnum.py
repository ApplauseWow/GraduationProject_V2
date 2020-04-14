# -*-coding:utf-8-*-
from enum import Enum
from enum import unique


@unique
class ClientRequest(Enum):
    """
    前后端通信交互接口
    客户端请求成功与否枚举类
    0:请求失败 1:请求成功
    """

    Failure = 0

    Success = 1


@unique
class ProcessOperation(Enum):
    """
    非数据库相关的其他处理加工操作交互接口
    非数据库相关的其他处理加工操作成功与否枚举类
    0:操作失败 1:操作成功
    """

    Failure = 0

    Success = 1


@unique
class DBOperation(Enum):
    """
    数据库交互接口
    数据库操作成功与否枚举类
    0:操作失败 1:操作成功
    """

    Failure = 0

    Success = 1


@unique
class UserType(Enum):
    """
    user_info表　user_tyoe
    用户类型枚举类
    0:学生 1:教师
    """

    Student = 0

    Teacher = 1


@unique
class NoteStatus(Enum):
    """
    note_info表 is_valid
    公告是否有效
    0:公告过期 1:公告未过期
    """

    Invalid = 0

    Valid = 1


@unique
class AchievementType(Enum):
    """
    achievement_info表 ach_type
    成就类型
    0:竞赛 1:软著　2:实用创新型 3:专利 4:论文
    """

    Competition = 0

    SoftwareCopyright = 1

    UtilityModel = 2

    Patent = 3

    Paper = 4


@unique
class CompetitionGrade(Enum):
    """
    competition_info表 grade
    比赛级别
    0:未知 1:院级 2:校级 3:区级 4:市级 5:省级 6:国家级 7:世界级
    """

    Unknown = 0

    College = 1

    Campus = 2

    District = 3

    City = 4

    Province = 5

    Nation = 6

    World = 7


@unique
class CompetitionType(Enum):
    """
    competition_info表 comp_type
    比赛类型
    0:未知 1:B类 2:A类
    """

    Unknown = 0

    Class_B = 1

    Class_A = 2


@unique
class CompetitionStatus(Enum):
    """
    competition_info表 comp_status
    比赛状态（进度）
    -1:比赛作废 0:尚未开赛 1:开始报名 2:进行阶段 3:比赛结束
    """

    Absence = -1

    Preparation = 0

    Registration = 1

    Start = 2

    Finish = 3


@unique
class Awards(Enum):
    """
    competition_info表 is_awarded
    比赛获奖情况
    0:未获奖/尚未获奖　1:获奖
    """

    NotAwarded = 0

    Awarded = 1


@unique
class AttendanceType(Enum):
    """
    attendance_record表 record_type
    考勤类型
    0:上岗 1:下班
    """

    ClockIn = 0

    ClockOut = 1


@unique
class GroupMemberType(Enum):
    """
    group_member表 member_type
    小组成员类型
    0:普通组员 1:组长 2:指导老师
    """

    Member = 0

    Leader = 1

    Teacher = 2


@unique
class RequestType(Enum):
    """
    leave_permit_info表 req_type
    请假类型
    0:其他　1:病假　2:公事假
    """

    Other = 0

    Sick = 1

    Affair = 2


@unique
class Permission(Enum):
    """
    leave_permit_info表 is_permited
    假条批准情况
    0:不允许　1:允许
    """

    Deny = 0

    Allow = 1


@unique
class ProjectProgress(Enum):
    """
    project_info表 is_done
    项目进度
    0:未完成 1:完成
    """

    NotDone = 0

    IsDone = 1


@unique
class SeatMember(Enum):
    """
    seat_arrangement表 is_leader
    工位成员
    0:普通轮流使用者 1:负责人
    """

    Member = 0

    Leader = 1


@unique
class TaskProgress(Enum):
    """
    self_task表 is_done
    个人任务进度
    0:未完成　1:已完成
    """

    NotDone = 0

    IsDone = 1