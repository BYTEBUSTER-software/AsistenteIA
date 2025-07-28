import bcrypt
class Segutridad :
    def __init__(self):
        print("seguridad en linea")
        pass
    def hash_password(self , plain_password):
        return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()

    def verify_password(self , plain_password, hashed_password):
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
