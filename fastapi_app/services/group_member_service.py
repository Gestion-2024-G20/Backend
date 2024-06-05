from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from fastapi_app import schemas, models
from fastapi_app.services.balance_service import create_balance


def get_group_members(
    db: Session,
    skip: int, 
    limit: int, 
    id_group: int,
    id_user: int, 
    is_admin: bool
):    
    query = db.query(schemas.GroupMember)

    if id_group is not None:
        query = query.filter_by(id_group=id_group)

    if id_user is not None:
        query = query.filter_by(id_user=id_user)

    if is_admin is not None:
        query = query.filter_by(is_admin=is_admin)

    groupMembers = query.offset(skip).limit(limit).all()
    
    return [
        models.GroupMember(
            id_gm=gm.id_gm,
            id_group=gm.id_group,
            id_user=gm.id_user,
            is_admin=gm.is_admin,
        ) 

        for gm in groupMembers
    ]
    
def create_group_member(db: Session, group_member: models.GroupMember):
    
    db_group_member = schemas.GroupMember(
        id_group=group_member.id_group,
	    id_user=group_member.id_user,
        is_admin=group_member.is_admin,
    )
    group = db.query(schemas.Group).filter_by(id_group=group_member.id_group).first()
    if group is None: 
         raise KeyError("group_id not found: Group does not exist")
    
    user = db.query(schemas.User).filter_by(id_user=group_member.id_user).first()
    if user is None: 
         raise KeyError("user_id not found: User does not exist")
    group.members_count += 1
    
    db.add(db_group_member)
    db.commit()
    db.refresh(db_group_member)

    create_balance(db, group_member)
    
    return db_group_member
""" 
def update_group_member(db: Session, group_member_id: int, updated_group_member: models.GroupMember):
    db_group_member = db.query(schemas.GroupMember).filter_by(id=group_member_id).first()
    if db_group_member:
        db_group_member.id_group = updated_group_member.id_group
        db_group_member.id_user = updated_group_member.id_user
        db_group_member.is_admin = updated_group_member.is_admin
        db.commit()
        db.refresh(db_group_member)
        return db_group_member
    return None
 """
def delete_group_member(db: Session, group_member_id: int):
    db_group_member = db.query(schemas.GroupMember).filter_by(id_gm=group_member_id).first()
    if db_group_member:
        #print("El user_id del que quiero borrar es ", db_group_member.id_user)

        try:
            # Iniciando una transacción
            with db.begin_nested():
                # Actualización de balances (obtengo aquellas filas que tengan el id_user_1 o el id_user_2 del user_id que quiero borrar y ademas el id_group del user_id que quiero borrar)
                balances_query = db.query(schemas.Balance).filter(
                    and_(
                        schemas.Balance.id_group == db_group_member.id_group,
                        or_(
                            schemas.Balance.id_user_1 == db_group_member.id_user,
                            schemas.Balance.id_user_2 == db_group_member.id_user
                        )
                    )
                )

                #Ejecuto la query!
                balances = balances_query.all()
                #Los printeo para chequear
                # for balance in balances:
                #     balance_id = f"{balance.id_user_1}_{balance.id_user_2}_{balance.id_group}"
                #     #print("El id de balance es: ", balance_id)
                #     print("La fila que quiero borrar de la tabla de Balance es : ", balance_id)

                #Borro las filas correspondientes. El uso de synchronize_session=False es para que no se reflejen automaticamente las filas en la base de datos  puede ser útil en situaciones en las que se desea realizar múltiples operaciones en la base de datos y luego confirmar o revertir todas las operaciones juntas.)
                balances_query.delete(synchronize_session=False)

                # Defino la query para obtener las filas de categorías asociadas al grupo del usuario a borrar (y ademas que el usuario a borrar pertenezca a esa categoria)
                categorias_asociadas_al_grupo = db.query(schemas.Category).join(schemas.CategoryShare, schemas.Category.id_category == schemas.CategoryShare.id_category).filter(
                    schemas.Category.id_group == db_group_member.id_group,
                    schemas.CategoryShare.id_user == db_group_member.id_user
                ).all()
                
                #Las printeo
                # for c in categorias_asociadas_al_grupo:
                #     print("El nombre de las categorias asociadas al id_group de db_group_member es: ", c.name)

                #Defino la query para obtener las filas de category_share donde el id_user NO sea el user_id que quiero borrar (ya que quiero actualizar los porcentajes de los otros id users) y ademas el id_category sea igual a los id_category de las categorías asociadas al grupo del usuario
                category_shares_query = db.query(schemas.CategoryShare).filter(
                    and_(
                        schemas.CategoryShare.id_category.in_([c.id_category for c in categorias_asociadas_al_grupo]),
                        schemas.CategoryShare.id_user != db_group_member.id_user
                    )
                )

                #Ejecuto la query para la tabla de category_share
                category_shares = category_shares_query.all()
                #Printeo las filas
                # for cs in category_shares:
                #     print("Las filas que filtré de la tabla de category_shares son: cs.id_cs =  ", cs.id_cs)

                for cs in category_shares:
                    #Necesito reacomodar los porcentajes dentro de tal categoria, entonces necesito aquellas filas de category_share que coincidan con el mismo id de categoria que el categoryShare que estoy iterando (y que el user_id no sea el id del usuario que quiero borrar)
                    filas_que_comparten_id_category_con_cs = db.query(schemas.CategoryShare).filter(
                        and_(schemas.CategoryShare.id_category == cs.id_category,
                             schemas.CategoryShare.id_user != db_group_member.id_user
                        )
                    ).all()

                    # print("Las filas de category share que necesito reacomodar son: ")
                    # for f in filas_que_comparten_id_category_con_cs:
                    #     print("f.id_cs = ",f.id_cs)

                    if filas_que_comparten_id_category_con_cs:
                        #Sumo los porcentajes para obtener el porcentaje restante, resultado de eliminar al miembro
                        porcentaje_restante = sum(f.share_percentage for f in filas_que_comparten_id_category_con_cs)
                        #Recorro cada fila que necesito actualizarle el porcentaje
                        for f in filas_que_comparten_id_category_con_cs:
                            f.share_percentage = (f.share_percentage / porcentaje_restante) * 100

                # Eliminación de category shares del miembro
                filas_a_eliminar = db.query(schemas.CategoryShare).filter(
                    and_(
                        schemas.CategoryShare.id_category.in_([c.id_category for c in categorias_asociadas_al_grupo]),
                        schemas.CategoryShare.id_user == db_group_member.id_user
                    )
                ).all()

                for f in filas_a_eliminar:
                    # print("Las filas que QUIERO ELIMINAR de la tabla de category_shares son: ", f.id_cs)
                    db.delete(f)

                db.delete(db_group_member)
                db.commit()  # Confirmar todos los cambios
            return True

        except Exception as e:
            db.rollback()  # Revertir cambios en caso de error
            print("Error al eliminar el miembro del grupo:", e)
            return False
    return False

def update_group_member(db: Session, group_member_id: int, updated_group_member: schemas.GroupMember):
    print("El id del group member a actualizar es: ", group_member_id)
    db_group_member = db.query(schemas.GroupMember).filter_by(id_gm=group_member_id).first()
    if db_group_member:
        db_group_member.id_group = updated_group_member.id_group
        db_group_member.id_user = updated_group_member.id_user
        db_group_member.is_admin = updated_group_member.is_admin
        db.commit()
        db.refresh(db_group_member)
        return db_group_member
    return None