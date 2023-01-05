from ldap3 import Server, Connection, ALL_ATTRIBUTES, SYNC, SIMPLE, SUBTREE, ALL
import json




def auth_ldap(user, pwd):
    try:
        server = Server('10.114.118.39', get_info=None)
        conn = Connection(server, client_strategy='ASYNC', user=f'{user.lower()}@lginnotek.com', password=pwd, check_names=False,
                          raise_exceptions=False)

        status = conn.bind()
        conn.unbind()
    except:
        status = False
    return status

def get_user_profile(usr, pwd):
    server = Server('10.114.118.39', get_info=ALL)
    conn = Connection(server, user=f'{usr}@lginnotek.com', password=pwd, auto_bind=True)
    conn.search(search_base=f'DC=lginnotek,DC=com',
                search_filter=f'(&(objectClass=user)(|(sAMAccountName={usr})(mail={usr})))',
                search_scope=SUBTREE,
                attributes=['*'])
    status = json.loads(conn.response_to_json())
    
    return status