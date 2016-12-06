from le_dash.banner import get_student_list


def test_get_student_info(mocker, student_list_maker):
    fake_students = student_list_maker(
        ('12345', 'foo', 'b', 'baz'),
        ('12345', 'jane', 'q', 'public'),
        ('12345', 'fozzy', '', 'bear', 'Withdraw')
    )
    resp_data = {
        "students": {
            "student": [x for x in fake_students]
        }
    }
    mocker.patch('le_dash.banner.banner_req', return_value=resp_data)

    students = get_student_list("9999999")
    assert len(students) == 2
    assert students[1]['first_name'] == 'jane'


def test_get_student_info_one_result(mocker, student_maker):
    resp_data = {
        "students": {
            "student": student_maker('23456', 'arther', 'j', 'fonzarelli')
        }
    }
    mocker.patch('le_dash.banner.banner_req', return_value=resp_data)

    students = get_student_list("10101010")
    assert isinstance(students, list)
    assert len(students) == 1
    assert students[0]['huid'] == '23456'


def test_get_student_info_no_results(mocker):

    mocker.patch('le_dash.banner.banner_req',
                 return_value={'students': {}})
    students = get_student_list("33434334")
    assert len(students) == 0
