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

    # 2 Load roles with scope
    for role_name, role_data in policies["roles"].items():

        scope_type = role_data["scope"]
        perm_codes = role_data["permissions"]

        role = await db.scalar(
            select(Role).where(Role.name == role_name)
        )

        if not role:
            role = Role(
                name=role_name,
                scope_type=scope_type
            )
            db.add(role)
            await db.commit()
        else:
            # Optional: update scope if changed
            role.scope_type = scope_type
            await db.commit()

        # 3 Map permissions
        for code in perm_codes:

            if code.endswith(".*"):
                resource = code.split(".")[0]
                perms = (
                    await db.scalars(
                        select(Permission).where(Permission.resource == resource)
                    )
                ).all()
            else:
                perm = await db.scalar(
                    select(Permission).where(Permission.code == code)
                )
                perms = [perm] if perm else []

            for p in perms:
                exists = await db.scalar(
                    select(RolePermission).where(
                        RolePermission.role_id == role.id,
                        RolePermission.permission_id == p.id
                    )
                )

                if not exists:
                    db.add(RolePermission(
                        role_id=role.id,
                        permission_id=p.id
                    ))

        await db.commit()