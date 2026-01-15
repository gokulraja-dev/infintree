import yaml
from sqlalchemy import select
from app.modules.permissions.model import Permission, Role, RolePermission

async def load_iam_policies(db):

    with open("app/policies/iam_policies.yaml") as f:
        policies = yaml.safe_load(f)

    # 1 Load permissions
    for p in policies["permissions"]:
        exists = await db.scalar(select(Permission).where(Permission.code == p["code"]))
        if not exists:
            db.add(Permission(**p))
    await db.commit()

    # 2 Load roles & map permissions
    for role_name, perm_codes in policies["roles"].items():
        role = await db.scalar(select(Role).where(Role.name == role_name))
        if not role:
            role = Role(name=role_name)
            db.add(role)
            await db.commit()

        for code in perm_codes:
            if code.endswith(".*"):
                scope = code.split(".")[0]
                perms = (await db.scalars(
                    select(Permission).where(Permission.resource == scope)
                )).all()
            else:
                perms = [await db.scalar(select(Permission).where(Permission.code == code))]

            for p in perms:
                if not p:
                    continue
                exists = await db.scalar(select(RolePermission).where(
                    RolePermission.role_id == role.id,
                    RolePermission.permission_id == p.id
                ))
                if not exists:
                    db.add(RolePermission(role_id=role.id, permission_id=p.id))

        await db.commit()