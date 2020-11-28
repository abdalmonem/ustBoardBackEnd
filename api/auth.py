from flask import Blueprint, request

from Util.Iam import Iam
from Util.Validate import Validate, ValidateConstrins, ConstrinsType
from Util.ConnectionWorker import ConnectionWorker
from main_classes.Student import Student
from main_classes.User import User, Users, UserRank

auth = Blueprint('auth', __name__, url_prefix='/api')


@auth.route('/join', methods=["GET", "POST"])
def join():
    name = request.args.get('name', None)
    username = request.args.get('username', None)
    country = request.args.get('country', None)
    email = request.args.get('email', None)
    phone = request.args.get('phone', None)
    password = request.args.get('password', None)

    username_validate = Validate().is_valid(
        parameter_name='username',
        parameter_value=username,
        constrins=ValidateConstrins(
            min_lenth=3,
            max_lenth=15,
            is_required=True,
            type=ConstrinsType.username
        )
    )
    if not username_validate.is_valid:
        return ConnectionWorker().create_response(reason=username_validate.reason, state=username_validate.is_valid)

    if email is not None:
        email_validate = Validate().is_valid(
            parameter_name='email',
            parameter_value=email,
            constrins=ValidateConstrins(
                is_required=True,
                type=ConstrinsType.email
            )
        )
        if not email_validate.is_valid:
            return ConnectionWorker().create_response(reason=email_validate.reason, state=email_validate.is_valid)

    # في حال سجل برقم التلفون
    if email is None and phone is not None:
        phone_validate = Validate().is_valid(
            parameter_name='phone',
            parameter_value=phone,
            constrins=ValidateConstrins(
                is_required=True,
                type=ConstrinsType.integer
            )
        )
        if not phone_validate.is_valid:
            return ConnectionWorker().create_response(reason=phone_validate.reason, state=phone_validate.is_valid)

    # المستخدم لا دخل تلفون لا إيميل
    if phone is None and email is None:
        return ConnectionWorker().create_response(reason="no phone or email added", state=False)

    # التحقق من الدولة
    country_validate = Validate().is_valid(
        parameter_name='country',
        parameter_value=country,
        constrins=ValidateConstrins(
            min_lenth=2,
            max_lenth=2,
            is_required=True,
            type=ConstrinsType.englishAlpha
        )
    )
    if not country_validate.is_valid:
        return ConnectionWorker().create_response(reason=country_validate.reason, state=country_validate.is_valid)

    # التحقق من كلمة المرور
    password_validate = Validate().is_valid(
        parameter_name='password',
        parameter_value=password,
        constrins=ValidateConstrins(
            min_lenth=7,
            max_lenth=10,
            is_required=True,
        )
    )
    if not password_validate.is_valid:
        return ConnectionWorker().create_response(reason=password_validate.reason, state=password_validate.is_valid)

    users = Users()
    return users.login(username="admin", password="abcdefgh")
    # x = users.get(list_of_fields=[User.username, User.email], list_of_filters=[User.username == "www"])
    # print(x[0].email)
    # user_obj.set_email(email)
    # user_obj.set_phone(phone)
    # user_obj.set_email(email)
    # user_obj.set_username(username)
    # user_obj.create()

    # user_obj.add()

    return username_validate.reason + " " + username + str(username_validate.is_valid)

    multi_dict = request.args
    allparams = [];
    for di in multi_dict:
        allparams.append(di)
    return ''.join(allparams)


@auth.route('/login', methods=["GET", "POST"])
def login():
    username = request.args.get('username', None)
    email = request.args.get('email', None)
    phone = request.args.get('phone', None)
    password = request.args.get('password', None)
    return Users().login(username=username, phone=phone, email=email, password=password)


@auth.route('/add_user', methods=["GET", "POST"])
def add_user():
    iam = Iam()
    if not iam.is_login():
        return ConnectionWorker().create_response(reason="not authorized", state=False)

    name = request.args.get('name', None)
    username = request.args.get('username', None)
    email = request.args.get('email', None)
    phone = request.args.get('phone', None)
    password = request.args.get('password', None)
    type = request.args.get('type', None)

    username_validate = Validate().is_valid(
        parameter_name='username',
        parameter_value=username,
        constrins=ValidateConstrins(
            min_lenth=3,
            max_lenth=15,
            is_required=True,
            type=ConstrinsType.username
        )
    )
    if not username_validate.is_valid:
        return ConnectionWorker().create_response(reason=username_validate.reason, state=username_validate.is_valid)

    if email is not None:
        email_validate = Validate().is_valid(
            parameter_name='email',
            parameter_value=email,
            constrins=ValidateConstrins(
                is_required=True,
                type=ConstrinsType.email
            )
        )
        if not email_validate.is_valid:
            return ConnectionWorker().create_response(reason=email_validate.reason, state=email_validate.is_valid)

    # في حال سجل برقم التلفون
    if email is None and phone is not None:
        phone_validate = Validate().is_valid(
            parameter_name='phone',
            parameter_value=phone,
            constrins=ValidateConstrins(
                is_required=True,
                type=ConstrinsType.integer
            )
        )
        if not phone_validate.is_valid:
            return ConnectionWorker().create_response(reason=phone_validate.reason, state=phone_validate.is_valid)

    # المستخدم لا دخل تلفون لا إيميل
    if phone is None and email is None:
        return ConnectionWorker().create_response(reason="no phone or email added", state=False)


    # التحقق من كلمة المرور
    # password_validate = Validate().is_valid(
    #     parameter_name='password',
    #     parameter_value=password,
    #     constrins=ValidateConstrins(
    #         min_lenth=7,
    #         max_lenth=10,
    #         is_required=True,
    #     )
    # )
    # if not password_validate.is_valid:
    #     return ConnectionWorker().create_response(reason=password_validate.reason, state=password_validate.is_valid)

    # التحقق من تمرير النوع
    type_validate = Validate().is_valid(
        parameter_name='type',
        parameter_value=type,
        constrins=ValidateConstrins(
            is_required=True,
            type=ConstrinsType.integer
        )
    )
    if not type_validate.is_valid:
        return ConnectionWorker().create_response(reason=type_validate.reason, state=type_validate.is_valid)

    # في إكسبشن حا يحصل حا أشرحه ليكم عشان نتلافاه عملنا الشرط دا
    if int(type) > 3 or int(type) < 0:
        return ConnectionWorker().create_response(state=False, reason="user type is invalid option")


    allowed_add_ranks = []
    if iam.get_rank() == UserRank.admin:
        allowed_add_ranks.append(UserRank.supervisor)
        allowed_add_ranks.append(UserRank.teacher)
    elif iam.get_rank() == UserRank.supervisor:
        allowed_add_ranks.append(UserRank.student)

    # نوع المستخدم المسجل دخول ما بسمح بالإضافة
    if len(allowed_add_ranks) < 1:
        return ConnectionWorker().create_response(reason="user add denied", state=False)
    if UserRank(int(type)) not in allowed_add_ranks:
        return ConnectionWorker().create_response(reason="user type not allowed", state=False)

    new_user_object = User()
    new_user_object.set_email(email)
    new_user_object.set_rank(UserRank(int(type)))
    new_user_object.set_phone(phone)
    new_user_object.set_email(email)
    new_user_object.set_username(username)
    return Users().create(user=new_user_object)
