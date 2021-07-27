# coding=utf-8

import pub.tables.map.files as f



def is_valid_key(key):
    try:
        f.file_key_to_path.objects.get(key=key)
        return False
    except:
        try:
            f.file_key_to_user.object.get(key=key)
            return False
        except:
            try:
                f.file_hash_to_key.objects.get(key=key)
                return False
            except:
                return True