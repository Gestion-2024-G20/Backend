from pyparsing import List
from sqlalchemy.orm import Session
from fastapi_app import schemas, models
from fastapi_app.services.user_service import get_user
from fastapi_app.services.category_service import get_categories

def add_value_to_dict(dic, key, value):
    if key not in dic:
        dic[key] = value
    else:
        dic[key] += value
    
    return dic

def convert_sum_to_percetentage(dic):
    total_sum = sum(dic.values())

    percentage_dict = {
        key: value/total_sum * 100
        for key, value in dic.items()
    }

    return percentage_dict

def get_statistics(db: Session, id_group: int):
    expenditures = db.query(schemas.Expenditure).filter_by(id_group=id_group).all()
    if expenditures is None: 
        raise KeyError("No expenditure found")

    sum_by_category = {}
    sum_by_user = {}
    sum_by_category_and_user = {}        

    for expenditure in expenditures:
        user = get_user(db, expenditure.id_user).username
        category = get_categories(db=db, id_group=expenditure.id_group, id_category=expenditure.id_category, skip=0, limit=1, name=None)[0].name
        amount = expenditure.amount

        sum_by_category = add_value_to_dict(sum_by_category, category, amount)
        sum_by_user = add_value_to_dict(sum_by_user, user, amount)
        if category not in sum_by_category_and_user:
            sum_by_category_and_user[category] = {}
        sum_by_category_and_user[category] = add_value_to_dict(sum_by_category_and_user[category],user, amount)

    percentages_by_user=convert_sum_to_percetentage(sum_by_user)
    percentages_by_category=convert_sum_to_percetentage(sum_by_category)
    percentages_by_category_and_user = {
        category: convert_sum_to_percetentage(dic)
        for category, dic in sum_by_category_and_user.items()
    }

    return models.Statistics(
	    percentages_by_user=percentages_by_user,
	    percentages_by_category=percentages_by_category,
	    percentages_by_category_and_user=percentages_by_category_and_user
    )  
